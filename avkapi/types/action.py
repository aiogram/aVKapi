from . import base
from . import fields
from .base import VKObject
from .photo import Photo


class Action(VKObject):
    type: base.String = fields.Field()
    member_id: base.Integer = fields.Field()
    text: base.String = fields.Field()
    email: base.String = fields.Field()
    photo: Photo = fields.Field(base=Photo)


class ActionType:
    CHAT_PHOTO_UPDATE = 'chat_photo_update'
    CHAT_PHOTO_REMOVE = 'chat_photo_remove'
    CHAT_CREATE = 'chat_create'
    CHAT_TITLE_UPDATE = 'chat_title_update'
    CHAT_INVITE_USER = 'chat_invite_user'
    CHAT_KICK_USER = 'chat_kick_user'
    CHAT_PIN_MESSAGE = 'chat_pin_message'
    CHAT_UNPIN_MESSAGE = 'chat_unpin_message'
    CHAT_INVITE_USER_BY_LINK = 'chat_invite_user_by_link'
