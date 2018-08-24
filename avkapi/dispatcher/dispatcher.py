import asyncio
import functools
import logging

from .filters import generate_default_filters
from .handler import Handler
from .storage import DisabledStorage
from .middlewares import MiddlewareManager

from ..types import Message, MessageType
from ..utils import context
from ..vk import VK

EVENT_OBJECT = 'event_object'

logger = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self, vk, storage=None, loop=None):
        if loop is None:
            loop = vk.loop

        self.storage = storage or DisabledStorage()
        self.vk: VK = vk
        self.loop = loop
        self.run_tasks_by_default = True

        self.events_handler = Handler(self, middleware_key='event')
        self.message_handlers = Handler(self, middleware_key='message')
        self.errors_handlers = Handler(self, once=False, middleware_key='error')

        self.middleware = MiddlewareManager(self)
        self.events_handler.register(self.process_event)

        self._polling = False
        self._closed = True
        self._close_waiter = loop.create_future()

    async def process_events(self, events):
        """
        Process list of updates

        :param events:
        :return:
        """
        tasks = []
        for event in events:
            tasks.append(self.events_handler.notify(event))
        return await asyncio.gather(*tasks)

    async def process_event(self, event):
        """
        Process single event object

        :param event:
        :return:
        """
        context.set_value(EVENT_OBJECT, event)

        if event.message and isinstance(event.message, Message):
            msg = event.message
            logger.info(f"Received message from {msg.from_id}, text: {msg.text}")
            return await self.message_handlers.notify(msg)

        else:
            logger.error('ERROR! HELP ME!')

    def register_message_handler(self, callback, *, commands=None, regexp=None, content_types=None, func=None,
                                 state=None, custom_filters=None, run_task=None, **kwargs):
        if content_types is None:
            content_types = MessageType.ANY

        if custom_filters is None:
            custom_filters = []

        filters_set = generate_default_filters(self,
                                               *custom_filters,
                                               commands=commands,
                                               regexp=regexp,
                                               content_types=content_types,
                                               func=func,
                                               state=state,
                                               **kwargs)

        self.message_handlers.register(self._wrap_async_task(callback, run_task), filters_set)

    def message_handler(self, *custom_filters, commands=None, regexp=None, content_types=None, func=None, state=None,
                        run_task=None, **kwargs):

        def decorator(callback):
            self.register_message_handler(callback,
                                          commands=commands, regexp=regexp, content_types=content_types,
                                          func=func, state=state, custom_filters=custom_filters, run_task=run_task,
                                          **kwargs)
            return callback

        return decorator

    def async_task(self, func):
        """
        Execute handler as task and return None.


        :param func:
        :return:
        """

        def process_response(task):
            try:
                task.result()

            except Exception as e:
                self.loop.create_task(
                    self.errors_handlers.notify(self, task.context.get(EVENT_OBJECT, None), e))

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            task = self.loop.create_task(func(*args, **kwargs))
            task.add_done_callback(process_response)

        return wrapper

    def _wrap_async_task(self, callback, run_task=None) -> callable:
        if run_task is None:
            run_task = self.run_tasks_by_default

        if run_task:
            return self.async_task(callback)
        return callback

    def stop_polling(self):
        """
        Break long-polling process.

        :return:
        """
        if self._polling:
            logger.info('Stop polling...')
            self._polling = False

    async def wait_closed(self):
        """
        Wait for the long-polling to close

        :return:
        """
        await asyncio.shield(self._close_waiter, loop=self.loop)

    def is_polling(self):
        """
        Check if polling is enabled

        :return:
        """
        return self._polling
