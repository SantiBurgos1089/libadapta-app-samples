#!/usr/bin/python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

gi.require_version('Adap', '1')
from gi.repository import Adap as Adw

# Importacion de clases modulares
from sample7_appearance import DemoAppearance

# Application ID
app_id = "xyz.agatinos.app_sample_lightdm_settings"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Informacion general de la ventana de aplicacion e icono opcional
        self.set_title("Login Window")
        self.set_default_size(800, 620)
        self.set_icon_name("lightdm-settings")

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

        content_stack.add_titled_with_icon(
            DemoAppearance(),
            "appearance",
            "Appearance",
            "xsi-appearance-symbolic"
        )

        content_stack.add_titled_with_icon(
            DemoAppearance(),
            "users",
            "Users",
            "xsi-users-symbolic"
        )
        content_stack.add_titled_with_icon(
            DemoAppearance(),
            "settings",
            "Settings",
            "xsi-applications-administration-symbolic"
        )

        # Crear el ViewSwitcherTitle (El título que cambia según la vista y tiene los botones)
        switcher_title = Adw.ViewSwitcher()
        switcher_title.set_stack(content_stack)
        switcher_title.set_policy(Adw.ViewSwitcherPolicy.WIDE)

        # Crear HeaderBar y asignarlo como el widget de título de la barra
        headerbar = Adw.HeaderBar()
        headerbar.set_title_widget(switcher_title)

        # Añadir los widgets al contenedor principal
        main_content_box.append(headerbar)
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