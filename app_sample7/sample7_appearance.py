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

        # Seccion General
        self.general_group = Adw.PreferencesGroup()
        self.general_group.set_title("General")

        # Alignment row
        self.general_row = Adw.ActionRow()
        self.general_row.set_title("Alignment")

        self.general_string_list = Gtk.StringList.new(["Left", "Center", "Right"])
        self.general_dropdown = Gtk.DropDown.new(self.general_string_list)
        #self.general_dropdown.set_hexpand(True)
        self.general_row.add_suffix(self.general_dropdown)

        self.general_group.add(self.general_row)

        self.general_section.add(self.general_group)

        # Seccion Background
        self.background_group = Adw.PreferencesGroup()
        self.background_group.set_title("Background")

        # Background row
        self.background_row = Adw.ActionRow()
        self.background_row.set_title("Background")

        self.background_entry = Gtk.Entry()
        self.background_entry.set_hexpand(True)
        self.background_entry.set_property("editable", False)
        self.background_row.add_suffix(self.background_entry)

        self.background_group.add(self.background_row)

        # Background color row
        self.bgcolor_row = Adw.ActionRow()
        self.bgcolor_row.set_title("Background color")

        self.color_dialog = Gtk.ColorDialog()
        self.color_picker = Gtk.ColorDialogButton.new(dialog=self.color_dialog)
        self.bgcolor_row.add_suffix(self.color_picker)

        self.background_group.add(self.bgcolor_row)

        # Stretch background row
        self.stretchbg_switch = Adw.SwitchRow()
        self.stretchbg_switch.set_title("Stretch background across multiple monitors")
        self.stretchbg_switch.set_active(False)

        self.background_group.add(self.stretchbg_switch)

        # Draw user background row
        self.userbg_switch = Adw.SwitchRow()
        self.userbg_switch.set_title("Draw user backgrounds")
        self.userbg_switch.set_subtitle("When a user is selected, show that user's background.")
        self.userbg_switch.set_active(False)

        self.background_group.add(self.userbg_switch)

        # Draw a grid row
        self.gridbg_switch = Adw.SwitchRow()
        self.gridbg_switch.set_title("Draw a grid")
        self.gridbg_switch.set_subtitle("Draw a grid of white dots on top of the background.")
        self.gridbg_switch.set_active(False)

        self.background_group.add(self.gridbg_switch)

        self.general_section.add(self.background_group)

        self.append(self.general_section)