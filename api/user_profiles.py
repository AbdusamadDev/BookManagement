from exceptions import ValidationError, DatabaseError
from flask import Blueprint, request, jsonify
from utils import hash_pwd, generate_token, cesar_hash
from datetime import timedelta, datetime
from models import Database

auth_route = Blueprint("authentication", __name__)
database = Database(
    "users",
    fields={
        "id": "SERIAL",
        "username": "TEXT UNIQUE NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "password": "TEXT",
    },
    addons="PRIMARY KEY (id)"
)
database.createdb()


@auth_route.post("/auth/users")
def register():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    # Validation process goes for valid json data
    requirements = {
        "username": "Username was not provided",
        "email": "Email was not provided",
        "password": "Password was not provided",
        "confirm_password": "Confirm of password was not passed",
    }
    for key, value in requirements.items():
        if key not in data.keys():
            return ValidationError(description=value)
    email, username, password, confirm_password = (
        data.get("email"),
        data.get("username"),
        data.get("password"),
        data.get("confirm_password"),
    )
    if "@" not in email or "." not in email:
        return ValidationError(description="Invalid Email provided!")
    if password != confirm_password:
        return ValidationError(description="Passwords didn't match!")
    new_pwd = hash_pwd(password).decode()
    try:
        if database.get(username=username):
            return ValidationError(
                description=f"User with username: {username} already exists!",
                status=400,
            )
        database.add(username=username, email=email, password=new_pwd)
    except Exception as body:
        return DatabaseError(description=str(body), status=422)

    payload = {
        "username": username,
        "password": cesar_hash(password, 10, "+"),
        "exp": datetime.now() + timedelta(days=3),
    }
    new_token = generate_token(payload=payload)
    return jsonify({"user": username, "token": new_token})
