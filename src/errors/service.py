from helpers.errors import BaseError


class UserServiceIsUnavailableError(BaseError):
    message = 'User service is unavailable'
