"""
Basic group long polling example.

Caution: don't store credentials and settings in your git. Use env variables or config file
We set it here to simplify the example.


"""
from avkapi import VK
from avkapi import types
from avkapi.dispatcher import Dispatcher
from avkapi.utils.executor import start_polling

# Set your VK credentials.
VK_ACCESS_TOKEN = '2e37d9dd8f06e2ccf8dae5'
VK_GROUP_ID = 123456


# Create vk instance
# You can use it for simple calling VK API methods
vk = VK(access_token=VK_ACCESS_TOKEN)

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


if __name__ == '__main__':
    start_polling(dp, group_id=VK_GROUP_ID, on_shutdown=shutdown)

