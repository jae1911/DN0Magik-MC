from peewee import (
    SqliteDatabase,
    Model,
    Charfield,
    DateTimeField,
    IntegerField,
    ForeignKeyField,
)

# TODO: SUPPORT OTHER DBS THAN SQLITE
database = SqliteDatabase("mc.db")


class BaseModel(Model):
    # Base model
    class Meta:
        database = database


class Users(BaseModel):
    id = IntegerField(primary_key=True)
    username = Charfield(null=False)
    password = Charfield(null=True)  # NULL TRUE = IN CASE OF SSO LOGIN/REGISTER
    uuid = Charfield(null=False)
    registered_on = DateTimeField(
        null=False
    )  # USED MAINLY FOR NICE DATA STATS IN api/statusapi:status_order_stats()


class UsernameHistory(BaseModel):
    id = IntegerField(primary_key=True)
    username = Charfield(null=False)
    changed_on = DateTimeField(null=False)
    uuid = ForeignKeyField(Users, backref="uuid")
