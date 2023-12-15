from exceptions import AuthenticationError, ValidationError, DatabaseError
from flask import Blueprint, request, make_response, g, send_from_directory
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

@bms_route.get("/uploads/<fiename>")
def uploads(filename):
    return send_from_directory()

# CREATE
@bms_route.route("/books/create", methods=["POST"])
def create():
    # Validation
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    collected_data = {}
    books.name = "books"
    requirements = ["title", "page", "author", "publication_date"]
    keys = data.keys()
    for field in requirements:
        if field not in keys:
            return ValidationError(f"Field {field} is not provided")
        else:
            if data.get(field) is None or data.get(field) == "":
                return ValidationError(f"Field: {field} cannot be null or blank")
            collected_data[field] = data[field]
    source = request.files.get("source", None)
    if source is None:
        return ValidationError("Book source is not provided: source")
    source_path = os.path.join(
        str(os.path.abspath(__name__))[:-3], "uploads", source.filename
    )
    if source is None:
        return ValidationError("The books source is not provided")
    if not (source.filename.endswith(".pdf") or source.filename.endswith(".html")):
        return ValidationError("Only pdf and html files are allowed as a book")
    try:
        # Book creation
        books.add(
            user=g.user_id,
            source_path=f"/uploads/{source.filename}",
            date_created=str(datetime.now()),
            **collected_data,
        )
        source.save(source_path)
    except Exception as error:
        return DatabaseError(description=str(error))
    # Successful response
    return make_response(dict(data), 201)


@bms_route.get("/books/<book_id>")
def get(book_id: int):
    books.name = "books"
    book = books.get(id=book_id)
    if len(book) == 0:
        return {}
    return {books.columns[i]: book[i] for i in range(len(book))}

