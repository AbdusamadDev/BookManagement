from flask import Blueprint, request
from exceptions import ValidationError


auth_route = Blueprint("auth", __name__)


@auth_route.post("/users/new/")
def register():
    data = request.get_json()
    if "username" not in data.keys():
        return ValidationError("Username was not provided")
    return "success for now"
