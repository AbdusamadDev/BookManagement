from flask import Blueprint, request
from authentication import is_authenticated
from exceptions import AuthenticationError, ValidationError
from models import Database
from utils import decode_token


bms_route = Blueprint("Book Management Service", __name__)
books = Database(
    name="books",
    fields={
        "id": "SERIAL",
        "title": "TEXT NOT NULL",
        "page": "INtEGER",
        "author": "TEXT NOT NULL",
        "source_path": "TEXT NOT NULL",
        "publication_date": "TEXT",
        "date_created": "TEXT",
        '"user"': "INTEGER NOT NULL",
    },
    addons='PRIMARY KEY (id), FOREIGN KEY ("user") REFERENCES users (id)',
)
books.createdb()


@bms_route.post("/books/create")
def create():
    # Authentication
    token = request.headers.get("Authorization", None)
    data = request.get_json()
    print(token)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    else:
        username = decode_token(token)
        books.name = ""
        user_id = 
    # Fields validation
    for key in data.keys():
        if key not in books.columns:
            return ValidationError(description=f"Invalid field provided: {key}")
    # Fields preparation for book creation
    title = data.get("title")
    page = data.get("page")
    author = author.get("author")
    source_path = "path"
    publication_date = data.get("publication_date")
    user = ""
