from . import base
from . import fields
from .base import VKObject
import typing
import datetime


class Coordinates(VKObject):
    latitude: base.Float = fields.Field()
    longitude: base.Float = fields.Field()


class Place(VKObject):
    place_id: base.Integer = fields.Field(alias='id')
    title: base.String = fields.Field()
    latitude: base.Float = fields.Field()
    longitude: base.Float = fields.Field()
    created: datetime.datetime = fields.DateTimeField()
    icon: base.String = fields.Field()
    country: base.String = fields.Field()
    city: base.String = fields.Field()


class Geo(VKObject):
    type: base.String = fields.Field()
    coordinates: typing.List[Coordinates] = fields.ListField(base=Coordinates)
    place: Place = fields.Field(base=Place)





