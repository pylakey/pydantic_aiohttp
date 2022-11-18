import abc
import logging
from typing import (
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
)

import aiofiles
import aiohttp.web_response
import pydantic
import ujson
from aiohttp.typedefs import PathLike

from pydantic_aiohttp.utils import DEFAULT_DOWNLOAD_CHUNK_SIZE

ResponseContentType = TypeVar('ResponseContentType')
PydanticModel = TypeVar('PydanticModel')


class ResponseClass(abc.ABC, Generic[ResponseContentType]):
    charset: str = "utf-8"
    aiohttp_response: aiohttp.ClientResponse

    def __init__(self, aiohttp_response: aiohttp.ClientResponse):
        self.aiohttp_response = aiohttp_response
        self.logger = logging.getLogger(self.__class__.__name__)

    async def parse(self, *args, **kwargs) -> Optional[ResponseContentType]:
        return self.aiohttp_response.content


class NoneResponseClass(ResponseClass[None]):
    async def parse(self) -> None:
        return None


class PlainTextResponseClass(ResponseClass[str]):
    async def parse(self, *args, **kwargs) -> str:
        return await self.aiohttp_response.text(self.charset)


class JSONResponseClass(ResponseClass[Union[dict, list, str, None]]):
    async def parse(self, *args, **kwargs) -> Optional[ResponseContentType]:
        return await self.aiohttp_response.json(
            encoding=self.charset,
            loads=ujson.loads,
            content_type=None
        )


class PydanticModelResponseClass(ResponseClass[PydanticModel]):
    async def parse(self, *args, response_model: Type[PydanticModel], **kwargs) -> PydanticModel:
        if response_model is None:
            raise ValueError('response_model could not be None. If you need bare dict use JSONResponseClass instead')

        response_json = await self.aiohttp_response.json(
            encoding=self.charset,
            loads=ujson.loads,
            content_type=None
        )

        return pydantic.parse_obj_as(response_model, response_json)


class StreamResponseClass(ResponseClass[PathLike]):
    async def parse(
            self,
            *args,
            filepath: PathLike,
            chunk_size: int = DEFAULT_DOWNLOAD_CHUNK_SIZE,
            **kwargs
    ) -> PathLike:
        async with aiofiles.open(filepath, 'wb') as fd:
            async for chunk in self.aiohttp_response.content.iter_chunked(chunk_size):
                await fd.write(chunk)

        return filepath
