from . import base
from .base import BaseMethod
import typing
from ..types.user import User, NameCase
from ..utils.payload import generate_payload, prepare_arg


class Users(BaseMethod):

    async def get(self, user_ids: typing.List[base.Integer],
                  fields: typing.List[base.String],
                  name_case: base.String = NameCase.NOM) -> typing.List[User]:
        fields = ",".join(fields)

        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="users.get", parameters=parameters)
        return result
