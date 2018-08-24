import datetime
import typing

from . import base
from . import fields
from .action import Action
from .attachment import Attachment
from .geo import Geo


class MessageType:
    MESSAGE_NEW = ['message_new']
    MESSAGE_REPLY = ['message_reply']
    MESSAGE_EDIT = ['message_edit']

    ANY = ['any']


class Message(base.VKObject):
    """
    This object represents a message.

    https://vk.com/dev/objects/message
    """
    message_id: base.Integer = fields.Field(alias='id')
    date: datetime.datetime = fields.DateTimeField()
    peer_id: base.Integer = fields.Field()
    from_id: base.Integer = fields.Field()
    text: base.String = fields.Field()
    random_id: base.Integer = fields.Field()
    attachments: typing.List[Attachment] = fields.ListField(base=Attachment)
    important: base.Boolean = fields.Field()
    geo: Geo = fields.Field(base=Geo)
    payload: base.String = fields.Field()
    fwd_messages: typing.List['Message'] = fields.ListField(base='Message')
    action: Action = fields.Field(base=Action)
    content_type = fields.Field()

    def __int__(self):
        return self.message_id

