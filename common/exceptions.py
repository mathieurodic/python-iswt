class InvalidInputError(Exception):
    http_code = 400

class ForbiddenError(Exception):
    http_code = 403

class NotFoundError(Exception):
    http_code = 404

class ConflictError(Exception):
    http_code = 409

class DuplicateError(Exception):
    http_code = 409

class ServiceError(Exception):
    http_code = 503
