import datetime

from peewee import *


DATABASE = SqliteDatabase('journal.db')


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([], safe=True)
    DATABASE.close()
