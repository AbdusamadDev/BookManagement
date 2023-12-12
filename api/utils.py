from exceptions import ValidationError, AuthenticationError

from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import bcrypt
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)


def hash_pwd(passwd):
    # hashing password for user security
    bytes = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes, salt)
    return hashed_pwd


def verify_pwd(passwd, hashed_pwd):
    bytes_pwd = passwd.encode("utf-8")
    result = bcrypt.checkpw(bytes_pwd, hashed_pwd)
    return result


def generate_token(payload):
    try:
        algorithm = os.environ.get("ALGORITHM")
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return token
    except JWTError as jwt_error:
        return None, str(jwt_error)


def decode_token(token):
    try:
        algorithm = os.environ.get("ALGORITHM")
        secret_key = os.environ.get("SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as jwt_error:
        return None, str(jwt_error)


def authenticate_or_abort(token):
    decoded_payload = decode_token(token)
    if "username" in decoded_payload.keys() and "password" in decoded_payload.keys():
        user = 
    return AuthenticationError(
        description="Authentication credentials failed", status=401
    )


if __name__ == "__main__":
    print(
        decode_token(
            generate_token(
                payload={"msg": "hello", "exp": datetime.now() + timedelta(days=3)}
            )
        )
    )
