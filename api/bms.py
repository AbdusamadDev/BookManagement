from flask import Blueprint, request
from authentication import is_authenticated


bms_route = Blueprint("Book Management Service", __name__)


@bms_route.post("/books/create")
def create():
    token = request.headers.get("token", None)
    print(token)
    is_authenticated(token)
    # Now request is trusted and authenticated
    return "Authenticated successfully!"
