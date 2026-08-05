from werkzeug.exceptions import HTTPException


class HTTPExceptionSerializer:
    def __init__(self, error: HTTPException):
        self.error = error

    def serialize(self):
        return {
            "code": self.error.code,
            "name": self.error.name,
            "description": self.error.description,
        }
