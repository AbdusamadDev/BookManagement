from flask import Blueprint, request
from authentication import is_authenticated
from exceptions import AuthenticationError
from models import Database


bms_route = Blueprint("Book Management Service", __name__)
books = Database(
    name="books",
    fields={
        "id": "INTEGER PRIMARY KEY ('id')",
        "title": "TEXT NOT NULL",
        "page": "INEGER",
        "author": "TEXT NOT NULL",
        "source_path": "TEXT NOT NULL",
        "publication_date": "TEXT",
        "date_created": "TEXT",
        "user": "INTEGER FOREIGN KEY ('id') REFERENCES users ('id') NOT NULL",
    },
)
books.createdb()

@bms_route.post("/books/create")
def create():
    token = request.headers.get("Authorization", None)
    print(token)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    # Now request is trusted and authenticated
