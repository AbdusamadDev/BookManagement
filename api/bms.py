from exceptions import AuthenticationError, ValidationError, DatabaseError
from flask import Blueprint, request, make_response, g
from authentication import is_authenticated
from models import Database
from utils import decode_token
from datetime import datetime
import os


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

@bms_route.before_request
def authentication_middleware():
    token = request.headers.get("Authorization", None)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    username = decode_token(token).get("username")
    books.name = "users"
    user_id = books.get(username=username)
    if user_id:
        user_id = user_id[0]
        g.user_id = user_id


# CREATE
@bms_route.route("/books/create", methods=["POST"])
def create():
    # Authentication
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    books.name = "books"
    # Fields validation
    for key, value in data.items():
        if (value is None) or (not value):
            print("Value is being none")
            return ValidationError(f"This field can't be blank or null: {key}")
        if key not in books.columns:
            return ValidationError(description=f"Invalid field provided: {key}")
    # Fields preparation for book creation
    title = data.get("title")
    page = data.get("page")
    author = data.get("author")
    source = request.files.get("source")
    publication_date = data.get("publication_date")
    source_path = os.path.join(
        str(os.path.abspath(__name__))[:-3], "uploads", source.filename
    )
    # try:
        # Check book format
    if not (source.filename.endswith(".pdf") or source.filename.endswith(".html")):
        return ValidationError("Only pdf and html files are allowed as a book")
    # Book creation
    books.add(
        title=title,
        page=page,
        user=g.user_id,
        author=author,
        source_path=str(source_path),
        publication_date=publication_date,
        date_created=str(datetime.now()),
    )
    source.save(source_path)
    # except Exception as error:
    #     return DatabaseError(description=str(error))
    # Successful response
    return make_response(dict(data), 201)


@bms_route.patch("/books/update/<id>")
def partial_update(id: int):
    # Authentication
    token = request.headers.get("Authorization", None)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    else:
        username = decode_token(token).get("username")
        books.name = "users"
        user_id = books.get(username=username)
        if user_id:
            user_id = user_id[0]

