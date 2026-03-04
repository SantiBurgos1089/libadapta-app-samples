#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class DemoMenu(Gtk.MenuButton):
     def __init__(self, **kwargs):
          super().__init__()

          self.set_icon_name("xsi-open-menu-symbolic")

          demo_popover = Gtk.Popover()

          menu_box = Gtk.Box(
               orientation=Gtk.Orientation.VERTICAL, 
               spacing=6,
               #spacing=12,
               margin_top=6,
               margin_bottom=6,
               margin_start=6,
               margin_end=6
          )

          preferences_button = Gtk.Button()
          preferences_button.set_label("Preferences")
          preferences_button.set_halign(Gtk.Align.START)
          #preferences_button.connect("clicked", self.on_menu_preferences_clicked)

          demo_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

          help_button = Gtk.Button()
          help_button.set_label("Help")
          help_button.set_halign(Gtk.Align.START)
          #help_button.connect("clicked", self.on_menu_help_clicked)

          menu_box.append(preferences_button)
          menu_box.append(demo_separator)
          menu_box.append(help_button)

          demo_popover.set_child(menu_box)

          self.set_popover(demo_popover)