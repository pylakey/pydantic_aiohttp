# CHANGELOG

## 0.7.0

### **BREAKING**

* All types moved from `client` to separate `types` module

* Removed unused `error_response_class` from `Client` constructur parameters

___

* Added custom `url_compatible_encoder` for params, cookies and headers because Aiohttp expects their values to be `int`, `float` or `str` instances

## 0.6.2

* `model_to_dict` now accepts all `pydantic.BaseModel.dict` parameters

* `utils` module added to package export

* `encoders` module added to package export

* All absolute package path exports replaced with relative

## 0.6.1

* Upgraded dependencies

## 0.6.0

* Using custom json requests serializer for better pydantic model serialization

> Code of such json encoder was taken from https://github.com/tiangolo/fastapi. Thanks to @tiangolo for implementing it

## 0.5.1

* Hotfixes

## 0.5.0

* Removed `content_type` attribute in ResponseClass

* Ignore content type in `response.json()` when parsing response

## 0.4.1

* Common params between all requests

## 0.4.0

* Client response parsing customization

## 0.3.2

* Client now can be used as context manager:

```python
async with Client("https://api.example.com") as client:
    response = await client.get("/hello")
```

## 0.3.1

* Fixed null pointer when bearer_token passed to Client

* Bump JRubics/poetry-publish from 1.11 to 1.12 by @dependabot in #6

## 0.3.0

* base_url parameter of Client is optional now

* Added Client.download_file method for downloading files

* Renamed misleading filename parameter to form_key in Client.upload_file

## 0.2.1

Allow to set custom filename in `Client.upload_file`

## 0.2.0

### Breaking

Removed `status` module. Native Python `http.HTTPStatus` is used instead (#1)

Some code cleanups

## 0.1.1

Unset fields now excluded by default from pydantic models passed to `Client`

## 0.1.0 - First public release
