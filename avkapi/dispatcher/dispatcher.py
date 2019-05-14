import asyncio
import functools
import logging

from .handler import Handler
from .middlewares import MiddlewareManager
from .storage import DisabledStorage
from .filters import FiltersFactory
from ..types import Message, MessageType, VKException, Event
from ..utils.mixins import ContextInstanceMixin, DataMixin
from ..vk import VK

MODE = 'MODE'
LONG_POLLING = 'long-polling'
EVENT_OBJECT = 'event_object'

logger = logging.getLogger(__name__)


class Dispatcher(DataMixin, ContextInstanceMixin):
    def __init__(self, vk, storage=None, loop=None, filters_factory=None):
        if loop is None:
            loop = vk.loop or asyncio.get_event_loop()

        if storage is None:
            storage = DisabledStorage()

        if filters_factory is None:
            filters_factory = FiltersFactory(self)

        self.storage = storage or DisabledStorage()
        self.vk: VK = vk
        self.loop = loop
        self.run_tasks_by_default = True

        self.filters_factory: FiltersFactory = filters_factory
        self.events_handler = Handler(self, middleware_key='event')
        self.message_handlers = Handler(self, middleware_key='message')
        self.errors_handlers = Handler(self, once=False, middleware_key='error')

        self.middleware = MiddlewareManager(self)
        self.events_handler.register(self.process_event)

        self._polling = False
        self._closed = True
        self._close_waiter = loop.create_future()

        self._key = None
        self._server = None
        self._ts = None

    async def start_polling(self, group_id, relax=0.1):
        """
        Start long-polling

        :return:
        """
        if self._polling:
            raise RuntimeError('Polling already started')

        logger.info('Start polling.')

        # context
        Dispatcher.set_current(self)
        VK.set_current(self.vk)

        self._polling = True
        ts = None
        try:
            while self._polling:
                try:
                    if ts is None:
                        _data = await self.vk.groups.get_long_poll_server(group_id)
                        self._key = _data.get('key')
                        self._server = _data.get('server')
                        ts = _data.get('ts')
                    ts, events = await self.vk.act_a_check(key=self._key, server=self._server, ts=ts)

                except VKException:
                    logger.exception('Cause exception while getting events.')
                    await asyncio.sleep(15)
                    continue

                if events:
                    logger.debug(f"Received {len(events)} events.")
                    self.loop.create_task(self.process_events(events))

                if relax:
                    await asyncio.sleep(relax)
        finally:
            logger.warning('Polling is stopped.')

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
        Event.set_current(event)

        if event.message and isinstance(event.message, Message):
            msg = event.message
            logger.info(f"Received message from {msg.from_id}, text: {msg.text}")
            return await self.message_handlers.notify(msg)

        else:
            logger.error('ERROR! HELP ME!')

    def register_message_handler(self, callback, *, commands=None, regexp=None, content_types=None, func=None,
                                 state=None, custom_filters=None, run_task=None, **kwargs):
        filters_set = self.filters_factory.resolve(self.message_handlers,
                                                   *custom_filters,
                                                   commands=commands,
                                                   regexp=regexp,
                                                   content_types=content_types,
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

    async def wait_closed(self):
        """
        Wait for the long-polling to close

        :return:
        """
        await asyncio.shield(self._close_waiter, loop=self.loop)

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
