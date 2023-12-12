import bcrypt


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


if __name__ == "__main__":
    print(verify_pwd("wassup", hash_pwd("wassup")))
