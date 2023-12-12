import bcrypt


def hash_pwd(passwd):
    # hashing password for user security
    bytes = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes, salt)
    return hashed_pwd


def verify_pwd(passwd, hashed_pwd):
    bytes = passwd.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    userBytes = hashed_pwd.encode("utf-8")
    result = bcrypt.checkpw(hash, userBytes)
    return result

if __name__ == "__main__":
    print(verify_pwd("wassup", hash_pwd("wassup")))