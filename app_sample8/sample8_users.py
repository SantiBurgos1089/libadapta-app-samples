#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

gi.require_version('Adap', '1')
from gi.repository import Adap as Adw

# To use libAdwaita, we would import this instead:
# gi.require_version('Adw', '1')
# from gi.repository import Adw

class DemoUsers(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.users_page = Adw.PreferencesPage()
        self.users_page.set_title("Users")

        # User list section
        self.user_list_group = Adw.PreferencesGroup()
        self.user_list_group.set_title("User list")

        # Manual login row
        self.manual_login_switch = Adw.SwitchRow()
        self.manual_login_switch.set_title("Allow manual login *")
        self.manual_login_switch.set_subtitle("Add an option in the login window to enter a username.")
        self.manual_login_switch.set_active(False)

        # Add row to section
        self.user_list_group.add(self.manual_login_switch)

        # Hide the user list row
        self.hide_users_switch = Adw.SwitchRow()
        self.hide_users_switch.set_title("Hide the user list *")
        self.hide_users_switch.set_subtitle("Hide the list of users in the login window.")
        self.hide_users_switch.set_active(False)

        # Add row to section
        self.user_list_group.add(self.hide_users_switch)

        # Add section with all controls to page
        self.users_page.add(self.user_list_group)

        # Guest session section
        self.guest_session_group = Adw.PreferencesGroup()
        self.guest_session_group.set_title("Guest sessions")

        # Allow guest sessions row
        self.allow_guest_switch = Adw.SwitchRow()
        self.allow_guest_switch.set_title("Allow guest sessions *")
        self.allow_guest_switch.set_subtitle("Allow guests to use the computer without a password. A temporary guest account is created automatically when they log in.")
        self.allow_guest_switch.set_active(False)

        # Add row to section
        self.guest_session_group.add(self.allow_guest_switch)

        # Add section with all controls to page
        self.users_page.add(self.guest_session_group)

        # Automatic login section
        self.automatic_login_group = Adw.PreferencesGroup()
        self.automatic_login_group.set_title("Automatic login")

        # Username row
        self.username_row = Adw.ActionRow()
        self.username_row.set_title("Username *")
        self.username_row.set_subtitle("Warning: Automatic login will fail if the user's home directory is encrypted.")
        self.username_entry = Gtk.Entry()
        self.username_entry.set_hexpand(True)
        self.username_row.add_suffix(self.username_entry)

        # Add row to section
        self.automatic_login_group.add(self.username_row)

        # Delay connection row
        self.delay_connection_row = Adw.ActionRow()
        self.delay_connection_row.set_title("Delay before connection (in seconds) *")
        self.delay_connection_row.set_subtitle("If this option is set the login screen will be shown for this many seconds before the automatic login occurs. Any user activity will cancel the countdown.")
        self.delay_connection_entry = Gtk.Entry()
        self.delay_connection_entry.set_hexpand(True)
        self.delay_connection_row.add_suffix(self.delay_connection_entry)

        # Add row to section
        self.automatic_login_group.add(self.delay_connection_row)

        # Add section with all controls to page
        self.users_page.add(self.automatic_login_group)

        # Add a warning label
        self.warning_label = Gtk.Label()
        self.warning_label.set_label("* These settings require a computer reboot to take effect.")
        
        # Add page with all sections to inherited Gtk.Box
        self.append(self.users_page)
        self.append(self.warning_label)