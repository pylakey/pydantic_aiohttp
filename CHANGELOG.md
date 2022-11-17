# CHANGELOG

## 0.4.0

### Update

Client response parsing customization

## 0.3.2

### Update

* Client now can be used as context manager:

```python
async with Client("https://api.example.com") as client:
    response = await client.get("/hello")
```

## 0.3.1

### Update

* Fixed null pointer when bearer_token passed to Client

* Bump JRubics/poetry-publish from 1.11 to 1.12 by @dependabot in #6

## 0.3.0

### Update

* base_url parameter of Client is optional now

* Added Client.download_file method for downloading files

* Renamed misleading filename parameter to form_key in Client.upload_file

## 0.2.1

### Update

Allow to set custom filename in `Client.upload_file`

## 0.2.0

### Breaking

Removed `status` module. Native Python `http.HTTPStatus` is used instead (#1)

### Update

Some code cleanups

## 0.1.1

Unset fields now excluded by default from pydantic models passed to `Client`

## 0.1.0 - First public release
