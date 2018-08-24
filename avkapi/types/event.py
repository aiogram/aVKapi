from . import base
from . import fields
from .base import VKObject
from .message import Message


class EventType:
    CONFIRMATION = 'confirmation'

    MESSAGE_NEW = 'message_new'
    MESSAGE_REPLY = 'message_reply'
    MESSAGE_EDIT = 'message_edit'
    MESSAGES = MESSAGE_NEW, MESSAGE_REPLY, MESSAGE_EDIT

    MESSAGE_ALLOW = 'message_allow'
    MESSAGE_DENY = 'message_deny'


class Event(VKObject):
    type: base.String = fields.Field()
    group_id: base.String = fields.Field()
    secret: base.String = fields.Field()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        object_data = kwargs.get('object')
        object_data['content_type'] = self.type

        if self.type in EventType.MESSAGES:
            self.message = Message(**object_data)
