from datetime import datetime, timedelta

from utils.redisutil import cache_val, get_val
from utils.db import get_object, Users


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
