from os import PathLike
from typing import (
    Optional,
    Union,
)

import aiofiles
import pydantic
import ujson

from pydantic_aiohttp.encoders import jsonable_encoder

DEFAULT_DOWNLOAD_CHUNK_SIZE = 64 * 1024  # 128KB
DEFAULT_UPLOAD_CHUNK_SIZE = 64 * 1024  # 64KB


async def read_file_by_chunk(file: Union[str, PathLike[str]], chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE):
    async with aiofiles.open(file, 'rb') as f:
        chunk = await f.read(chunk_size)

        while chunk:
            yield chunk
            chunk = await f.read(chunk_size)


def model_to_dict(model: Union[dict, pydantic.BaseModel]) -> Optional[dict]:
    if isinstance(model, pydantic.BaseModel):
        return model.dict(exclude_unset=True)

    if isinstance(model, dict):
        return model

    return None


def json_serialize(o, *args, **kwargs):
    return ujson.dumps(jsonable_encoder(o), *args, **kwargs)
