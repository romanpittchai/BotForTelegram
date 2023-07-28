from typing import Dict

AMOUNT_CHAR_TO_SLICE: int = 15

TUPLE_OF_DEFAULT_VALUES_MAIN_CHECKBOX: Dict[str, bool] = {
    'checkbox': False
}

TUPLE_OF_DEFAULT_VALUES: Dict[str, bool] = {
    'task_name': True,
    'start_date': True,
    'end_date': True,
    'amount_of_time': True,
    'task_about': True,
}

message_error_db: str = 'There is no such file:\nTaskTimerDB.db'

message_error_fields: str = 'All fields must be filled in'

message_error_timer: str = 'The timer was not started'
