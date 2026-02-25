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

# Application ID
app_id = "xyz.agatinos.app_sample2"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Informacion general de la ventana de aplicacion e icono opcional
        self.set_title("App Sample 2")
        self.set_default_size(800, 600)
        self.set_icon_name("application-certificate")

        # Crear el contenedor principal donde iran todos los controles
        main_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_content(main_content_box)

        ## Crear el contenedor principal donde iran todos los controles (version Adw.ToastOverlay)
        #main_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        #self.toast_overlay = Adw.ToastOverlay()
        #self.toast_overlay.set_child(main_content_box)
        #self.set_content(self.toast_overlay)

        # Crear el stack de vistas donde va el contenido de las paginas
        # Permitir que el stack se expanda para llenar la ventana
        content_stack = Adw.ViewStack()
        content_stack.set_vexpand(True)
        content_stack.set_hexpand(True)

        # Crea y añade vistas al ViewStack para mostrar
        # Para definir algo diferente se debe realizar lo siguiente:
        # 1. Construir una funcion con todos los controles y/o metodos a ocupar (tomar 
        # demo_libadapta como muestra)
        # 2. Llamar al stack de vistas con el metodo "add_titled_with_icon"
        # 3. Proveer los parametros necesarios para la vista a crear en el siguiente orden:
        # variable_stack_vistas.add_titled_with_icon(
        #       self.nombre_funcion_a_ocupar(),
        #       "id_de_la_pagina",
        #       "Titulo de la pagina",
        #       "icono_simbolico_gtk")
        # Repetir los pasos 1 a 3 para cada vista adicional que se desee agregar
        # Adicionalmente, verificar el orden en que se agregan las vistas, ya que este sera 
        # el orden en que se muestren en la interfaz

        # Primer stack de vistas, este se muestra al iniciar la aplicacion
        content_stack.add_titled_with_icon(
            self.demo1(),
            "demo1",
            "Demo 1",
            "xsi-auth-face-symbolic"
        )

        # Segundo stack de vistas
        content_stack.add_titled_with_icon(
            self.demo2(),
            "demo2",
            "Demo 2",
            "xsi-avatar-default-symbolic"
        )

        # Crear el ViewSwitcherTitle (El título que cambia según la vista y tiene los botones)
        switcher_title = Adw.ViewSwitcher()
        switcher_title.set_stack(content_stack)
        switcher_title.set_policy(Adw.ViewSwitcherPolicy.WIDE)

        # Crear HeaderBar y asignarlo como el widget de título de la barra
        fel_headerbar = Adw.HeaderBar()
        fel_headerbar.set_title_widget(switcher_title)

        # Añadir los widgets al contenedor principal
        main_content_box.append(fel_headerbar)
        main_content_box.append(content_stack)

    def demo1(self):
        # Create the content page
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        status_page = Adw.StatusPage()
        status_page.set_title("Python libAdapta Demo 1")
        status_page.set_description("Stack navigation view, xapp symbolic icon (xsi) and a calendar widget to feature the accent color.")
        status_page.set_icon_name("xsi-auth-face-symbolic")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        calendar = Gtk.Calendar()
        box.append(status_page)
        box.append(calendar)
        content_box.append(box)

        return content_box

    def demo2(self):
        # Create the content page
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        status_page = Adw.StatusPage()
        status_page.set_title("Python libAdapta Demo 2")
        status_page.set_description("Stack navigation view, xapp symbolic icon (xsi) and a calendar widget to feature the accent color.")
        status_page.set_icon_name("xsi-avatar-default-symbolic")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        calendar = Gtk.Calendar()
        box.append(status_page)
        box.append(calendar)
        content_box.append(box)

        return content_box

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def main():
    app = MyApp(application_id=app_id)
    app.run(None)

if __name__ == "__main__":
    main()