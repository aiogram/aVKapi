import asyncio
import asyncio.tasks
import ipaddress
import logging

from aiohttp import web
from aiohttp.web_exceptions import HTTPGone

from avkapi.types.event import EventType, Event
from avkapi.utils import context

logger = logging.getLogger(__name__)

DEFAULT_WEB_PATH = '/webhook'
VK_DISPATCHER_KEY = 'VK_DISPATCHER'

RESPONSE_TIMEOUT = 55

WEBHOOK = 'webhook'
WEBHOOK_CONNECTION = 'WEBHOOK_CONNECTION'
WEBHOOK_REQUEST = 'WEBHOOK_REQUEST'

# IP filter
VK_IP_LOWER = ipaddress.IPv4Address('149.154.167.197')
VK_IP_UPPER = ipaddress.IPv4Address('149.154.167.233')
allowed_ips = set()


def _check_ip(ip: str) -> bool:
    """ Check IP in range. """
    # address = ipaddress.IPv4Address(ip)
    # return address in allowed_ips
    # todo add vk ip
    return True


def allow_ip(*ips: str):
    """ Allow ip address. """
    allowed_ips.update(ipaddress.IPv4Address(ip) for ip in ips)


# Allow access from VK servers
allow_ip(*(ip for ip in range(int(VK_IP_LOWER), int(VK_IP_UPPER) + 1)))


class WebhookRequestHandler(web.View):
    """
    Simple Webhook request handler for aiohttp web server.

    You need to register that in app:

    .. code-block:: python3

        app.router.add_route('*', '/your/webhook/path', WebhookRequestHadler, name='webhook_handler')

    But first you need to configure application for getting Dispatcher instance from request handler!
    It must always be with key 'VK_DISPATCHER'

    .. code-block:: python3

        vk = VK(TOKEN, loop)
        dp = Dispatcher(vk)
        app['VK_DISPATCHER'] = dp

    """

    def get_dispatcher(self):
        """
        Get Dispatcher instance from environment

        :return: :class:`avkapi.Dispatcher`
        """
        dp = self.request.app[VK_DISPATCHER_KEY]
        try:
            context.set_value('dispatcher', dp)
            context.set_value('vk', dp.vk)
        except RuntimeError:
            pass
        return dp

    async def parse_event(self, vk):
        """
        Read update from stream and deserialize it.

        :param vk: VK instance. You an get it from Dispatcher
        :return: :class:`avkapi.types.Update`
        """
        data = await self.request.json()
        logger.debug(f'Received request: {self.request} {data}')

        # check secret
        result = await self.check_secret_key(vk, data)
        if not result:
            raise web.HTTPForbidden(reason='Error: wrong callback secret')

        # check server confirmation
        event_type = data.get('type')
        if event_type and event_type == EventType.CONFIRMATION:
            return web.Response(text=vk.confirmation_code)

        event = Event(**data)
        logger.debug(f'New event: {event}')
        return event

    @staticmethod
    async def check_secret_key(vk, data):
        secret_key = data.get('secret')
        if secret_key and secret_key == vk.secret_key:
            return True
        return False

    @staticmethod
    async def confirm_server(vk):
        return web.Response(text=vk.confirmation_code)

    async def post(self):
        """ Process POST request """
        self.validate_ip()

        context.update_state({'CALLER': WEBHOOK,
                              WEBHOOK_CONNECTION: True,
                              WEBHOOK_REQUEST: self.request})

        dispatcher = self.get_dispatcher()
        event = await self.parse_event(dispatcher.vk)

        asyncio.ensure_future(dispatcher.process_event(event))
        return web.Response(text='ok')

    async def get(self):
        self.validate_ip()
        return web.Response(text='')

    async def head(self):
        self.validate_ip()
        return web.Response(text='')

    def check_ip(self):
        """
        Check client IP. Accept requests only from VK servers.

        :return:
        """
        # For reverse proxy (nginx)
        forwarded_for = self.request.headers.get('X-Forwarded-For', None)
        if forwarded_for:
            return forwarded_for, _check_ip(forwarded_for)

        # For default method
        peer_name = self.request.transport.get_extra_info('peername')
        if peer_name is not None:
            host, _ = peer_name
            return host, _check_ip(host)

        # Not allowed and can't get client IP
        return None, False

    def validate_ip(self):
        """
        Check ip if that is needed. Raise web.HTTPUnauthorized for not allowed hosts.
        """
        if self.request.app.get('_check_ip', False):
            ip_address, accept = self.check_ip()
            if not accept:
                raise web.HTTPUnauthorized()
            context.set_value('VK_IP', ip_address)


class GoneRequestHandler(web.View):
    """
    If a webhook returns the HTTP error 410 Gone for all requests for more than 23 hours successively,
    it can be automatically removed.
    """

    async def get(self):
        raise HTTPGone()

    async def post(self):
        raise HTTPGone()


def get_new_configured_app(dispatcher, path=DEFAULT_WEB_PATH):
    """
    Create new :class:`aiohttp.web.Application` and configure it.

    :param dispatcher: Dispatcher instance
    :param path: Path to your webhook.
    :return:
    """
    app = web.Application()
    configure_app(dispatcher, app, path)
    return app


def configure_app(dispatcher, app: web.Application, path=DEFAULT_WEB_PATH):
    """
    You can prepare web.Application for working with webhook handler.

    :param dispatcher: Dispatcher instance
    :param app: :class:`aiohttp.web.Application`
    :param path: Path to your webhook.
    :return:
    """
    app.router.add_route('*', path, WebhookRequestHandler, name='webhook_handler')
    app[VK_DISPATCHER_KEY] = dispatcher
