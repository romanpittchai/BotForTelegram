import os

from models import TimerObject, CheckBoxTable, db
from peewee import *

from constants import TUPLE_OF_DEFAULT_VALUES
MODELS_TUPLE = (TimerObject, CheckBoxTable)



def create_and_migrate():
    """Создание и миграции в БД."""

    db.connect()
    for obj in MODELS_TUPLE:
        db.create_tables([obj])
    
    CheckBoxTable.create(**TUPLE_OF_DEFAULT_VALUES)

    db.close()

def check_sql():
    """
    Checking for the presence of a database.
    Проверка на наличие БД.
    """

    if not os.path.exists("TaskTimerDB.db"):
        create_and_migrate()
