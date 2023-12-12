from flask import Blueprint, request
from authentication import authenticate_or_abort


bms_route = Blueprint("Book Management Service", __name__)


@bms_route.post("/books/create")
def create():
    authenticate_or_abort(request.headers.get("token", None))
    # Now request is trusted and authenticated
    pass
