from typing import Any
from typing import Type
from typing import TypeVar
from typing import Union

import pydantic

StrIntMapping = dict[str, Union[str, int]]
HttpEncodableMapping = dict[str, Union[str, int, list[Union[str, int]]]]
Params = Union[HttpEncodableMapping, pydantic.BaseModel]
Cookies = Union[StrIntMapping, pydantic.BaseModel]
Headers = Union[StrIntMapping, pydantic.BaseModel]
Body = Union[dict[str, Any], pydantic.BaseModel]
ErrorResponseModels = dict[int, Type[pydantic.BaseModel]]

ResponseType = TypeVar('ResponseType')


class EmptyResponse(pydantic.BaseModel):
    pass
