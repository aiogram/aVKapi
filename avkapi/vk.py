from __future__ import annotations

import asyncio
import logging
import ssl
import certifi
import contextlib
import aiohttp
import typing
from aiohttp import ClientSession
from aiohttp.helpers import sentinel
from contextvars import ContextVar


from .types import Event, base
from .methods import Messages, Users, Groups
from .utils import json
from .utils.payload import generate_payload
from .utils.mixins import DataMixin, ContextInstanceMixin

logger = logging.getLogger(__name__)

API_URL = 'https://api.vk.com/method/'


class VK(DataMixin, ContextInstanceMixin):
    _ctx_timeout = ContextVar('VKRequestTimeout')

    def __init__(self, confirmation_code=None, secret_key=None, access_token=None, loop=None):
        """
        :type confirmation_code: str
        """
        self.confirmation_code = confirmation_code
        self.secret_key = secret_key
        self.access_token = access_token
        self.api_version = '5.95'

        # asyncio loop instance
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl_context=ssl_context, loop=self.loop)
        self._session = ClientSession(loop=self.loop, json_serialize=json.dumps, connector=connector)

        # methods
        _data = {'access_token': access_token, 'session': self._session, 'api_version': self.api_version}
        self.messages = Messages(**_data)
        self.users = Users(**_data)
        self.groups = Groups(**_data)

    async def get_session(self):
        if not self._session:
            self._session = ClientSession()

    async def api_request(self, method_name, parameters):
        params = {
            'access_token': self.access_token,
            'v': self.api_version
        }
        parameters.update(**params)
        link = f'{API_URL}{method_name}?{parameters}'

        async with self._session.post(link) as resp:
            status = resp.status
            text = await resp.text()
            logger.info(f'Response: {status}, {text}')

    async def act_a_check(self, key, server, ts, wait=25):

        parameters = generate_payload(**locals())
        parameters['act'] = 'a_check'
        async with self._session.post(server, params=parameters) as resp:
            status = resp.status
            result = await resp.json()
            logger.info(f'Response: {status}, {result}')

        ts = result.get('ts')
        updates = result.get('updates')

        return ts, [Event(**data) for data in updates]

    async def close(self):
        if isinstance(self._session, ClientSession) and not self._session.closed:
            await self._session.close()

    @staticmethod
    def _prepare_timeout(
            value: typing.Optional[typing.Union[base.Integer, base.Float, aiohttp.ClientTimeout]]
    ) -> typing.Optional[aiohttp.ClientTimeout]:
        if value is None or isinstance(value, aiohttp.ClientTimeout):
            return value
        return aiohttp.ClientTimeout(total=value)

    @property
    def timeout(self):
        timeout = self._ctx_timeout.get(self._timeout)
        if timeout is None:
            return sentinel
        return timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = self._prepare_timeout(value)

    @timeout.deleter
    def timeout(self):
        self.timeout = None

    @contextlib.contextmanager
    def request_timeout(self, timeout: typing.Union[base.Integer, base.Float, aiohttp.ClientTimeout]):
        """
        Context manager implements opportunity to change request timeout in current context

        :param timeout: Request timeout
        :type timeout: :obj:`typing.Optional[typing.Union[base.Integer, base.Float, aiohttp.ClientTimeout]]`
        :return:
        """
        timeout = self._prepare_timeout(timeout)
        token = self._ctx_timeout.set(timeout)
        try:
            yield
        finally:
            self._ctx_timeout.reset(token)

