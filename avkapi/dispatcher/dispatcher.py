import asyncio
import functools
import logging

from .filters import generate_default_filters
from .handler import Handler
from .middlewares import MiddlewareManager
from .storage import DisabledStorage
from ..types import Message, MessageType
from ..utils import context
from ..utils.mixins import ContextInstanceMixin, DataMixin
from ..vk import VK

EVENT_OBJECT = 'event_object'

logger = logging.getLogger(__name__)


class Dispatcher(DataMixin, ContextInstanceMixin):
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

    #
    # def stop_polling(self):
    #     """
    #     Break long-polling process.
    #     :return:
    #     """
    #     if hasattr(self, '_polling') and self._polling:
    #         logger.info('Stop polling...')
    #         self._polling = False
    #
    # async def start_polling(self, timeout=20, relax=0.1, limit=None, reset_webhook=None,
    #                         fast: typing.Optional[bool] = True):
    #     """
    #     Start long-polling
    #     :param timeout:
    #     :param relax:
    #     :param limit:
    #     :param reset_webhook:
    #     :param fast:
    #     :return:
    #     """
    #     if self._polling:
    #         raise RuntimeError('Polling already started')
    #
    #     logger.info('Start polling.')
    #
    #     # context.set_value(MODE, LONG_POLLING)
    #     Dispatcher.set_current(self)
    #     Bot.set_current(self.bot)
    #
    #     if reset_webhook is None:
    #         await self.reset_webhook(check=False)
    #     if reset_webhook:
    #         await self.reset_webhook(check=True)
    #
    #     self._polling = True
    #     offset = None
    #     try:
    #         while self._polling:
    #             try:
    #                 updates = await self.bot.get_updates(limit=limit, offset=offset, timeout=timeout)
    #             except:
    #                 logger.exception('Cause exception while getting updates.')
    #                 await asyncio.sleep(15)
    #                 continue
    #
    #             if updates:
    #                 logger.debug(f"Received {len(updates)} updates.")
    #                 offset = updates[-1].update_id + 1
    #
    #                 self.loop.create_task(self._process_polling_updates(updates, fast))
    #
    #             if relax:
    #                 await asyncio.sleep(relax)
    #     finally:
    #         self._close_waiter._set_result(None)
    #         logger.warning('Polling is stopped.')
    #
    #
    # async def reset_webhook(self, check=True) -> bool:
    #     """
    #     Reset webhook
    #     :param check: check before deleting
    #     :return:
    #     """
    #     if check:
    #         wh = await self.bot.get_webhook_info()
    #         if not wh.url:
    #             return False
    #
    #     return await self.bot.delete_webhook()
    #
    # async def _process_polling_updates(self, updates, fast: typing.Optional[bool] = True):
    #     """
    #     Process updates received from long-polling.
    #     :param updates: list of updates.
    #     :param fast:
    #     """
    #     need_to_call = []
    #     for responses in itertools.chain.from_iterable(await self.process_updates(updates, fast)):
    #         for response in responses:
    #             if not isinstance(response, BaseResponse):
    #                 continue
    #             need_to_call.append(response.execute_response(self.bot))
    #     if need_to_call:
    #         try:
    #             asyncio.gather(*need_to_call)
    #         except TelegramAPIError:
    #             logger.exception('Cause exception while processing updates.')
    #
    #
