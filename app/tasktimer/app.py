#!/usr/bin/env python
import datetime
import os
import sqlite3

import pandas as pd
import pgi

pgi.require_version('Gtk', '3.0')
from models import TimerObject
from peewee import *
from pgi.repository import GLib, Gtk
from utils import check_sql


class AppWindow(Gtk.Window):
    """Класс приложения. Application class."""

    def __init__(self):
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

        self.is_window_open = False
        self.is_paused = False
        self.start_time = None
        self.timer_id = None
        self.seconds_elapsed = 0
        self.pause_start_time = None

    def on_button_clicked_open(self, widget):
        """Открытие окна таймера. Opening the timer window."""

        check_sql()
        if not self.is_window_open:
            second_builder = Gtk.Builder()
            second_builder.add_from_file("../interface/interface.glade")
            self.dialog_window = second_builder.get_object("time_window")
            timer_label = second_builder.get_object("GtkLabel2_timer_window")
            start_time_label = second_builder.get_object("GtkLabel2start_date")
            end_time_label = second_builder.get_object("GtkLabel2end_date")
            button2run = second_builder.get_object("Button2Run")
            button2run.connect(
                "clicked", self.on_button_clicked_run,
                timer_label, start_time_label
            )
            button2pause = second_builder.get_object("Button2Pause")
            button2pause.connect(
                "clicked", self.on_button_clicked_pause,
                timer_label
            )
            enrty2_name = second_builder.get_object("GtkEntry_2_timer_window")
            text2_field = second_builder.get_object("Text2_timer_window")
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
            self.dialog_window.show_all()
            self.is_window_open = True

    def error_message_db(self, widget, message):
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
        error_db_label.set_text(message)
        error_db_button = error_db_builder.get_object("Button3_error_window")
        error_db_button.connect(
            "clicked", self.on_button_clicked_destroy_error_db_msg
        )
        self.dialog_error_db_window.show_all()

    def on_button_clicked_destroy_error_db_msg(self, widget):
        """Разрушение окна ошибки. The destruction of the error window."""

        self.dialog_error_db_window.destroy()

    def on_button_clicked_unload_to_exel(self, widget):
        """Выгрузка данных в exel. Uploading data to exel."""

        if os.path.exists("TaskTimerDB.db"):
            conn = sqlite3.connect('TaskTimerDB.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT *'
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
        else:
            message = 'There is no such file:\nTaskTimerDB.db'
            self.error_message_db(widget, message)

    def on_button_clicked_select(self, widget, text_main_window):
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
                f"End_date: {timer['end_date']}\n"
                f"Amount of time: {timer['amount_of_time']}\n"
                "-----------------\n"
                for timer in timers
            ]
            result_str = "".join(result_lines)
            text_buffer = text_main_window.get_buffer()
            text_buffer.set_text(result_str)
        else:
            message = 'There is no such file:\nTaskTimerDB.db'
            self.error_message_db(widget, message)

    def format_time(self, seconds):
        """Форматирование даты. Formatting the date."""

        return str(datetime.timedelta(seconds=seconds))[:-7]

    def update_time(self, timer_label, start_time):
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

    def on_button_clicked_exit_from_timewin(self, widget):
        """Разрушение окна с таймером. Destruction of the timer window."""

        if self.timer_id:
            GLib.source_remove(self.timer_id)
        self.is_window_open = False
        self.dialog_window.destroy()

    def on_button_clicked_pause(self, widget, timer_label):
        """Пауза таймера. Timer pause."""

        if self.is_paused:
            self.is_paused = False
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
            self.is_paused = True
            if self.timer_id is not None:
                GLib.source_remove(self.timer_id)
            self.timer_id = None
            self.pause_start_time = int((
                datetime.datetime.utcnow() - self.start_time
            ).total_seconds())

    def formatted_date_time(self, input_date):
        """
        Форматирование даты. Вывод в виджет.
        Formatting the date. Output to the widget.
        """

        parsed_date = datetime.datetime.strptime(
            input_date, '%a, %d %b %Y\n%H:%M'
        )
        return parsed_date.strftime('%d/%m/%y %H:%M')

    def on_button_clicked_stop_write_db(
        self, widget, end_time_label,
        timer_label, start_time_label,
        enrty2_name, text2_field
    ):
        """Остановка и запись в БД. Stop and write to the database."""

        end_time_label.set_text(
            datetime.datetime.now().strftime('%a, %d %b %Y\n%H:%M')
        )
        if self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = None

        start_time = datetime.datetime.strptime(
            self.formatted_date_time(start_time_label.get_text()),
            "%d/%m/%y %H:%M"
        )
        end_time = datetime.datetime.strptime(
            self.formatted_date_time(end_time_label.get_text()),
            "%d/%m/%y %H:%M"
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

    def on_button_clicked_run(
        self, widget, timer_label, start_time_label
    ):
        """Запуск таймера. Start the timer."""

        self.is_paused = False
        self.pause_start_time = None
        start_time_label.set_text(
            datetime.datetime.now().strftime('%a, %d %b %Y\n%H:%M')
        )
        self.start_time = datetime.datetime.utcnow()
        self.timer_id = GLib.timeout_add_seconds(
            1, self.update_time, timer_label, self.start_time
        )

    def on_dialog_window_closed(self, widget):
        """Закрытие окна. Closing the window."""

        self.is_window_open = False
        if self.timer_id:
            GLib.source_remove(self.timer_id)

    def destroy_main_window(self, widget):
        """Разрушение окна. The destruction of the window."""

        if self.timer_id:
            GLib.source_remove(self.timer_id)
        self.window.destroy()


win = AppWindow()

Gtk.main()
