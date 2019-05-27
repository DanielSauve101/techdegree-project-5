import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=50)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        with DATABASE.transaction():
            cls.create(
                username=username,
                password=generate_password_hash(password)
            )


class Entry(Model):
    user = ForeignKeyField(User, related_name='entries')
    title = CharField(max_length=100)
    date = DateField(formats=['%Y-%m-%d'])
    time = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('date',)


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry], safe=True)
    DATABASE.close()
