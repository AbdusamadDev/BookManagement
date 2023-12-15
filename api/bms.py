from exceptions import AuthenticationError, ValidationError, DatabaseError
from flask import Blueprint, request, Response
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


@bms_route.route("/books/create", methods=["POST"])
def create():
    # Authentication
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
        print("Form: ", dict(data))
    token = request.headers.get("Authorization", None)
    if not is_authenticated(token):
        return AuthenticationError(description="Not authenticated", status=401)
    else:
        username = decode_token(token).get("username")
        books.name = "users"
        user_id = books.get(username=username)
        if user_id:
            user_id = user_id[0]
    books.name = "books"
    # Fields validation
    for key, value in data.items():
        if value is None:
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
    # Book creation
    # try:
    print(source_path)
    books.add(
        title=title,
        page=page,
        author=author,
        source_path=str(source_path),
        publication_date=publication_date,
        date_created=str(datetime.now()),
        user=user_id,
    )
    source.save(source_path)
    # except Exception as error:
    #     return DatabaseError(description=str(error))
    # Successful response
    return Response(data, status=201)
