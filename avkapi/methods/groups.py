from . import base
from .base import BaseMethod
import typing
from ..utils.payload import generate_payload


class Groups(BaseMethod):
    async def get_long_poll_server(self, group_id: typing.Union[base.Integer, base.String]):
        if not isinstance(group_id, int):
            try:
                group_id = int(group_id)
            except NameError:
                pass
            except ValueError:
                pass
            except TypeError:
                pass
            except Exception:
                pass

        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="groups.getLongPollServer", parameters=parameters)
        return result.get('response')
