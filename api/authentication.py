from flask import Blueprint, request
from exceptions import ValidationError


auth_route = Blueprint("auth", __name__)


@auth_route.post("/users/")
def register():
    data = request.get_json()
    # Validation process goes for valid json data
    requirements = {
        "username": "Username was not provided",
        "email": "Email was not provided",
        "password": "Password was not provided",
        "confirm_password": "Confirm of password was not passed"
    }
    for key, value in requirements.items():
        if key not in data.keys():
            return ValidationError(value)
    email, username, password, confirm_password = data.get("email"), d
    if "@" not in vl_email or "." not in vl_email:
        return ValidationError(description="Invalid Email provided!")
    
