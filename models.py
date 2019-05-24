import datetime

from peewee import *


DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    title = CharField(max_length=100)
    date = DateField(formats=['%Y-%m-%d'])
    time = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('date',)

    @classmethod
    def create_entry(cls, title, date, time, learned, resources):
        with DATABASE.transaction():
            cls.create(
                title=title,
                date=date,
                time=time,
                learned=learned,
                resources=resources
            )


def initialise():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
