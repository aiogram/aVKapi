from . import base
from . import fields
from .base import VKObject


class Photo(VKObject):
    photo_50: base.String = fields.Field()
    photo_100: base.String = fields.Field()
    photo_200: base.String = fields.Field()

