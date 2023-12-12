from flask import Blueprint, request
from exceptions import ValidationError


auth_route = Blueprint("auth", __name__)


@auth_route.post("/users/new/")
def register():
    data = request.get_json()
    # Validation process goes for valid json data
    if "username" not in data.keys():
        return ValidationError(description="Username was not provided!")
    if "email" not in data.keys():
        vl_email = data.get("email")
        if "@" not in vl_email or "." not in vl_email:
            return ValidationError(description="Invalid Email provided!")
        return ValidationError(description="Email is not provided!")
