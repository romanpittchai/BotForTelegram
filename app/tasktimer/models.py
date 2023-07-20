import datetime

from constants import AMOUNT_CHAR_TO_SLICE
from peewee import *

db = SqliteDatabase('TaskTimerDB.db')


class BaseModel(Model):
    class Meta:
        database = db


class TimerObject(BaseModel):
    """Модель для записи объекта таймера."""

    task_name = CharField(max_length=70)
    start_date = DateTimeField()
    end_date = DateTimeField()
    amount_of_time = CharField()
    task_about = TextField()

    def __str__(self) -> str:
        """Для вывода строкового представления."""
        return (f'Объект {self.task_name[:AMOUNT_CHAR_TO_SLICE]}, '
                'продолжительность , '
                f'{self.amount_of_time[:AMOUNT_CHAR_TO_SLICE]}'
                f'дата {self.create_date[:AMOUNT_CHAR_TO_SLICE]}')
