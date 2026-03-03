#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

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

        self.appearance_page = Adw.PreferencesPage()
        self.appearance_page.set_title("Appearance")

        # General section
        self.general_group = Adw.PreferencesGroup()
        self.general_group.set_title("General")

        # Alignment row
        self.general_row = Adw.ActionRow()
        self.general_row.set_title("Alignment")
        self.general_string_list = Gtk.StringList.new(["Left", "Center", "Right"])
        self.general_dropdown = Gtk.DropDown.new(self.general_string_list)
        #self.general_dropdown.set_hexpand(True)
        self.general_row.add_suffix(self.general_dropdown)

        # Add row to section
        self.general_group.add(self.general_row)

        # Add section with all controls to page
        self.appearance_page.add(self.general_group)

        # Background section
        self.background_group = Adw.PreferencesGroup()
        self.background_group.set_title("Background")

        # Background row
        self.background_row = Adw.ActionRow()
        self.background_row.set_title("Background")
        #self.background_row.set_subtitle("Don't select a background from your home directory if it's encrypted or if its permissions are restricted.")
        #self.background_row.set_tooltip_text("Don't select a background from your home directory if it's encrypted or if its permissions are restricted.")
        self.background_preview = Gtk.Image()
        self.background_preview.set_pixel_size(40)
        self.background_preview.set_margin_start(6)
        self.background_preview.set_from_icon_name("xsi-image-missing-symbolic")
        self.background_button = Gtk.Button()
        self.background_button.set_icon_name("xsi-document-open-symbolic")
        self.background_button.set_valign(Gtk.Align.CENTER)
        self.background_row.add_suffix(self.background_button)
        self.background_row.add_suffix(self.background_preview)

        # Add row to section
        self.background_group.add(self.background_row)

        # Background color row
        self.bgcolor_row = Adw.ActionRow()
        self.bgcolor_row.set_title("Background color")
        self.color_dialog = Gtk.ColorDialog()
        self.color_picker = Gtk.ColorDialogButton.new(dialog=self.color_dialog)
        self.bgcolor_row.add_suffix(self.color_picker)

        # Add row to section
        self.background_group.add(self.bgcolor_row)

        # Stretch background row
        self.stretchbg_switch = Adw.SwitchRow()
        self.stretchbg_switch.set_title("Stretch background across multiple monitors")
        self.stretchbg_switch.set_active(False)

        # Add row to section
        self.background_group.add(self.stretchbg_switch)

        # Draw user background row
        self.userbg_switch = Adw.SwitchRow()
        self.userbg_switch.set_title("Draw user backgrounds")
        self.userbg_switch.set_subtitle("When a user is selected, show that user's background.")
        self.userbg_switch.set_active(False)

        # Add row to section
        self.background_group.add(self.userbg_switch)

        # Draw a grid row
        self.gridbg_switch = Adw.SwitchRow()
        self.gridbg_switch.set_title("Draw a grid")
        self.gridbg_switch.set_subtitle("Draw a grid of white dots on top of the background.")
        self.gridbg_switch.set_active(False)

        # Add row to section
        self.background_group.add(self.gridbg_switch)

        # Add section with all controls to page
        self.appearance_page.add(self.background_group)

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
        self.appearance_page.add(self.themes_group)

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
        self.appearance_page.add(self.optional_group)
        
        # Add page with all sections to inherited Gtk.Box
        self.append(self.appearance_page)