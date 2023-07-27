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

    task_name = CharField(
        max_length=70,
        help_text="Name of the task",
    )
    start_date = DateTimeField(
        help_text="Initial time",
    )
    end_date = DateTimeField(
        help_text="End time",
    )
    amount_of_time = CharField(
        help_text="Amount of time",
    )
    task_about = TextField(
        help_text="Notes",
    )

    def __str__(self) -> str:
        """Для вывода строкового представления."""

        return (
            f'Объект {self.task_name[:AMOUNT_CHAR_TO_SLICE]}, '
            'продолжительность , '
            f'{self.amount_of_time[:AMOUNT_CHAR_TO_SLICE]}'
            f'дата {self.create_date[:AMOUNT_CHAR_TO_SLICE]}'
        )
    

class CheckBoxTable(BaseModel):
    """
    Модель для чекбоксов.
    Model for checkboxes.
    """

    task_name = BooleanField(
        help_text="Name of the task",
    )
    start_date = BooleanField(
        help_text="Initial time",
    )
    end_date = BooleanField(
        help_text="End time",
    )
    amount_of_time = BooleanField(
        help_text="Amount of time",
    )
    task_about = BooleanField(
        help_text="Notes",
    )

    def __str__(self) -> str:
        """Для вывода строкового представления."""

        return (
            f'task_name - {self.task_name}, '
            f'start_date - {self.start_date}, '
            f'end_date - {self.end_date}, '
            f'amount_of_time - {self.amount_of_time}, '
            f'task_about - {self.task_about}.'
        )

