#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

gi.require_version('Adap', '1')
from gi.repository import Adap as Adw

# To use libAdwaita, we would import this instead:
# gi.require_version('Adw', '1')
# from gi.repository import Adw

class DemoAppearance(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.general_section = Adw.PreferencesPage()
        self.general_section.set_title("General")

        self.general_group = Adw.PreferencesGroup()
        self.general_group.set_title("General")

        self.general_row = Adw.ActionRow()
        self.general_row.set_title("Alignment")

        self.general_string_list = Gtk.StringList.new(["Left", "Center", "Right"])
        self.general_dropdown = Gtk.DropDown.new(self.general_string_list)
        #self.general_dropdown.set_hexpand(True)
        self.general_row.add_suffix(self.general_dropdown)

        self.general_group.add(self.general_row)

        self.general_section.add(self.general_group)

        self.append(self.general_section)