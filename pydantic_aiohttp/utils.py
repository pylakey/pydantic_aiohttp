from os import PathLike
from typing import Optional
from typing import Union

import aiofiles
import pydantic
import ujson

from .encoders import IncEx
from .encoders import jsonable_encoder

DEFAULT_DOWNLOAD_CHUNK_SIZE = 64 * 1024  # 128KB
DEFAULT_UPLOAD_CHUNK_SIZE = 64 * 1024  # 64KB


async def read_file_by_chunk(file: Union[str, PathLike[str]], chunk_size: int = DEFAULT_UPLOAD_CHUNK_SIZE):
    async with aiofiles.open(file, 'rb') as f:
        chunk = await f.read(chunk_size)

        while chunk:
            yield chunk
            chunk = await f.read(chunk_size)


def model_to_dict(
        model: Union[dict, pydantic.BaseModel],
        *,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = False,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
) -> Optional[dict]:
    return jsonable_encoder(
        model,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
    )


def json_serialize(o, *args, **kwargs):
    return ujson.dumps(jsonable_encoder(o), *args, **kwargs)
