from flask import Blueprint, request
from authentication import authenticate_or_abort


bms_route = Blueprint("Book Management Service", __name__)


@bms_route.post("/books/create")
def create():
    token = request.headers.get("token", None)
    print(token)
    authenticate_or_abort(to)
    # Now request is trusted and authenticated
    return "Authenticated successfully!"
