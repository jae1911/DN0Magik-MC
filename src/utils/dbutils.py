from datetime import datetime, timedelta

from utils.db import get_object, Users


def get_uuid_from_username(username: str):
    user = get_object(Users, username=username)

    return user.uuid if user else None


def get_users_registered_last_day():
    day_ago = datetime.now() - timedelta(days=1)

    number_last_day = Users.select().where(Users.registered_on > day_ago).count()

    return number_last_day


def get_all_users_count():
    number_all_users = Users.select().count()

    return number_all_users
