#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

# Leaving the original import process as examples and reference
# libAdapta uses its own module name (Adap.ApplicationWindow etc..).
# We would normally import it like this:
# from gi.repository import Adap
# Since libAdapta and libAdwaita use the same class names,
# the same code can work with both libraries, as long as we rename
# the module when importing it

#gi.require_version('Adap', '1')
#from gi.repository import Adap as Adw

# To use libAdwaita, we would import this instead:
# gi.require_version('Adw', '1')
# from gi.repository import Adw

# Additionally, we try to import libAdwaita first since it's has better 
# chances to be installed on the system, otherwise, we try to import 
# libAdapta as a secondary option, you can change the order if needed.

try:
    # Importing libAdwaita first
    gi.require_version('Adw', '1')
    from gi.repository import Adw
except(ValueError, ImportError):
    # Importing libAdapta second
    gi.require_version('Adap', '1')
    from gi.repository import Adap as Adw

class DemoLibadapta1:
    def __init__(self, main_window):
        self.main_window = main_window

    def get_widget(self):
        # Boton para alternar visibilidad de menu lateral
        demo_toggle_btn = Gtk.ToggleButton()
        demo_toggle_btn.set_icon_name("xsi-sidebar-show-symbolic")
        demo_toggle_btn.set_active(True)
        demo_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        demo_header = Adw.HeaderBar()
        demo_header.pack_start(demo_toggle_btn)

        # Create the content page
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.status_page = Adw.StatusPage()
        self.status_page.set_title("Python libAdapta Demo 1")
        self.status_page.set_description("Split navigation view, xapp symbolic icon (xsi) and a calendar widget to feature the accent color.")
        self.status_page.set_icon_name("xsi-auth-face-symbolic")
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.calendar = Gtk.Calendar()
        self.box.append(self.status_page)
        self.box.append(self.calendar)
        self.content_box.append(self.box)

        # For Mint libAdapta demo, uncomment line 152 and comment line 151
        self.content_toolbar = Adw.ToolbarView()
        #content_toolbar.add_top_bar(Adw.HeaderBar())
        self.content_toolbar.add_top_bar(demo_header)
        self.content_toolbar.set_content(self.content_box)
        self.content_page = Adw.NavigationPage(title="Demo 1")

        self.content_page.set_child(self.content_toolbar)

        # Next 3 lines are commented due to being used on the original demo of libAdapta and not here
        #split_view.set_sidebar(sidebar_page)
        #split_view.set_content(content_page)
        
        #self.set_content(split_view)
        return self.content_page