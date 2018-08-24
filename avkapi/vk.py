import asyncio
import logging

from aiohttp import ClientSession

from .methods import Messages
from .utils import json

logger = logging.getLogger(__name__)

API_URL = 'https://api.vk.com/method/'


class VK:
    def __init__(self, confirmation_code=None, secret_key=None, access_token=None, loop=None):
        """
        :type confirmation_code: str
        """
        self.confirmation_code = confirmation_code
        self.secret_key = secret_key
        self.access_token = access_token
        self.api_version = '5.80'

        # asyncio loop instance
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        self._session = ClientSession(loop=self.loop, json_serialize=json.dumps)
        self.messages = Messages(access_token=access_token, session=self._session, api_version=self.api_version)

    async def get_session(self):
        if not self._session:
            self._session = ClientSession()

    async def api_request(self, method_name, parameters):
        link = f'{API_URL}{method_name}?{parameters}'
        params = {
            'access_token': self.access_token,
            'v': self.api_version
        }
        params.update(**parameters)
        async with self._session.post(link) as resp:
            status = resp.status
            text = await resp.text()
            logger.info(f'Response: {status}, {text}')

    async def close(self):
        if isinstance(self._session, ClientSession) and not self._session.closed:
            await self._session.close()
