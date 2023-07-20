import datetime
import os
import time

from models import TimerObject, db
from peewee import *


def create_and_migrate():
    """Создание и миграции в БД."""
    db.create_tables([TimerObject])


def check_sql():
    """
    Checking for the presence of a database.
    Проверка на наличие БД.
    """
    if not os.path.exists("TaskTimerDB.db"):
        create_and_migrate()
