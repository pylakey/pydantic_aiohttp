from typing import (
    Union,
)

import pydantic

from .status import *

Response = Union[str, bytes, dict, list, pydantic.BaseModel]
RawResponse = Union[str, bytes]


class ClientError(Exception):
    pass


class ResponseParseError(ClientError):
    def __init__(self, raw_response: RawResponse):
        self.raw_response = raw_response


class HTTPError(Exception):
    status_code: int = None
    response: Response = None

    def __init__(self, response: Response):
        self.response = response


class HTTPRedirect(HTTPError):
    pass


class HTTPClientError(HTTPError):
    pass


class HTTPServerError(HTTPError):
    pass


# 300
class HTTPMultipleChoices(HTTPRedirect):
    status_code = HTTP_300_MULTIPLE_CHOICES


class HTTPMovedPermanently(HTTPRedirect):
    status_code = HTTP_301_MOVED_PERMANENTLY


class HTTPFound(HTTPRedirect):
    status_code = HTTP_302_FOUND


class HTTPSeeOther(HTTPRedirect):
    status_code = HTTP_303_SEE_OTHER


class HTTPNotModified(HTTPRedirect):
    status_code = HTTP_304_NOT_MODIFIED


class HTTPUseProxy(HTTPRedirect):
    status_code = HTTP_305_USE_PROXY


class HTTPReserved(HTTPRedirect):
    status_code = HTTP_306_RESERVED


class HTTPTemporaryRedirect(HTTPRedirect):
    status_code = HTTP_307_TEMPORARY_REDIRECT


class HTTPPermanentRedirect(HTTPRedirect):
    status_code = HTTP_308_PERMANENT_REDIRECT


# 400
class HTTPBadRequest(HTTPClientError):
    status_code = HTTP_400_BAD_REQUEST


class HTTPUnauthorized(HTTPClientError):
    status_code = HTTP_401_UNAUTHORIZED


class HTTPPaymentRequired(HTTPClientError):
    status_code = HTTP_402_PAYMENT_REQUIRED


class HTTPForbidden(HTTPClientError):
    status_code = HTTP_403_FORBIDDEN


class HTTPNotFound(HTTPClientError):
    status_code = HTTP_404_NOT_FOUND


class HTTPMethodNotAllowed(HTTPClientError):
    status_code = HTTP_405_METHOD_NOT_ALLOWED


class HTTPNotAcceptable(HTTPClientError):
    status_code = HTTP_406_NOT_ACCEPTABLE


class HTTPProxyAuthenticationRequired(HTTPClientError):
    status_code = HTTP_407_PROXY_AUTHENTICATION_REQUIRED


class HTTPRequestTimeout(HTTPClientError):
    status_code = HTTP_408_REQUEST_TIMEOUT


class HTTPConflict(HTTPClientError):
    status_code = HTTP_409_CONFLICT


class HTTPGone(HTTPClientError):
    status_code = HTTP_410_GONE


class HTTPLengthRequired(HTTPClientError):
    status_code = HTTP_411_LENGTH_REQUIRED


class HTTPPreconditionFailed(HTTPClientError):
    status_code = HTTP_412_PRECONDITION_FAILED


class HTTPRequestEntityTooLarge(HTTPClientError):
    status_code = HTTP_413_REQUEST_ENTITY_TOO_LARGE


class HTTPRequestUriTooLong(HTTPClientError):
    status_code = HTTP_414_REQUEST_URI_TOO_LONG


class HTTPUnsupportedMediaType(HTTPClientError):
    status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class HTTPRequestedRangeNotSatisfiable(HTTPClientError):
    status_code = HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE


class HTTPExpectationFailed(HTTPClientError):
    status_code = HTTP_417_EXPECTATION_FAILED


class HTTPImATeapot(HTTPClientError):
    status_code = HTTP_418_IM_A_TEAPOT


class HTTPMisdirectedRequest(HTTPClientError):
    status_code = HTTP_421_MISDIRECTED_REQUEST


class HTTPUnprocessableEntity(HTTPClientError):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY


class HTTPLocked(HTTPClientError):
    status_code = HTTP_423_LOCKED


class HTTPFailedDependency(HTTPClientError):
    status_code = HTTP_424_FAILED_DEPENDENCY


class HTTPTooEarly(HTTPClientError):
    status_code = HTTP_425_TOO_EARLY


class HTTPUpgradeRequired(HTTPClientError):
    status_code = HTTP_426_UPGRADE_REQUIRED


class HTTPPreconditionRequired(HTTPClientError):
    status_code = HTTP_428_PRECONDITION_REQUIRED


class HTTPTooManyRequests(HTTPClientError):
    status_code = HTTP_429_TOO_MANY_REQUESTS


class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    status_code = HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE


class HTTPUnavailableForLegalReasons(HTTPClientError):
    status_code = HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS


# 500
class HTTPInternalServerError(HTTPServerError):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR


class HTTPNotImplemented(HTTPServerError):
    status_code = HTTP_501_NOT_IMPLEMENTED


class HTTPBadGateway(HTTPServerError):
    status_code = HTTP_502_BAD_GATEWAY


class HTTPServiceUnavailable(HTTPServerError):
    status_code = HTTP_503_SERVICE_UNAVAILABLE


class HTTPGatewayTimeout(HTTPServerError):
    status_code = HTTP_504_GATEWAY_TIMEOUT


class HTTPHttpServerVersionNotSupported(HTTPServerError):
    status_code = HTTP_505_HTTP_VERSION_NOT_SUPPORTED


class HTTPVariantAlsoNegotiates(HTTPServerError):
    status_code = HTTP_506_VARIANT_ALSO_NEGOTIATES


class HTTPInsufficientStorage(HTTPServerError):
    status_code = HTTP_507_INSUFFICIENT_STORAGE


class HTTPLoopDetected(HTTPServerError):
    status_code = HTTP_508_LOOP_DETECTED


class HTTPNotExtended(HTTPServerError):
    status_code = HTTP_510_NOT_EXTENDED


class HTTPNetworkAuthenticationRequired(HTTPServerError):
    status_code = HTTP_511_NETWORK_AUTHENTICATION_REQUIRED


errors_classes = {
    # 300
    HTTP_300_MULTIPLE_CHOICES: HTTPMultipleChoices,
    HTTP_301_MOVED_PERMANENTLY: HTTPMovedPermanently,
    HTTP_302_FOUND: HTTPFound,
    HTTP_303_SEE_OTHER: HTTPSeeOther,
    HTTP_304_NOT_MODIFIED: HTTPNotModified,
    HTTP_305_USE_PROXY: HTTPUseProxy,
    HTTP_306_RESERVED: HTTPReserved,
    HTTP_307_TEMPORARY_REDIRECT: HTTPTemporaryRedirect,
    HTTP_308_PERMANENT_REDIRECT: HTTPPermanentRedirect,
    # 400
    HTTP_400_BAD_REQUEST: HTTPBadRequest,
    HTTP_401_UNAUTHORIZED: HTTPUnauthorized,
    HTTP_402_PAYMENT_REQUIRED: HTTPPaymentRequired,
    HTTP_403_FORBIDDEN: HTTPForbidden,
    HTTP_404_NOT_FOUND: HTTPNotFound,
    HTTP_405_METHOD_NOT_ALLOWED: HTTPMethodNotAllowed,
    HTTP_406_NOT_ACCEPTABLE: HTTPNotAcceptable,
    HTTP_407_PROXY_AUTHENTICATION_REQUIRED: HTTPProxyAuthenticationRequired,
    HTTP_408_REQUEST_TIMEOUT: HTTPRequestTimeout,
    HTTP_409_CONFLICT: HTTPConflict,
    HTTP_410_GONE: HTTPGone,
    HTTP_411_LENGTH_REQUIRED: HTTPLengthRequired,
    HTTP_412_PRECONDITION_FAILED: HTTPPreconditionFailed,
    HTTP_413_REQUEST_ENTITY_TOO_LARGE: HTTPRequestEntityTooLarge,
    HTTP_414_REQUEST_URI_TOO_LONG: HTTPRequestUriTooLong,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE: HTTPUnsupportedMediaType,
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE: HTTPRequestedRangeNotSatisfiable,
    HTTP_417_EXPECTATION_FAILED: HTTPExpectationFailed,
    HTTP_418_IM_A_TEAPOT: HTTPImATeapot,
    HTTP_421_MISDIRECTED_REQUEST: HTTPMisdirectedRequest,
    HTTP_422_UNPROCESSABLE_ENTITY: HTTPUnprocessableEntity,
    HTTP_423_LOCKED: HTTPLocked,
    HTTP_424_FAILED_DEPENDENCY: HTTPFailedDependency,
    HTTP_425_TOO_EARLY: HTTPTooEarly,
    HTTP_426_UPGRADE_REQUIRED: HTTPUpgradeRequired,
    HTTP_428_PRECONDITION_REQUIRED: HTTPPreconditionRequired,
    HTTP_429_TOO_MANY_REQUESTS: HTTPTooManyRequests,
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE: HTTPRequestHeaderFieldsTooLarge,
    HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS: HTTPUnavailableForLegalReasons,
    # 500
    HTTP_500_INTERNAL_SERVER_ERROR: HTTPInternalServerError,
    HTTP_501_NOT_IMPLEMENTED: HTTPNotImplemented,
    HTTP_502_BAD_GATEWAY: HTTPBadGateway,
    HTTP_503_SERVICE_UNAVAILABLE: HTTPServiceUnavailable,
    HTTP_504_GATEWAY_TIMEOUT: HTTPGatewayTimeout,
    HTTP_505_HTTP_VERSION_NOT_SUPPORTED: HTTPHttpServerVersionNotSupported,
    HTTP_506_VARIANT_ALSO_NEGOTIATES: HTTPVariantAlsoNegotiates,
    HTTP_507_INSUFFICIENT_STORAGE: HTTPInsufficientStorage,
    HTTP_508_LOOP_DETECTED: HTTPLoopDetected,
    HTTP_510_NOT_EXTENDED: HTTPNotExtended,
    HTTP_511_NETWORK_AUTHENTICATION_REQUIRED: HTTPNetworkAuthenticationRequired,
}
