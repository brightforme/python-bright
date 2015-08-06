import requests

class BrightException(Exception):
    """ Base error. """
    def __init__(self, message, result=None):
        super(BrightException, self).__init__(message)
        self.result = result

class BadRequest(BrightException):
    pass

class AuthenticationError(BrightException):
    pass

class BadGatewayError(BrightException):
    pass

class ResourceNotFound(BrightException):
    pass

class ServerError(BrightException):
    pass

class ServiceUnavailableError(BrightException):
    pass

class RequestTooLarge(BrightException):
    pass

class FileTypeUnsupported(BrightException):
    pass

class UnprocessableEntity(BrightException):
    pass

class TooManyRequests(BrightException):
    pass

class Forbidden(BrightException):
    pass


def get_error_json(json):
    return json['message']

def raise_errors_on_failure(response):

    msg = ""
    if response.status_code != requests.codes.ok:
        msg = get_error_json(response.json())

    if response.status_code == 404:
        raise ResourceNotFound(msg)
    elif response.status_code == 400:
        raise BadRequest(msg)
    elif response.status_code == 401:
        raise AuthenticationError(msg)
    elif response.status_code == 403:
        raise Forbidden(msg)
    elif response.status_code == 429:
        raise TooManyRequests(msg)
    elif response.status_code == 500:
        raise ServerError(msg)
    elif response.status_code == 502:
        raise BadGatewayError(msg)
    elif response.status_code == 503:
        raise ServiceUnavailableError(msg)

    return response