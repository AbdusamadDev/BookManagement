from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response
from flask import jsonify


class ValidationError(HTTPException):
    """Custom Validation error for api"""

    def __init__(
        self,
        description: str | None = None,
        response: Response | None = None,
        status=400,
    ) -> None:
        self.status = status
        super().__init__(description, response)

    def get_response(self):
        exception_body = jsonify({"msg": self.description})
        exception_body.status = self.status
        return exception_body
