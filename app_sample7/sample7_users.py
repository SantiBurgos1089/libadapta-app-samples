#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

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

        # Themes section
        self.themes_group = Adw.PreferencesGroup()
        self.themes_group.set_title("Themes")

        # GTK theme row
        self.gtk_theme_row = Adw.ActionRow()
        self.gtk_theme_row.set_title("GTK theme")
        self.gtk_theme_string_list = Gtk.StringList.new(["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"])
        self.gtk_theme_dropdown = Gtk.DropDown.new(self.gtk_theme_string_list)
        #self.gtk_theme_dropdown.set_hexpand(True)
        self.gtk_theme_row.add_suffix(self.gtk_theme_dropdown)

        # Add row to section
        self.themes_group.add(self.gtk_theme_row)

        # Icon theme row
        self.icon_theme_row = Adw.ActionRow()
        self.icon_theme_row.set_title("Icon theme")
        self.icon_theme_string_list = Gtk.StringList.new(["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"])
        self.icon_theme_dropdown = Gtk.DropDown.new(self.icon_theme_string_list)
        #self.icon_theme_dropdown.set_hexpand(True)
        self.icon_theme_row.add_suffix(self.icon_theme_dropdown)

        # Add row to section
        self.themes_group.add(self.icon_theme_row)

        # Mouse pointer row
        self.mouse_pointer_row = Adw.ActionRow()
        self.mouse_pointer_row.set_title("Mouse pointer")
        self.mouse_pointer_string_list = Gtk.StringList.new(["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"])
        self.mouse_pointer_dropdown = Gtk.DropDown.new(self.mouse_pointer_string_list)
        #self.mouse_pointer_dropdown.set_hexpand(True)
        self.mouse_pointer_row.add_suffix(self.mouse_pointer_dropdown)

        # Add row to section
        self.themes_group.add(self.mouse_pointer_row)

        # Mouse pointer size row
        self.pointer_size_row = Adw.ActionRow()
        self.pointer_size_row.set_title("Mouse pointer size")
        self.pointer_size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 5, 50, 1)
        self.pointer_size_scale.set_value(24)
        self.pointer_size_scale.set_hexpand(True)
        self.pointer_size_scale.set_draw_value(True)
        self.pointer_size_row.add_suffix(self.pointer_size_scale)

        # Add row to section
        self.themes_group.add(self.pointer_size_row)

        # Add section with all controls to page
        self.users_page.add(self.themes_group)

        # Optional picture section
        self.optional_group = Adw.PreferencesGroup()
        self.optional_group.set_title("Optional pictures")

        # Other monitors row
        self.other_monitors_row = Adw.ActionRow()
        self.other_monitors_row.set_title("Other monitors")
        self.other_monitors_preview = Gtk.Image()
        self.other_monitors_preview.set_pixel_size(40)
        self.other_monitors_preview.set_margin_start(6)
        self.other_monitors_preview.set_from_icon_name("xsi-image-missing-symbolic")
        self.other_monitors_button = Gtk.Button()
        self.other_monitors_button.set_icon_name("xsi-document-open-symbolic")
        self.other_monitors_button.set_valign(Gtk.Align.CENTER)
        self.other_monitors_row.add_suffix(self.other_monitors_button)
        self.other_monitors_row.add_suffix(self.other_monitors_preview)

        # Add row to section
        self.optional_group.add(self.other_monitors_row)

        # Bottom left row
        self.bottom_row = Adw.ActionRow()
        self.bottom_row.set_title("Bottom left")
        self.bottom_preview = Gtk.Image()
        self.bottom_preview.set_pixel_size(40)
        self.bottom_preview.set_margin_start(6)
        self.bottom_preview.set_from_icon_name("xsi-image-missing-symbolic")
        self.bottom_button = Gtk.Button()
        self.bottom_button.set_icon_name("xsi-document-open-symbolic")
        self.bottom_button.set_valign(Gtk.Align.CENTER)
        self.bottom_row.add_suffix(self.bottom_button)
        self.bottom_row.add_suffix(self.bottom_preview)

        # Add row to section
        self.optional_group.add(self.bottom_row)

        # Add section with all controls to page
        self.users_page.add(self.optional_group)
        
        # Add page with all sections to inherited Gtk.Box
        self.append(self.users_page)