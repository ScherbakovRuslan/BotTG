from peewee import *
from db import *
import asyncio


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    id = AutoField()
    user_id = IntegerField(null=False)
    name = TextField(null=False)

    class Meta:
        table_name = 'users'


class Buses(BaseModel):
    id = AutoField()
    coming = TextField(null=False)
    price = IntegerField(null=False)

    class Meta:
        table_name = 'buses'


class History(BaseModel):
    id = AutoField()
    user_id = TextField(null=False)
    place = IntegerField(null=False)
    bus_name = TextField(null=False)
    price = IntegerField(null=False)
    date_by = TextField(null=False)
    date_travel = TextField(null=False)

    class Meta:
        table_name = 'history'
        database = db


class Schedule(BaseModel):
    id = AutoField()
    bus_id = IntegerField(null=False)
    places = IntegerField(null=False)
    data = TextField(null=False)

    class Meta:
        table_name = 'schedule'


async def setup_database():
    db = await create_db_connection()
    await db.connect()
    await db.create_tables([Users, Buses, History, Schedule])
