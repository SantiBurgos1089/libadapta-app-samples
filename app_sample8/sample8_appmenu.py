#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

class DemoMenu(Gtk.MenuButton):
     def __init__(self, **kwargs):
          super().__init__()

          self.set_icon_name("xsi-open-menu-symbolic")

          demo_menu = Gio.Menu()

          section1 = Gio.Menu()
          section1.append("Preferences","app.preferences")
          demo_menu.append_section(None, section1)

          section2 = Gio.Menu()
          section2.append("Help","app.help")
          section2.append("About","app.about")
          demo_menu.append_section(None, section2)

          demo_popover = Gtk.PopoverMenu.new_from_model(demo_menu)
          self.set_popover(demo_popover)