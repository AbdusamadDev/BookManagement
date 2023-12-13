from exceptions import AuthenticationError
from utils import decode_token, verify_pwd
from models import Database


def is_authenticated(token):
    if token is None:
        return False
    decoded_payload = decode_token(token)
    if "username" in decoded_payload.keys() and "password" in decoded_payload.keys():
        model = Database(name="users")
        user = model.get(username=decoded_payload.get("username"))
        if user:
            is_correct_passwd = verify_pwd(decoded_payload.get("password"), user[-1])
            if not is_correct_passwd:
                return False
            return True
        else:
            return False
    return False
