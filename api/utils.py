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

if __name__ == "__main__":
    print(generate_token({"user": "Abdusamad"}))
