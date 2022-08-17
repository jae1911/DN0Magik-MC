from utils.db import get_object, Users


def get_uuid_from_username(username: str):
    user = get_object(Users, username=username)

    return user.uuid if user else None
