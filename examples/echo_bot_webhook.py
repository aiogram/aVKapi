"""
Basic webhook example.

Caution: don't store credentials and settings in your git. Use env variables or config file
We set it here to simplify the example.

Recommended to use nginx as external web server and then proxy requests to your python application.

"""
import asyncio

from avkapi import VK
from avkapi import types
from avkapi.dispatcher import Dispatcher
from avkapi.utils.executor import start_webhook

# Set your VK credentials.
VK_CONFIRMATION_CODE = '12345678'
VK_CALLBACK_SECRET_KEY = 'secret_key'
VK_ACCESS_TOKEN = '2e37d9dd8f06e2ccf8dae5'

# Set your webapp setting
WEBHOOK_PATH = '/'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 3100

# Create vk instance
# You can use it for simple calling VK API methods
vk = VK(confirmation_code=VK_CONFIRMATION_CODE,
        secret_key=VK_CALLBACK_SECRET_KEY,
        access_token=VK_ACCESS_TOKEN)

# Create dispatcher instance
# You need to use a dispatcher for handling incoming messages from your users
dp = Dispatcher(vk)


@dp.message_handler(content_types=types.MessageType.MESSAGE_NEW)
async def echo_handler(message: types.Message):
    """ Handler catches all incoming messages and sends back the same. """
    # calling message.send method
    await vk.messages.send(message=message.text, peer_id=message.peer_id)


async def shutdown(_: Dispatcher):
    """ Graceful application shutdown. """
    await vk.close()
    await asyncio.sleep(0.250)  # to gracefully shutdown aiohttp server


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH,
                  host=WEBAPP_HOST, port=WEBAPP_PORT,
                  on_shutdown=shutdown)
