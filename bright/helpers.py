class BrightException(Exception):
    """ Base error. """
    def __init__(self, message, result=None):
        super(BrightException, self).__init__(message)
        self.result = result

class BadRequest(BrightException):
    code = 400

class AuthenticationError(BrightException):
    code = 401

class Forbidden(BrightException):
    code = 403

class TooManyRequests(BrightException):
    code = 429

class ResourceNotFound(BrightException):
    code = 404

class ServerError(BrightException):
    code = 500

class BadGatewayError(BrightException):
    code = 502

class ServiceUnavailableError(BrightException):
    code = 503


def get_error(response):
    try:
        json = response.json()
        if "message" in json:
            return json['message']
        if "error" in json:
            return json["error"]
    except ValueError:
        pass

    return ''


def raise_errors_on_failure(response):
    if response.status_code == 500:
        raise ServerError("Internal Server Error")
    elif response.status_code == 502:
        raise BadGatewayError("Bad Gateway")
    elif response.status_code == 503:
        raise ServiceUnavailableError("Service is unvailable")

    msg = ""

    if not str(response.status_code).startswith('2') \
        or not str(response.status_code).startswith('3'):
        msg = get_error(response)

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

    return response
