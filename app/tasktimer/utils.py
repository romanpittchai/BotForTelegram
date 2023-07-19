import os
from peewee import *

from models import TimerObject, db

def create_and_migrate() -> None:
	"""Создание и миграции в БД."""
	db.create_tables([TimerObject])
	
	
def check_sql() -> None:
    """
    Checking for the presence of a database.
    Проверка на наличие БД.
    """
    if not os.path.exists("TaskTimerDB.db"):
        create_and_migrate()

