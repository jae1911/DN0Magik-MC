from peewee import (
    SqliteDatabase,
    CharField,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
    Model,
)
from playhouse import migrate

# TODO: SUPPORT OTHER DBS THAN SQLITE
database = SqliteDatabase("mc.db")


class BaseModel(Model):
    # Base model
    class Meta:
        database = database


class Users(BaseModel):
    username = CharField(null=False)
    password = CharField(null=True)  # NULL TRUE = IN CASE OF SSO LOGIN/REGISTER
    uuid = CharField(null=False)
    registered_on = DateTimeField(
        null=False
    )  # USED MAINLY FOR NICE DATA STATS IN api/statusapi:status_order_stats()


class UsernameHistory(BaseModel):
    username = CharField(null=False)
    changed_on = DateTimeField(null=False)
    uuid = ForeignKeyField(model=Users, column_name="uuid")


class Media(BaseModel):
    hash = CharField(null=False)
    type = CharField(null=False)  # MAY BE "SKIN" OR "CAPE" DEPENDING ON WHAT USER CHOSE
    uuid = ForeignKeyField(model=Users, column_name="uuid")


def get_object(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        return None
