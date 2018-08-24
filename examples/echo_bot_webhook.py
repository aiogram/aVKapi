import asyncio

import config
from avkapi import VK
from avkapi import types
from avkapi.dispatcher import Dispatcher

loop = asyncio.get_event_loop()
vk = VK(confirmation_code=config.VK_CONFIRMATION_CODE,
        secret_key=config.VK_CALLBACK_SECRET_KEY,
        access_token=config.VK_ACCESS_TOKEN,
        loop=loop)
dp = Dispatcher(vk, loop=loop)


@dp.message_handler(content_types=types.MessageType.MESSAGE_NEW)
async def echo_handler(message: types.Message):
    peer_id = message.peer_id
    text = message.text
    await vk.messages.send(message=text, peer_id=peer_id)


async def shutdown(_):
    await vk.close()
    await asyncio.sleep(0.250)


if __name__ == '__main__':
    from avkapi.utils.executor import start_webhook

    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT,
                  on_shutdown=shutdown)
