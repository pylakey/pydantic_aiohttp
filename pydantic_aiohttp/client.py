import logging
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
    Union,
)

import aiofiles
import aiohttp
import pydantic
import ujson
from aiohttp.typedefs import PathLike
from ujson import JSONDecodeError

from .errors import (
    HTTPError,
    ResponseParseError,
    errors_classes,
)
from .utils import (
    DEFAULT_DOWNLOAD_CHUNK_SIZE,
    model_to_dict,
    read_file_by_chunk,
)

StrIntMapping = dict[str, Union[str, int]]
HttpEncodableMapping = dict[str, Union[str, int, list[Union[str, int]]]]
Params = Union[HttpEncodableMapping, pydantic.BaseModel]
Cookies = Union[StrIntMapping, pydantic.BaseModel]
Headers = Union[StrIntMapping, pydantic.BaseModel]
Body = Union[dict[str, Any], pydantic.BaseModel]
ErrorResponseModels = dict[int, Type[pydantic.BaseModel]]

Response = TypeVar('Response')


class Client:
    def __init__(
            self,
            base_url: str = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            error_response_models: ErrorResponseModels = None,
            bearer_token: Union[str, pydantic.SecretStr] = None
    ):
        self.logger = logging.getLogger("pydantic_aiohttp.Client")
        headers = model_to_dict(headers) or {}
        cookies = model_to_dict(cookies) or {}

        if bearer_token is not None:
            if isinstance(bearer_token, pydantic.SecretStr):
                bearer_token = bearer_token.get_secret_value()

            headers["Authorization"] = f"Bearer {bearer_token}"

        self._error_response_models = error_response_models or {}
        self._session = aiohttp.ClientSession(
            base_url,
            headers=headers,
            cookies=cookies,
            json_serialize=ujson.dumps
        )

    async def _parse_response_error(
            self,
            response: aiohttp.ClientResponse,
            error_response_models: ErrorResponseModels = None
    ):
        error_response_models = self._error_response_models | (error_response_models or {})
        error_class = errors_classes.get(response.status, HTTPError)
        error_response_model = error_response_models.get(response.status)

        try:
            response_json = await response.json(loads=ujson.loads, content_type=None)
        except JSONDecodeError:
            response_text = await response.text()
            raise ResponseParseError(raw_response=response_text)

        if bool(error_response_model):
            raise error_class(pydantic.parse_obj_as(error_response_model, response_json))

        raise error_class(response_json)

    async def _parse_response_json(
            self,
            response: aiohttp.ClientResponse,
            response_model: Type[Response] = None,
    ):
        try:
            response_json = await response.json(loads=ujson.loads, content_type=None)
        except JSONDecodeError:
            response_text = await response.text()
            raise ResponseParseError(raw_response=response_text)

        if response_model is not None:
            return pydantic.parse_obj_as(response_model, response_json)

        return response_json

    async def download_file(
            self,
            path: str,
            filepath: aiohttp.typedefs.PathLike = None,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None,
            chunk_size: int = DEFAULT_DOWNLOAD_CHUNK_SIZE,
    ):
        async with self._session.request(
                'GET',
                path,
                headers=model_to_dict(headers),
                cookies=model_to_dict(cookies),
                params=model_to_dict(params),
                timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            if response.ok:
                if response.content_type == 'application/json':
                    return await self._parse_response_json(response, response_model=response_model)

                if filepath is None:
                    # TODO: Retrieve original file name from response
                    filepath = path.rsplit("/", maxsplit=1)[-1]

                async with aiofiles.open(filepath, 'wb') as fd:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await fd.write(chunk)

                return

            return await self._parse_response_error(response, error_response_models=error_response_models)

    async def upload_file(
            self,
            path: str,
            file: aiohttp.typedefs.PathLike,
            *,
            form_key: str = 'file',
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None,
    ) -> Optional[Response]:
        return await self.post(
            path,
            headers=headers,
            cookies=cookies,
            params=params,
            # TODO: aiofiles?
            data={form_key: open(file, 'rb')},
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def stream_file(
            self,
            path: str,
            file: aiohttp.typedefs.PathLike,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.post(
            path,
            headers=headers,
            cookies=cookies,
            params=params,
            data=read_file_by_chunk(file),
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def request(
            self,
            method: str,
            path: str,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        async with self._session.request(
                method,
                path,
                headers=model_to_dict(headers),
                cookies=model_to_dict(cookies),
                params=model_to_dict(params),
                json=model_to_dict(body),
                data=data,
                timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            if response.ok:
                return await self._parse_response_json(response, response_model=response_model)

            return await self._parse_response_error(response, error_response_models=error_response_models)

    async def get(
            self,
            path: str,
            *,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.request(
            "GET",
            path,
            headers=headers,
            cookies=cookies,
            params=params,
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def post(
            self,
            path: str,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.request(
            "POST",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def patch(
            self,
            path: str,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.request(
            "PATCH",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def put(
            self,
            path: str,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.request(
            "PUT",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def delete(
            self,
            path: str,
            *,
            body: Body = None,
            data: Any = None,
            headers: Headers = None,
            cookies: Cookies = None,
            params: Params = None,
            response_model: Type[Response] = None,
            timeout: int = 300,  # Default in aiohttp
            error_response_models: ErrorResponseModels = None
    ) -> Optional[Response]:
        return await self.request(
            "DELETE",
            path,
            body=body,
            data=data,
            headers=headers,
            cookies=cookies,
            params=params,
            response_model=response_model,
            timeout=timeout,
            error_response_models=error_response_models,
        )

    async def close(self):
        await self._session.close()
