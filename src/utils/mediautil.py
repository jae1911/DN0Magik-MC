from os import environ, remove, mkdir
from hashlib import sha1

from boto3 import client
from botocore.exceptions import ClientError

from utils.db import Media
from utils.redisutil import cache_val, get_val

# ENV
S3_ENDPOINT = environ.get("S3_ENDPOINT")
S3_PRIVATE_KEY = environ.get("S3_PRIVATE_KEY")
S3_LOGIN_KEY = environ.get("S3_LOGIN_KEY")
S3_BUCKET = environ.get("S3_BUCKET")

client_args = {
    "aws_access_key_id": S3_LOGIN_KEY,
    "aws_secret_access_key": S3_PRIVATE_KEY,
    "endpoint_url": S3_ENDPOINT,
}

s3_client = client("s3", **client_args)
ALLOWED_EXTENSIONS = {"png"}
TEMP_UPLOAD_FOLDER = "/tmp/mc/"


def upload_file(path: str, type: str, player: str):
    file_hash = get_hash(path)
    final_file_name = f"{type}/{file_hash}.png"
    uuid = get_uuid_from_username(player)

    m = Media.create(hash=file_hash, type=type, uuid=uuid)

    try:
        res = s3_client.upload_file(path, S3_BUCKET, final_file_name)
    except ClientError as e:
        return False

    remove(path)

    m.save()
    return True


def download_file(hash: str, path: str):
    try:
        s3_client.download_file(S3_BUCKET, hash, path)
    except:
        return False

    return True


def delete_file(path: str):
    try:
        s3_client.delete_object(S3_BUCKET, path)
    except:
        return False

    return True


def get_hash(file: str):
    h = sha1()

    with open(file, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()


def get_player_skin(uuid: str):
    cachekey = f"player_skin_hash_{uuid}"
    cached_val = get_val(cachekey)
    if cached_val:
        return cached_val

    try:
        m = Media.select().where(Media.uuid == uuid and Media.type == "SKIN").get()

        cache_val(cachekey, m.hash)

        return m.hash
    except:
        return None


def get_player_cape(uuid: str):
    cachekey = f"player_cape_hash_{uuid}"
    cached_val = get_val(cachekey)
    if cached_val:
        return cached_val

    try:
        m = Media.select().where(Media.uuid == uuid and Media.type == "CAPE").get()

        cache_val(cachekey, m.hash)

        return m.hash
    except:
        return None


def remove_skin_from_player(username: str):
    uuid = get_uuid_from_username(username)

    m = Media.select().where(Media.uuid == uuid and Media.type == "SKIN").get()

    full_path = f"SKIN/{m.hash}.png"

    m.delete_instance()

    delete_file(full_path)

    return None


def is_file_allowed(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_temp_folder():
    os.mkdir(f"{TEMP_UPLOAD_FOLDER}")
    os.mkdir(f"{TEMP_UPLOAD_FOLDER}/skins")
    os.mkdir(f"{TEMP_UPLOAD_FOLDER}/capes")
