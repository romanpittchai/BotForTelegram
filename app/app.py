import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="My Window")

        # Load the interface from the XML file
        builder = Gtk.Builder()
        builder.add_from_file("interface.glade")

        # Get the main window object
        self.window = builder.get_object("main_window")
        print(self.window)
        # Connect the "destroy" event to the Gtk.main_quit() function
        self.window.connect("destroy", Gtk.main_quit)

        # Show the main window
        self.window.show_all()

# Create an instance of the MyWindow class
win = MyWindow()

# Start the Gtk main loop
Gtk.main()
