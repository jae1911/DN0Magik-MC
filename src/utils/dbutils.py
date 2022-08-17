from datetime import datetime, timedelta
from uuid import uuid4
from base64 import b64encode

from bcrypt import gensalt, hashpw, checkpw

from utils.redisutil import cache_val, get_val
from utils.db import get_object, Users, UsernameHistory


def get_uuid_from_username(username: str):
    cachekey = f"get_uuid_from_username_{username}"

    cached_val = get_val(cachekey)
    if cached_val:
        return cached_val

    user = get_object(Users, username=username)

    cache_val(cachekey, user.uuid if user else None, 3600)

    return user.uuid if user else None


def get_users_registered_last_day():
    cachekey = "get_users_registered_last_day"

    cached_val = get_val(cachekey)
    if cached_val:
        return cached_val

    day_ago = datetime.now() - timedelta(days=1)

    number_last_day = Users.select().where(Users.registered_on > day_ago).count()

    cache_val(cachekey, number_last_day, expiration=3600)

    return number_last_day


def get_all_users_count():
    cachekey = "get_all_users_count"

    cached_val = get_val(cachekey)
    if cached_val:
        return cached_val

    number_all_users = Users.select().count()

    cache_val(cachekey, number_all_users, expiration=3600)

    return number_all_users


def hash_password(password: str):
    salt = gensalt(10)
    hashed = hashpw(password.encode("utf-8"), salt)

    return str(hashed.decode())


def register_user(username: str, password: str):
    # USER CHECK
    existing_user = get_object(Users, username=username)
    if existing_user:
        return None

    # DO REGISTRATION
    hashed_pass = hash_password(password)
    uuid = str(uuid4())
    register_date = datetime.now()

    user = Users.create(
        username=username,
        password=hashed_pass,
        uuid=uuid,
        registered_on=register_date,
    )

    uh = UsernameHistory.create(
        username=username, changed_on=register_date, uuid=user.uuid
    )

    user.save()
    uh.save()

    return uuid


def verify_login(username: str, password: str):
    user_exists = get_object(Users, username=username)
    if not user_exists:
        return False

    check = hashpw(str.encode(password), str.encode(user_exists.password))
    return check


def get_user_remoteid(username: str):
    user_exists = get_object(Users, username=username)
    if not user_exists:
        return None

    return user_exists.id
