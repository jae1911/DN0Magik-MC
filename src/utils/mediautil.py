from os import environ
from hashlib import sha1

from boto3 import client
from botocore.exceptions import ClientError

from utils.db import Media

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


def upload_file(path: str, type: str, player: str):
    file_hash = get_hash(path)
    final_file_name = f"{file_hash}.png"

    m = Media.create(hash=file_hash, type=type, uuid=player)

    try:
        res = s3_client.upload_file(path, S3_BUCKET, final_file_name)
    except ClientError as e:
        return False

    m.save()
    return True


def get_hash(file: str):
    h = sha1()

    with open(file, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
