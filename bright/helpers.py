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

def raise_errors_on_failure(response):
    if response.status_code == 404:
        raise ResourceNotFound("Not found.")
    elif response.status_code == 400:
        raise BadRequest("Incoming request body does not contain a valid JSON object.")
    elif response.status_code == 401:
        raise AuthenticationError("Unnknown API Key. Please check your API key and try again")
    elif response.status_code == 413:
        raise RequestTooLarge("File size too large.")
    elif response.status_code == 415:
        raise FileTypeUnsupported("File type not supported.")
    elif response.status_code == 429:
        raise TooManyRequests("Overage usage limit hit.")
    elif response.status_code == 500:
        raise ServerError("BRIGHT has encountered an unexpected error and cannot fulfill your request")
    elif response.status_code == 502:
        raise BadGatewayError("Bad gateway.")
    elif response.status_code == 503:
        raise ServiceUnavailableError("Service unavailable.")

    return response