from .base import BaseMethod


class Messages(BaseMethod):

    async def send(self, user_id=None, random_id=None, peer_id=None, domain=None, chat_id=None, user_ids=None,
                   message=None, lat=None, long=None, attachment=None, forward_messages=None, sticker_id=None,
                   group_id=None, keyboard=None, payload=None):

        params = {
            'user_id': user_id,
            'random_id': random_id,
            'peer_id': peer_id,
            'domain': domain,
            'chat_id': chat_id,
            'user_ids': user_ids,
            'message': message,
            'lat': lat,
            'long': long,
            'attachment': attachment,
            'forward_messages': forward_messages,
            'sticker_id': sticker_id,
            'group_id': group_id,
            'keyboard': keyboard,
            'payload': payload,
        }

        result = await self._api_request(method_name='messages.send', parameters=params)
        return result
