from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response

import json

class ValidationError(HTTPException):
    """Custom Validation error for api"""

    status = 400

    def get_response(self):
        exception_body = json.dumps({"msg": "Validation error with "})
