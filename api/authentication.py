from exceptions import ValidationError, DatabaseError
from flask import Blueprint, request, Response
from utils import hash_pwd, generate_token
from datetime import timedelta, datetime
from models import Database

auth_route = Blueprint("auth", __name__)


@auth_route.post("/users/")
def register():
    data = request.get_json()
    # Validation process goes for valid json data
    requirements = {
        "username": "Username was not provided",
        "email": "Email was not provided",
        "password": "Password was not provided",
        "confirm_password": "Confirm of password was not passed",
    }
    for key, value in requirements.items():
        if key not in data.keys():
            return ValidationError(value)
    email, username, password, confirm_password = (
        data.get("email"),
        data.get("username"),
        data.get("password"),
        data.get("confirm_password"),
    )
    if "@" not in email or "." not in email:
        return ValidationError(description="Invalid Email provided!")
    if password != confirm_password:
        return ValidationError("Passwords didn't match!")

    try:
        user = Database(
            "users",
            fields={
                "username": "TEXT NOT NULL",
                "email": "TEXT UNIQUE NOT NULL",
                "password": "TEXT",
            },
        )
        user.add(username=username, email=email, password=hash_pwd(password))
    except Exception as body:
        return DatabaseError(description=str(body), status=422)

    payload = {"username": username, "exp": datetime.now() + timedelta(days=3)}
    new_token = generate_token(payload=payload)
    return Response({"user": username, "token": new_token})
