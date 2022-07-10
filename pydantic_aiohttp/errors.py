import http
from typing import Union

import pydantic

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
    status_code = http.HTTPStatus.MULTIPLE_CHOICES


class HTTPMovedPermanently(HTTPRedirect):
    status_code = http.HTTPStatus.MOVED_PERMANENTLY


class HTTPFound(HTTPRedirect):
    status_code = http.HTTPStatus.FOUND


class HTTPSeeOther(HTTPRedirect):
    status_code = http.HTTPStatus.SEE_OTHER


class HTTPNotModified(HTTPRedirect):
    status_code = http.HTTPStatus.NOT_MODIFIED


class HTTPUseProxy(HTTPRedirect):
    status_code = http.HTTPStatus.USE_PROXY


# class HTTPReserved(HTTPRedirect):
#     status_code = http.HTTPStatus.RESERVED


class HTTPTemporaryRedirect(HTTPRedirect):
    status_code = http.HTTPStatus.TEMPORARY_REDIRECT


class HTTPPermanentRedirect(HTTPRedirect):
    status_code = http.HTTPStatus.PERMANENT_REDIRECT


# 400
class HTTPBadRequest(HTTPClientError):
    status_code = http.HTTPStatus.BAD_REQUEST


class HTTPUnauthorized(HTTPClientError):
    status_code = http.HTTPStatus.UNAUTHORIZED


class HTTPPaymentRequired(HTTPClientError):
    status_code = http.HTTPStatus.PAYMENT_REQUIRED


class HTTPForbidden(HTTPClientError):
    status_code = http.HTTPStatus.FORBIDDEN


class HTTPNotFound(HTTPClientError):
    status_code = http.HTTPStatus.NOT_FOUND


class HTTPMethodNotAllowed(HTTPClientError):
    status_code = http.HTTPStatus.METHOD_NOT_ALLOWED


class HTTPNotAcceptable(HTTPClientError):
    status_code = http.HTTPStatus.NOT_ACCEPTABLE


class HTTPProxyAuthenticationRequired(HTTPClientError):
    status_code = http.HTTPStatus.PROXY_AUTHENTICATION_REQUIRED


class HTTPRequestTimeout(HTTPClientError):
    status_code = http.HTTPStatus.REQUEST_TIMEOUT


class HTTPConflict(HTTPClientError):
    status_code = http.HTTPStatus.CONFLICT


class HTTPGone(HTTPClientError):
    status_code = http.HTTPStatus.GONE


class HTTPLengthRequired(HTTPClientError):
    status_code = http.HTTPStatus.LENGTH_REQUIRED


class HTTPPreconditionFailed(HTTPClientError):
    status_code = http.HTTPStatus.PRECONDITION_FAILED


class HTTPRequestEntityTooLarge(HTTPClientError):
    status_code = http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE


class HTTPRequestUriTooLong(HTTPClientError):
    status_code = http.HTTPStatus.REQUEST_URI_TOO_LONG


class HTTPUnsupportedMediaType(HTTPClientError):
    status_code = http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE


class HTTPRequestedRangeNotSatisfiable(HTTPClientError):
    status_code = http.HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE


class HTTPExpectationFailed(HTTPClientError):
    status_code = http.HTTPStatus.EXPECTATION_FAILED


class HTTPImATeapot(HTTPClientError):
    status_code = http.HTTPStatus.IM_A_TEAPOT


class HTTPMisdirectedRequest(HTTPClientError):
    status_code = http.HTTPStatus.MISDIRECTED_REQUEST


class HTTPUnprocessableEntity(HTTPClientError):
    status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY


class HTTPLocked(HTTPClientError):
    status_code = http.HTTPStatus.LOCKED


class HTTPFailedDependency(HTTPClientError):
    status_code = http.HTTPStatus.FAILED_DEPENDENCY


class HTTPTooEarly(HTTPClientError):
    status_code = http.HTTPStatus.TOO_EARLY


class HTTPUpgradeRequired(HTTPClientError):
    status_code = http.HTTPStatus.UPGRADE_REQUIRED


class HTTPPreconditionRequired(HTTPClientError):
    status_code = http.HTTPStatus.PRECONDITION_REQUIRED


class HTTPTooManyRequests(HTTPClientError):
    status_code = http.HTTPStatus.TOO_MANY_REQUESTS


class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    status_code = http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE


class HTTPUnavailableForLegalReasons(HTTPClientError):
    status_code = http.HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS


# 500
class HTTPInternalServerError(HTTPServerError):
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR


class HTTPNotImplemented(HTTPServerError):
    status_code = http.HTTPStatus.NOT_IMPLEMENTED


class HTTPBadGateway(HTTPServerError):
    status_code = http.HTTPStatus.BAD_GATEWAY


class HTTPServiceUnavailable(HTTPServerError):
    status_code = http.HTTPStatus.SERVICE_UNAVAILABLE


class HTTPGatewayTimeout(HTTPServerError):
    status_code = http.HTTPStatus.GATEWAY_TIMEOUT


class HTTPHttpServerVersionNotSupported(HTTPServerError):
    status_code = http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED


class HTTPVariantAlsoNegotiates(HTTPServerError):
    status_code = http.HTTPStatus.VARIANT_ALSO_NEGOTIATES


class HTTPInsufficientStorage(HTTPServerError):
    status_code = http.HTTPStatus.INSUFFICIENT_STORAGE


class HTTPLoopDetected(HTTPServerError):
    status_code = http.HTTPStatus.LOOP_DETECTED


class HTTPNotExtended(HTTPServerError):
    status_code = http.HTTPStatus.NOT_EXTENDED


class HTTPNetworkAuthenticationRequired(HTTPServerError):
    status_code = http.HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED


errors_classes = {
    # 300
    http.HTTPStatus.MULTIPLE_CHOICES: HTTPMultipleChoices,
    http.HTTPStatus.MOVED_PERMANENTLY: HTTPMovedPermanently,
    http.HTTPStatus.FOUND: HTTPFound,
    http.HTTPStatus.SEE_OTHER: HTTPSeeOther,
    http.HTTPStatus.NOT_MODIFIED: HTTPNotModified,
    http.HTTPStatus.USE_PROXY: HTTPUseProxy,
    # http.HTTPStatus.RESERVED: HTTPReserved,
    http.HTTPStatus.TEMPORARY_REDIRECT: HTTPTemporaryRedirect,
    http.HTTPStatus.PERMANENT_REDIRECT: HTTPPermanentRedirect,
    # 400
    http.HTTPStatus.BAD_REQUEST: HTTPBadRequest,
    http.HTTPStatus.UNAUTHORIZED: HTTPUnauthorized,
    http.HTTPStatus.PAYMENT_REQUIRED: HTTPPaymentRequired,
    http.HTTPStatus.FORBIDDEN: HTTPForbidden,
    http.HTTPStatus.NOT_FOUND: HTTPNotFound,
    http.HTTPStatus.METHOD_NOT_ALLOWED: HTTPMethodNotAllowed,
    http.HTTPStatus.NOT_ACCEPTABLE: HTTPNotAcceptable,
    http.HTTPStatus.PROXY_AUTHENTICATION_REQUIRED: HTTPProxyAuthenticationRequired,
    http.HTTPStatus.REQUEST_TIMEOUT: HTTPRequestTimeout,
    http.HTTPStatus.CONFLICT: HTTPConflict,
    http.HTTPStatus.GONE: HTTPGone,
    http.HTTPStatus.LENGTH_REQUIRED: HTTPLengthRequired,
    http.HTTPStatus.PRECONDITION_FAILED: HTTPPreconditionFailed,
    http.HTTPStatus.REQUEST_ENTITY_TOO_LARGE: HTTPRequestEntityTooLarge,
    http.HTTPStatus.REQUEST_URI_TOO_LONG: HTTPRequestUriTooLong,
    http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE: HTTPUnsupportedMediaType,
    http.HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE: HTTPRequestedRangeNotSatisfiable,
    http.HTTPStatus.EXPECTATION_FAILED: HTTPExpectationFailed,
    http.HTTPStatus.IM_A_TEAPOT: HTTPImATeapot,
    http.HTTPStatus.MISDIRECTED_REQUEST: HTTPMisdirectedRequest,
    http.HTTPStatus.UNPROCESSABLE_ENTITY: HTTPUnprocessableEntity,
    http.HTTPStatus.LOCKED: HTTPLocked,
    http.HTTPStatus.FAILED_DEPENDENCY: HTTPFailedDependency,
    http.HTTPStatus.TOO_EARLY: HTTPTooEarly,
    http.HTTPStatus.UPGRADE_REQUIRED: HTTPUpgradeRequired,
    http.HTTPStatus.PRECONDITION_REQUIRED: HTTPPreconditionRequired,
    http.HTTPStatus.TOO_MANY_REQUESTS: HTTPTooManyRequests,
    http.HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE: HTTPRequestHeaderFieldsTooLarge,
    http.HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS: HTTPUnavailableForLegalReasons,
    # 500
    http.HTTPStatus.INTERNAL_SERVER_ERROR: HTTPInternalServerError,
    http.HTTPStatus.NOT_IMPLEMENTED: HTTPNotImplemented,
    http.HTTPStatus.BAD_GATEWAY: HTTPBadGateway,
    http.HTTPStatus.SERVICE_UNAVAILABLE: HTTPServiceUnavailable,
    http.HTTPStatus.GATEWAY_TIMEOUT: HTTPGatewayTimeout,
    http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED: HTTPHttpServerVersionNotSupported,
    http.HTTPStatus.VARIANT_ALSO_NEGOTIATES: HTTPVariantAlsoNegotiates,
    http.HTTPStatus.INSUFFICIENT_STORAGE: HTTPInsufficientStorage,
    http.HTTPStatus.LOOP_DETECTED: HTTPLoopDetected,
    http.HTTPStatus.NOT_EXTENDED: HTTPNotExtended,
    http.HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED: HTTPNetworkAuthenticationRequired,
}
