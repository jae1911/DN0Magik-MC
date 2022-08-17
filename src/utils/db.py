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
    id = IntegerField(primary_key=True)
    username = CharField(null=False)
    password = CharField(null=True)  # NULL TRUE = IN CASE OF SSO LOGIN/REGISTER
    uuid = CharField(null=False)
    registered_on = DateTimeField(
        null=False
    )  # USED MAINLY FOR NICE DATA STATS IN api/statusapi:status_order_stats()


class UsernameHistory(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(null=False)
    changed_on = DateTimeField(null=False)
    uuid = ForeignKeyField(Users, backref="uuid")


def get_object(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        return None
