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

# Importacion de clases modulares
from sample5_libadapta1 import DemoLibadapta1
from sample5_libadapta2 import DemoLibadapta2

# Application ID
app_id = "xyz.agatinos.app_sample5"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Informacion general de la ventana de aplicacion e icono opcional
        self.set_title("App Sample 5")
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
        # 1. Crear un archivo que llevara la clase a importar (tomar sample5_libadapta1
        #  como muestra)
        # 2. Dentro de dicha clase agregar todos los controles y/o metodos a ocupar segun 
        # convenga
        # 3. Llamar al stack de vistas con el metodo "add_titled_with_icon"
        # 4. Proveer los parametros necesarios para la vista a crear en el siguiente orden:
        # variable_stack_vistas.add_titled_with_icon(
        #       nombre_clase_importada,
        #       "id_de_la_pagina",
        #       "Titulo de la pagina",
        #       "icono_simbolico_xapp_xsi")
        # Repetir los pasos 1 a 4 para cada vista adicional que se desee agregar
        # Adicionalmente, verificar el orden en que se agregan las vistas, ya que este sera 
        # el orden en que se muestren en la interfaz

        # Primer stack de vistas, este se muestra al iniciar la aplicacion
        content_stack.add_titled_with_icon(
            DemoLibadapta1(),
            "demo1",
            "Demo 1",
            "xsi-auth-face-symbolic"
        )

        # Segundo stack de vistas
        content_stack.add_titled_with_icon(
            DemoLibadapta2(),
            "demo2",
            "Demo 2",
            "xsi-avatar-default-symbolic"
        )

        # Crear el ViewSwitcherTitle (El título que cambia según la vista y tiene los botones)
        switcher_title = Adw.ViewSwitcher()
        switcher_title.set_stack(content_stack)
        switcher_title.set_policy(Adw.ViewSwitcherPolicy.WIDE)

        # Crear HeaderBar y asignarlo como el widget de título de la barra
        demo_headerbar = Adw.HeaderBar()
        demo_headerbar.set_title_widget(switcher_title)

        # Añadir los widgets al contenedor principal
        main_content_box.append(demo_headerbar)
        main_content_box.append(content_stack)

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