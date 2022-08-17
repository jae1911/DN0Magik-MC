from os import environ
from pickle import dumps, loads

from redis import Redis

# ENV
REDIS_HOST = environ.get("REDIS_HOST", "localhost")
REDIS_PORT = environ.get("REDIS_PORT", 6379)

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)


def cache_val(key, val, expiration=86400):
    if not key or val:
        return None

    try:
        s = dumps(val)
        redis.set(key, s, expiration or None)
    except:
        return None


def get_val(key, default=None):
    if not key:
        return None

    try:
        v = redis.get(key)
        if not v:
            return default

        return loads(v) or default
    except:
        return default
