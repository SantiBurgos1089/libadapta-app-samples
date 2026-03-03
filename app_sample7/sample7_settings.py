#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

gi.require_version('Adap', '1')
from gi.repository import Adap as Adw

# To use libAdwaita, we would import this instead:
# gi.require_version('Adw', '1')
# from gi.repository import Adw

class DemoSettings(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.settings_page = Adw.PreferencesPage()
        self.settings_page.set_title("Settings")

        # Settings section
        self.settings_group = Adw.PreferencesGroup()
        self.settings_group.set_title("Settings")

        # Numlock activation row
        self.numlock_switch = Adw.SwitchRow()
        self.numlock_switch.set_title("Activate numlock")
        self.numlock_switch.set_subtitle("Please install numlockx to use this option.")
        self.numlock_switch.set_active(False)

        # Add row to section
        self.settings_group.add(self.numlock_switch)

        # HiDPI row
        self.hidpi_row = Adw.ActionRow()
        self.hidpi_row.set_title("HiDPI support")
        self.hidpi_string_list = Gtk.StringList.new(["Auto", "Enable", "Disable"])
        self.hidpi_dropdown = Gtk.DropDown.new(self.hidpi_string_list)
        #self.hidpi_dropdown.set_hexpand(True)
        self.hidpi_row.add_suffix(self.hidpi_dropdown)

        # Add row to section
        self.settings_group.add(self.hidpi_row)

        # Add section with all controls to page
        self.settings_page.add(self.settings_group)

        # Panel indicators section
        self.indicators_group = Adw.PreferencesGroup()
        self.indicators_group.set_title("Panel indicators")

        # Hostname row
        self.hostname_switch = Adw.SwitchRow()
        self.hostname_switch.set_title("Hostname")
        self.hostname_switch.set_subtitle("Show the computer hostname in the panel.")
        self.hostname_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.hostname_switch)

        # Accesibility options row
        self.accesibility_switch = Adw.SwitchRow()
        self.accesibility_switch.set_title("Accessibility options")
        self.accesibility_switch.set_subtitle("Show accessibility options in the panel.")
        self.accesibility_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.accesibility_switch)

        # Battery power row
        self.battery_switch = Adw.SwitchRow()
        self.battery_switch.set_title("Battery power")
        self.battery_switch.set_subtitle("On laptops, show the battery power in the panel.")
        self.battery_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.battery_switch)

        # Keyboard layout row
        self.kblayout_switch = Adw.SwitchRow()
        self.kblayout_switch.set_title("Keyboard layout")
        self.kblayout_switch.set_subtitle("Show the keyboard layout in the panel.")
        self.kblayout_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.kblayout_switch)

        # Quit menu row
        self.quit_menu_switch = Adw.SwitchRow()
        self.quit_menu_switch.set_title("Quit menu")
        self.quit_menu_switch.set_subtitle("Show the quit menu in the panel.")
        self.quit_menu_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.quit_menu_switch)

        # Clock row
        self.clock_switch = Adw.SwitchRow()
        self.clock_switch.set_title("Clock")
        self.clock_switch.set_subtitle("Show a clock in the panel.")
        self.clock_switch.set_active(True)

        # Add row to section
        self.indicators_group.add(self.clock_switch)

        # Clock format row
        self.clock_format_row = Adw.ActionRow()
        self.clock_format_row.set_title("Clock format")
        self.clock_format_row.set_subtitle("See https://www.foragoodstrftime.com for more information on formatting.")
        self.clock_format_entry = Gtk.Entry()
        self.clock_format_entry.set_hexpand(True)
        self.clock_format_entry.set_placeholder_text("%I:%M %p")
        self.clock_format_row.add_suffix(self.clock_format_entry)

        # Add row to section
        self.indicators_group.add(self.clock_format_row)

        # Add section with all controls to page
        self.settings_page.add(self.indicators_group)
        
        # Add page with all sections to inherited Gtk.Box
        self.append(self.settings_page)