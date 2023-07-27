import os

from models import TimerObject, CheckBoxTable, db
from peewee import *

MODELS_TUPLE = (TimerObject, CheckBoxTable)

def create_and_migrate():
    """Создание и миграции в БД."""

    for obj in MODELS_TUPLE:
        db.create_tables([obj])


def check_sql():
    """
    Checking for the presence of a database.
    Проверка на наличие БД.
    """

    if not os.path.exists("TaskTimerDB.db"):
        create_and_migrate()
