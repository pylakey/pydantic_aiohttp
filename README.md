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


class HelloWorldResponse(pydantic.BaseModel):
    hello: str


async def main():
    example_client = Client("https://api.example.com")

    response = await example_client.get("/hello", response_model=HelloWorldResponse)
    print(response.hello)

    # After all your work is done you should close client (this method closes aiohttp session instance)
    await example_client.close()


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
