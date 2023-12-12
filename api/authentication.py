from exceptions import ValidationError, DatabaseError
from flask import Blueprint, request, jsonify, authenticate
from utils import hash_pwd, generate_token
from datetime import timedelta, datetime
from models import Database

auth_route = Blueprint("authentication", __name__)


@auth_route.post("/auth/users")
def register():
    data = request.get_json()
    # Validation process goes for valid json data
    print("Validation is being executed")
    requirements = {
        "username": "Username was not provided",
        "email": "Email was not provided",
        "password": "Password was not provided",
        "confirm_password": "Confirm of password was not passed",
    }
    for key, value in requirements.items():
        print(key, value)
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

    try:
        user = Database(
            "users",
            fields={
                "username": "TEXT NOT NULL",
                "email": "TEXT UNIQUE NOT NULL",
                "password": "TEXT",
            },
        )
        user.createdb()
        user.add(username=username, email=email, password=hash_pwd(password).decode())
        print("User creation")
    except Exception as body:
        print("Database error: ", body)
        return DatabaseError(description=str(body), status=422)

    payload = {"username": username, "exp": datetime.now() + timedelta(days=3)}
    new_token = generate_token(payload=payload)
    print("Success")
    return jsonify({"user": username, "token": new_token})


@auth_route.post("/users/login")
def login():
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)
    if username or password is None:
        return 
