import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Task Tracker")

        main_builder = Gtk.Builder()
        main_builder.add_from_file("interface.glade")

        self.window = main_builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

        button = main_builder.get_object("Open")
        button.connect("clicked", self.on_button_clicked)

        exit_button = main_builder.get_object("Exit")
        exit_button.connect("clicked", self.on_exit_button_clicked)

        self.is_window_open = False

    def on_button_clicked(self, widget):
        if not self.is_window_open:
            second_builder = Gtk.Builder()
            second_builder.add_from_file("interface.glade")
            dialog_window = second_builder.get_object("time_window")
            dialog_window.connect("destroy", self.on_dialog_window_closed)
            dialog_window.show_all()
            self.is_window_open = True

    def on_dialog_window_closed(self, widget):
        self.is_window_open = False

    def on_exit_button_clicked(self, widget):
        self.window.destroy()

        
    

win = AppWindow()

Gtk.main()
