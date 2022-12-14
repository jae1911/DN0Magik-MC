from os import environ
from base64 import b64encode
from time import time

from jwt import encode, decode

from utils.redisutil import cache_val, get_val

# ENV
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")


def encode_auth_jwt(username: str, client_token: str):
    # IF THERE IS A GOD, HE WEEPS
    # user_base = str(b64encode(username.encode("ascii")))
    # token_base = str(b64encode(client_token.encode("ascii")))

    payload = {
        "sub": username,
        "yggt": client_token,
        "spr": username,
        "iss": "dn0magik",
        "exp": int(time()) + 86400,
        "iat": int(time()),
    }

    encoded_jwt = encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    return encoded_jwt


def check_auth_jwt(token: str, client_identifer: str):
    if not client_identifer:
        try:
            data = decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except:
            return None

        return data
    else:
        try:
            data = decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

            ctoken = data["yggt"]
            cuser = data["sub"]

            if client_identifer == ctoken:
                return cuser
            else:
                return False
        except:
            return None
