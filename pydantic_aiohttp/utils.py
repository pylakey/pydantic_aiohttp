from os import PathLike
from typing import Union

import aiofiles

DEFAULT_CHUNK_SIZE = 64 * 1024


async def read_file_by_chunk(file: Union[str, PathLike[str]], chunk_size: int = DEFAULT_CHUNK_SIZE):
    async with aiofiles.open(file, 'rb') as f:
        chunk = await f.read(chunk_size)

        while chunk:
            yield chunk
            chunk = await f.read(chunk_size)
