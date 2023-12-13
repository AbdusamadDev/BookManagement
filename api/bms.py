from flask import Blueprint, request
from authentication import is_authenticated
from exceptions import AuthenticationError


bms_route = Blueprint("Book Management Service", __name__)


@bms_route.post("/books/create")
def create():
    token = request.headers.get("token", None)
    print(token)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    # Now request is trusted and authenticated
    return "Authenticated successfully!"
