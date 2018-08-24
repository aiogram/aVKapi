import logging
logger = logging.getLogger(__name__)


class BaseMethod:
    def __init__(self, session, access_token, api_version):
        self._session = session
        self._access_token = access_token
        self._api_version = api_version

    async def _api_request(self, method_name, parameters):
        """

        :param method_name:
        :type method_name: str
        :param parameters:
        :type parameters: dict
        :return:
        """
        parameters['access_token'] = self._access_token
        parameters['v'] = self._api_version
        p = {k: v for k, v in parameters.items() if v is not None}
        link = f'https://api.vk.com/method/{method_name}'

        async with self._session.post(link, params=p) as resp:
            status = resp.status
            text = await resp.text()
            logger.info(f'Response: {status}, {text}')

        return text
