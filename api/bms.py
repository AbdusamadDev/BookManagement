from flask import Blueprint, request
from authentication import is_authenticated
from exceptions import AuthenticationError
from models import D


bms_route = Blueprint("Book Management Service", __name__)
books = Database()


@bms_route.post("/books/create")
def create():
    token = request.headers.get("Authorization", None)
    print(token)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    # Now request is trusted and authenticated
    # Book Title
    # Book page amount
    # Book author
    # Book source (pdf)
    # User (book created user)
    # Publication date
    # date created

