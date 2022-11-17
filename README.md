# pydantic_aiohttp - Symbiosis of [Pydantic](https://github.com/samuelcolvin/pydantic) and [Aiohttp](https://github.com/aio-libs/aiohttp)

[![PyPI version shields.io](https://img.shields.io/pypi/v/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)
[![PyPI license](https://img.shields.io/pypi/l/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)

This repository provides simple HTTP Client based on aiohttp with integration of pydantic

## Examples

### Basic example

```python
import asyncio

import pydantic

from pydantic_aiohttp import Client
from pydantic_aiohttp.responses import (
    JSONResponseClass,
    PlainTextResponseClass,
    PydanticModelResponseClass
)


class Todo(pydantic.BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


async def main():
    client = Client('https://jsonplaceholder.typicode.com')

    async with client:
        # Text response
        todo = await client.get('/todos/1', response_class=PlainTextResponseClass)
        print(isinstance(todo, str))  # True

        # JSON Response
        todo = await client.get('/todos/1', response_class=JSONResponseClass)
        print(isinstance(todo, dict))  # True
        # You can achieve the same result if you know exact shape of response, dict for example
        todo = await client.get('/todos/1', response_class=PydanticModelResponseClass, response_model=dict)
        print(isinstance(todo, dict))  # True

        # Deserialization in pydantic model
        todo = await client.get('/todos/1', response_class=PydanticModelResponseClass, response_model=Todo)
        print(isinstance(todo, Todo))  # True

        # PydanticModelResponseClass is used by default, so you can omit it
        todo = await client.get('/todos/1', response_model=Todo)
        print(isinstance(todo, Todo))  # True


if __name__ == '__main__':
    asyncio.run(main())


```

### Explicitly close connection

```python
import asyncio

import pydantic

from pydantic_aiohttp import Client

class Todo(pydantic.BaseModel):
    userId: int
    id: int
    title: str
    completed: bool


async def main():
    client = Client('https://jsonplaceholder.typicode.com')

    try:
        await client.get('/todos/1', response_model=Todo)
    finally:
        # Don't forget to close client session after use
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())

```

### Downloading files

```python
import asyncio
import uuid

from pydantic_aiohttp import Client


async def main():
    client = Client('https://source.unsplash.com')

    async with client:
        filepath = await client.download_file("/random", filepath=f"random_{uuid.uuid4()}.jpg")
        print(filepath)


if __name__ == '__main__':
    asyncio.run(main())

```

### Handling errors parsed as pydantic models

```python
import http
import asyncio

import pydantic

import pydantic_aiohttp
from pydantic_aiohttp import Client


class FastAPIValidationError(pydantic.BaseModel):
    loc: list[str]
    msg: str
    type: str


class FastAPIUnprocessableEntityError(pydantic.BaseModel):
    detail: list[FastAPIValidationError]


class User(pydantic.BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    is_admin: bool


async def main():
    client = Client(
        "https://fastapi.example.com",
        error_response_models={
            http.HTTPStatus.UNPROCESSABLE_ENTITY: FastAPIUnprocessableEntityError
        }
    )

    try:
        # Imagine, that "email" field is required for this route
        await client.post(
            "/users",
            body={
                "first_name": "John",
                "last_name": "Doe"
            },
            response_model=User
        )
    except pydantic_aiohttp.HTTPUnprocessableEntity as e:
        # response field of exception now contain parsed pydantic model entity 
        print(e.response.detail[0].json(indent=4))
        # >>>
        # {
        #     "loc": [
        #         "body",
        #         "email"
        #     ],
        #     "msg": "field required",
        #     "type": "value_error.missing"
        # }
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())

```

## LICENSE

This project is licensed under the terms of the [MIT](https://github.com/pylakey/aiotdlib/blob/master/LICENSE) license.
