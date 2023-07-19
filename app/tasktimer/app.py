import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Task Tracker")

        main_builder = Gtk.Builder()
        main_builder.add_from_file("../interface/interface.glade")
        label = Gtk.Label(label="Task Tracker", angle=25, halign=Gtk.Align.END)

        self.window = main_builder.get_object("main_window")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

        button = main_builder.get_object("Button1Open")
        button.connect("clicked", self.on_button_clicked)

        exit_button = main_builder.get_object("Button1Exit")
        exit_button.connect("clicked", self.destroy_main_window)

        self.is_window_open = False

    def on_button_clicked(self, widget):
        if not self.is_window_open:
            second_builder = Gtk.Builder()
            second_builder.add_from_file("../interface/interface.glade")
            dialog_window = second_builder.get_object("time_window")
            dialog_window.connect("destroy", self.on_dialog_window_closed)
            dialog_window.show_all()
            self.is_window_open = True

    def on_dialog_window_closed(self, widget):
        self.is_window_open = False

    def destroy_main_window(self, widget):
        self.window.destroy()

        
    

win = AppWindow()

Gtk.main()
