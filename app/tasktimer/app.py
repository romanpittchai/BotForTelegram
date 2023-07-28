#!/usr/bin/env python
import datetime
import os
import sqlite3
from typing import Any, Tuple, Union

import pandas as pd
import pgi

pgi.require_version('Gtk', '3.0')
from peewee import *
from pgi.repository import GLib, Gtk

from constants import (message_error_db, message_error_fields,
                       message_error_timer)
from models import CheckBoxTable, MainCheckBoxTable, TimerObject, db
from utils import check_sql


class AppWindow(Gtk.Window):
    """Класс приложения. Application class."""

    def __init__(self) -> None:
        Gtk.Window.__init__(self, title="Task Tracker")

        main_builder = Gtk.Builder()
        main_builder.add_from_file("../interface/interface.glade")
        label = Gtk.Label(
            label="Task Tracker", angle=25, halign=Gtk.Align.END
        )

        self.window = main_builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

        text_main_window = main_builder.get_object("text_main_window")

        button = main_builder.get_object("Button1Open")
        button.connect("clicked", self.on_button_clicked_open)

        button_select_from_bd = main_builder.get_object(
            "Button1RefreshTheList"
        )
        button_select_from_bd.connect(
            "clicked", self.on_button_clicked_select,
            text_main_window
        )

        exit_button = main_builder.get_object("Button1Exit")
        exit_button.connect("clicked", self.destroy_main_window)

        button_exel = main_builder.get_object("Button1_main_window_unload")
        button_exel.connect(
            "clicked", self.on_button_clicked_unload_to_exel
        )
        self.checkbox_main = main_builder.get_object("main_window_checkbutton")

        if os.path.exists("TaskTimerDB.db"):
            conn = sqlite3.connect('TaskTimerDB.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT checkbox '
                'FROM maincheckboxtable '
                'WHERE id=1'
            )
            results = cursor.fetchall()
            for value in results[0]:
                self.checkbox_main.set_active(value)
            conn.close()
        else:
            self.checkbox_main.set_active(False)

        def error_message_db(self, message_error_db: str) -> None:
            """
            Ошибка отсутствия БД.
            Database absence error.
            """

            error_db_builder = Gtk.Builder()
            error_db_builder.add_from_file("../interface/interface.glade")
            self.dialog_error_db_window = error_db_builder.get_object(
                "Error_window"
            )
            error_db_label = error_db_builder.get_object("Label3_error_window")
            error_db_label.set_text(message_error_db)
            error_db_button = error_db_builder.get_object(
                "Button3_error_window"
            )
            error_db_button.connect(
                "clicked", on_button_clicked_destroy_error_db_msg,
                self.dialog_error_db_window
            )
            checkbox_main = main_builder.get_object("main_window_checkbutton")
            checkbox_main.set_active(False)
            self.dialog_error_db_window.show_all()

        def on_button_clicked_destroy_error_db_msg(
                self, dialog_error_db_window: Gtk.Dialog
        ) -> None:
            """
            Разрушение окна.
            The destruction of the window.
            """

            dialog_error_db_window.destroy()

        def on_checkbutton_main(self, checkbox_main: Gtk.CheckButton) -> None:
            """Обработка чекбаттона. Checkbutton processing."""

            if os.path.exists("TaskTimerDB.db"):
                checkbox_main_value = checkbox_main.get_active()
                checkbox_main.set_active(checkbox_main_value)
                obj_checkbox = MainCheckBoxTable.get(id=1)
                obj_checkbox.checkbox = checkbox_main_value
                obj_checkbox.save()
            else:
                error_message_db(self, message_error_db)

        self.checkbox_main.connect(
            "toggled", on_checkbutton_main, self.checkbox_main
        )

        self.is_window_open: bool = False
        self.is_paused: bool = False
        self.start_time: None = None
        self.timer_id: None = None
        self.seconds_elapsed: int = 0
        self.pause_start_time: None = None

        self.list_of_column: Tuple[str, ...] = (
            "task_name",
            "start_date",
            "end_date",
            "amount_of_time",
            "task_about"
        )

    def on_button_clicked_open(self, widget: Gtk.Widget) -> None:
        """Открытие окна таймера. Opening the timer window."""

        check_sql()
        if not self.is_window_open:
            second_builder = Gtk.Builder()
            second_builder.add_from_file("../interface/interface.glade")
            self.dialog_window = second_builder.get_object("time_window")
            self.dialog_window.connect(
                "delete-event", self.on_time_window_delete_event
            )
            timer_label = second_builder.get_object("GtkLabel2_timer_window")
            start_time_label = second_builder.get_object("GtkLabel2start_date")
            end_time_label = second_builder.get_object("GtkLabel2end_date")
            button2run = second_builder.get_object("Button2Run")
            enrty2_name = second_builder.get_object("GtkEntry_2_timer_window")
            text2_field = second_builder.get_object("Text2_timer_window")
            button2run.connect(
                "clicked", self.on_button_clicked_run,
                timer_label, start_time_label,
                enrty2_name, text2_field
            )
            button2pause = second_builder.get_object("Button2Pause")
            button2pause.connect(
                "clicked", self.on_button_clicked_pause,
                timer_label
            )
            button2stop_write = second_builder.get_object(
                "Button2Stop/WriteDB"
            )
            button2stop_write.connect(
                "clicked", self.on_button_clicked_stop_write_db,
                end_time_label, timer_label, start_time_label,
                enrty2_name, text2_field
            )
            button2exit = second_builder.get_object("Button2Exit")
            button2exit.connect(
                "clicked", self.on_button_clicked_exit_from_timewin
            )
            self.is_window_open: bool = True
            self.dialog_window.show_all()

    def error_message_fields(
            self, widget: Gtk.Widget, message_error: str
    ) -> None:
        error_db_builder2 = Gtk.Builder()
        error_db_builder2.add_from_file("../interface/interface.glade")
        self.dialog_error_fields_window = error_db_builder2.get_object(
            "Error_window2"
        )
        error_db_label2 = error_db_builder2.get_object("Label_error_window2")
        error_db_label2.set_text(message_error)
        error_db_button2 = error_db_builder2.get_object("Button_error_window2")
        error_db_button2.connect(
            "clicked", self.on_button_clicked_destroy_error_fields_msg
        )
        self.dialog_error_fields_window.show_all()

    def error_message_db(
            self, widget: Gtk.Widget, message_error_db: str
    ) -> None:
        """
        Вывод ошибки отсутствия БД.
        Output of the database absence error.
        """

        error_db_builder = Gtk.Builder()
        error_db_builder.add_from_file("../interface/interface.glade")
        self.dialog_error_db_window = error_db_builder.get_object(
            "Error_window"
        )
        error_db_label = error_db_builder.get_object("Label3_error_window")
        error_db_label.set_text(message_error_db)
        error_db_button = error_db_builder.get_object("Button3_error_window")
        error_db_button.connect(
            "clicked", self.on_button_clicked_destroy_error_db_msg
        )
        self.dialog_error_db_window.show_all()

    def on_button_clicked_destroy_error_db_msg(
            self, widget: Gtk.Widget
    ) -> None:
        """
        Разрушение окна ошибки.
        The destruction of the error window.
        """

        self.dialog_error_db_window.destroy()

    def dialog_checkbutton_window_destroy_exit(
            self, widget: Gtk.Widget
    ) -> None:
        """
        Разрушение окна кнопкой Exit.
        Destroying the window with the Exit button.
        """

        self.dialog_checkbutton_window.destroy()

    def dialog_checkbutton_window_destroy(self) -> None:
        """
        Разрушение окна с чебаттонами.
        Запуск функции exel.
        The destruction of the window with chebattons.
        Launching the excel function.
        """

        self.dialog_checkbutton_window.destroy()
        self.exel()

    def on_checkbutton_event(self, widget: Gtk.Widget, event) -> bool:
        """
        Разрушение окна через крестик.
        The destruction of the window through the cross.
        """

        self.dialog_checkbutton_window.destroy()
        return True

    def on_button_clicked_check_button(self, widget: Gtk.Widget) -> None:
        """
        Обработка выбора чекбаттонов.
        Processing the selection of checkbuttons.
        """

        self.value_check_button1 = self.check_button1.get_active()
        self.value_check_button2 = self.check_button2.get_active()
        self.value_check_button3 = self.check_button3.get_active()
        self.value_check_button4 = self.check_button4.get_active()
        self.value_check_button5 = self.check_button5.get_active()

        obj_checkbox = CheckBoxTable.get(id=1)
        obj_checkbox.task_name = self.value_check_button1
        obj_checkbox.start_date = self.value_check_button2
        obj_checkbox.end_date = self.value_check_button3
        obj_checkbox.amount_of_time = self.value_check_button4
        obj_checkbox.task_about = self.value_check_button5
        obj_checkbox.save()
        self.dialog_checkbutton_window_destroy()

    def checkbutton_db_window(self) -> None:
        """
        Обработка значений чекбаттновов в БД.
        Processing the values of checkbuttons in the database.
        """

        checkbutton_builder = Gtk.Builder()
        checkbutton_builder.add_from_file("../interface/interface.glade")

        self.dialog_checkbutton_window = checkbutton_builder.get_object(
            "CheckBox_window"
        )
        self.dialog_checkbutton_window.connect(
            "delete-event", self.on_checkbutton_event
        )
        self.dialog_checkbutton_window.connect(
            "delete-event", self.on_checkbutton_delete_event
        )
        self.check_button1 = checkbutton_builder.get_object(
            "Check_button1"
        )
        self.check_button2 = checkbutton_builder.get_object(
            "Check_button2"
        )
        self.check_button3 = checkbutton_builder.get_object(
            "Check_button3"
        )
        self.check_button4 = checkbutton_builder.get_object(
            "Check_button4"
        )
        self.check_button5 = checkbutton_builder.get_object(
            "Check_button5"
        )
        self.value_check_button: Tuple[Gtk.CheckButton, ...] = (
            self.check_button1,
            self.check_button2,
            self.check_button3,
            self.check_button4,
            self.check_button5,
        )
        if os.path.exists("TaskTimerDB.db"):
            columns_checkbox = ', '.join(self.list_of_column)
            conn = sqlite3.connect('TaskTimerDB.db')
            cursor = conn.cursor()
            cursor.execute(
                f'SELECT {columns_checkbox} '
                'FROM checkboxtable '
                'WHERE id=1'
            )

            results = cursor.fetchall()
            for key, value in enumerate(results[0]):
                self.value_check_button[key].set_active(value)
            conn.close()

            button_check_box = checkbutton_builder.get_object(
                "Button_window3_OK"
            )
            button_check_box.connect(
                "clicked", self.on_button_clicked_check_button,
            )
            button_check_box_exit = checkbutton_builder.get_object(
                "Button_window3_Exit"
            )
            button_check_box_exit.connect(
                "clicked", self.dialog_checkbutton_window_destroy_exit,
            )

        self.dialog_checkbutton_window.show_all()

    def on_checkbutton_delete_event(
            self, widget: Gtk.Widget, event
    ) -> bool:
        """
        Разрушение окна через крестик.
        The destruction of the window through the cross.
        """

        self.dialog_checkbutton_window.destroy()
        return True

    def exel(self) -> None:
        """
        Обработка выгрузки exel-файла.
        Processing of the excel file upload.
        """

        list_columns = []
        columns = ', '.join(self.list_of_column)
        conn = sqlite3.connect('TaskTimerDB.db')
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT {columns} '
            'FROM checkboxtable '
            'WHERE id=1'
        )
        results = cursor.fetchall()
        for key, value in enumerate(results[0]):
            if value == 1:
                list_columns.append(self.list_of_column[key])
        join_list_columns = ', '.join(list_columns)

        conn = sqlite3.connect('TaskTimerDB.db')
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT {join_list_columns} '
            'FROM timerobject'
        )
        results = cursor.fetchall()
        column_names = [
            description[0] for description in cursor.description
        ]
        dataframe = pd.DataFrame(
            results, columns=column_names
        )
        dataframe.to_excel('worksheet.xlsx', index=False)
        conn.close()

    def on_button_clicked_unload_to_exel(self, widget: Gtk.Widget) -> None:
        """Выгрузка данных в exel. Uploading data to exel."""

        if os.path.exists("TaskTimerDB.db"):
            conn = sqlite3.connect('TaskTimerDB.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT checkbox '
                'FROM maincheckboxtable '
                'WHERE id=1'
            )
            results = cursor.fetchall()
            conn.close()

            if results[0][0] == 1:
                self.checkbutton_db_window()
            elif results[0][0] == 0:
                self.exel()
        else:
            self.error_message_db(widget, message_error_db)

    def on_button_clicked_select(
            self, widget: Gtk.Widget, text_main_window: str
    ) -> None:
        """
        Выборка данных и вывод в окно.
        Data sampling and output to the window.
        """

        if os.path.exists("TaskTimerDB.db"):
            timers = TimerObject.select().dicts()
            result_lines = [
                f"Entry number: {timer['id']}\n"
                f"Task name: {timer['task_name']}\n"
                f"Task about: {timer['task_about']}\n"
                f"Start date: {timer['start_date']}\n"
                f"End date: {timer['end_date']}\n"
                f"Amount of time: {timer['amount_of_time']}\n"
                "-----------------\n"
                for timer in timers
            ]
            result_str = "".join(result_lines)
            text_buffer = text_main_window.get_buffer()
            text_buffer.set_text(result_str)
        else:
            self.error_message_db(widget, message_error_db)

    def format_time(self, seconds: int) -> str:
        """Форматирование даты. Formatting the date."""

        return str(datetime.timedelta(seconds=seconds))[:-7]

    def update_time(
            self, timer_label: Gtk.Label, start_time: datetime.datetime
    ) -> bool:
        """Для таймера. For the timer."""

        if not self.is_paused:
            current_time = datetime.datetime.utcnow()
            elapsed_time = current_time - start_time
            timer_label.set_text(
                self.format_time(
                    elapsed_time.total_seconds()
                )
            )
        return True

    def destroy_timer(self) -> None:
        """
        Обработка разрушения таймера.
        Processing the destruction of the timer.
        """

        self.timer_id: None = None
        self.is_paused: bool = False
        self.start_time: None = None
        self.pause_start_time: int = 0

    def on_time_window_delete_event(
            self, widget: Gtk.Widget, event
    ) -> bool:
        """
        Обработка разрушения окна с таймером
        через крестик.
        Processing of window destruction with a timer
        through the cross.
        """

        self.is_window_open: bool = False
        self.dialog_window.destroy()
        self.destroy_timer()
        return True

    def on_button_clicked_exit_from_timewin(self, widget: Gtk.Widget) -> None:
        """Разрушение окна с таймером. Destruction of the timer window."""

        if self.timer_id:
            GLib.source_remove(self.timer_id)
        self.is_window_open: bool = False
        self.destroy_timer()
        self.dialog_window.destroy()

    def on_button_clicked_pause(
            self, widget: Gtk.Widget, timer_label: Gtk.Label
    ) -> None:
        """Пауза таймера. Timer pause."""

        if self.is_paused:
            self.is_paused: bool = False
            self.start_time = (
                datetime.datetime.utcnow() - datetime.timedelta(
                    seconds=self.pause_start_time
                )
            )
            self.timer_id = GLib.timeout_add_seconds(
                1, self.update_time,
                timer_label, self.start_time
            )
        else:
            if not self.timer_id:
                self.error_message_fields(widget, message_error_timer)
            else:
                self.is_paused: bool = True
                if self.timer_id:
                    GLib.source_remove(self.timer_id)
                self.timer_id: None = None
                self.pause_start_time: int = int((
                    datetime.datetime.utcnow() - self.start_time
                ).total_seconds())

    def formatted_date_time(
            self, input_date: Union[str, datetime.datetime]
    ) -> str:
        """
        Форматирование даты. Вывод в виджет.
        Formatting the date. Output to the widget.
        """

        parsed_date = datetime.datetime.strptime(
            input_date, '%a, %d %b %Y\n%H%M%S'
        )
        return parsed_date.strftime('%d/%m/%y %H:%M:%S')

    def on_button_clicked_stop_write_db(
        self, widget: Gtk.Widget, end_time_label: Gtk.Label,
        timer_label: Gtk.Label, start_time_label: Gtk.Label,
        enrty2_name: Any, text2_field: Any
    ) -> None:
        """Остановка и запись в БД. Stop and write to the database."""

        if self.timer_id or (self.is_paused and not self.timer_id):
            end_time_label.set_text(
                datetime.datetime.now().strftime('%a, %d %b %Y\n%H:%M:%S')
            )
            if self.timer_id:
                GLib.source_remove(self.timer_id)
                self.timer_id = None

            start_time = datetime.datetime.strptime(
                self.formatted_date_time(
                    start_time_label.get_text().replace(':', '')
                ),
                "%d/%m/%y %H:%M:%S"
            )
            end_time = datetime.datetime.strptime(
                self.formatted_date_time(
                    end_time_label.get_text().replace(':', '')
                ),
                "%d/%m/%y %H:%M:%S"
            )
            time_label = timer_label.get_text()
            name_entry = enrty2_name.get_text()
            text_note = text2_field.get_buffer().get_text(
                text2_field.get_buffer().get_start_iter(),
                text2_field.get_buffer().get_end_iter(),
                False
            )
            obj_timer = TimerObject(
                task_name=name_entry, start_date=start_time,
                end_date=end_time, amount_of_time=time_label,
                task_about=text_note
            )
            obj_timer.save()
        else:
            self.error_message_fields(widget, message_error_timer)

    def on_button_clicked_destroy_error_fields_msg(
            self, widget: Gtk.Widget
    ) -> None:
        """ Разрушение окна. Destroy the window."""

        self.dialog_error_fields_window.destroy()

    def on_button_clicked_run(
        self, widget: Gtk.Widget, timer_label: Gtk.Label,
        start_time_label: Gtk.Label,
        enrty2_name: Any, text2_field: Any
    ) -> None:
        """Запуск таймера. Start the timer."""

        name_entry = enrty2_name.get_text()
        text_note = text2_field.get_buffer().get_text(
            text2_field.get_buffer().get_start_iter(),
            text2_field.get_buffer().get_end_iter(),
            False
        )
        if name_entry == "" or text_note == "":
            self.error_message_fields(widget, message_error_fields)
        else:
            self.is_paused: bool = False
            self.pause_start_time: None = None
            start_time_label.set_text(
                datetime.datetime.now().strftime('%a, %d %b %Y\n%H:%M:%S')
            )
            self.start_time = datetime.datetime.utcnow()
            self.timer_id = GLib.timeout_add_seconds(
                1, self.update_time, timer_label, self.start_time
            )

    def destroy_main_window(self, widget: Gtk.Widget) -> None:
        """Разрушение окна. The destruction of the window."""

        if self.timer_id:
            GLib.source_remove(self.timer_id)
        self.window.destroy()


win = AppWindow()

Gtk.main()
