from constants import AMOUNT_CHAR_TO_SLICE
from peewee import *

db = SqliteDatabase('TaskTimerDB.db')


class BaseModel(Model):
    """Базовая модель. The basic model."""

    class Meta:
        database = db


class TimerObject(BaseModel):
    """
    Модель для записи объекта таймера.
    A model for recording a timer object.
    """

    task_name = CharField(max_length=70)
    start_date = DateTimeField()
    end_date = DateTimeField()
    amount_of_time = CharField()
    task_about = TextField()

    def __str__(self) -> str:
        """Для вывода строкового представления."""

        return (
            f'Объект {self.task_name[:AMOUNT_CHAR_TO_SLICE]}, '
            'продолжительность , '
            f'{self.amount_of_time[:AMOUNT_CHAR_TO_SLICE]}'
            f'дата {self.create_date[:AMOUNT_CHAR_TO_SLICE]}'
        )
    

class CheckBoxTable(BaseModel):
    """ """

    task_name = BooleanField()
    start_date = BooleanField()
    end_date = BooleanField()
    amount_of_time = BooleanField()
    task_about = BooleanField()

    def __str__(self) -> str:
        """Для вывода строкового представления."""

        return (
            f'task_name - {self.task_name}, '
            f'start_date - {self.start_date}, '
            f'end_date - {self.end_date}, '
            f'amount_of_time - {self.amount_of_time}, '
            f'task_about - {self.task_about}.'
        )

