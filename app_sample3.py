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
app_id = "xyz.agatinos.app_sample3"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Informacion general de la ventana de aplicacion e icono opcional
        self.set_title("App Sample 1")
        self.set_default_size(800, 600)
        self.set_icon_name("application-certificate")

        # Crear overlay split view visible hacia otros metodos por medio de self
        self.split_view = Adw.OverlaySplitView()
        self.split_view.set_max_sidebar_width(260)
        self.split_view.set_show_sidebar(True)

        # Construir el sidebar
        self.sidebar_page = self.sidebar_page()
        self.split_view.set_sidebar(self.sidebar_page)

        # Mostrar un contenido inicial al abrir el programa
        # Para definir algo diferente se debe realizar lo siguiente:
        # 1. Construir una funcion con todos los controles y/o metodos a ocupar (tomar demo_libadapta como muestra)
        # 2. Definir las lineas a ocupar dentro de la funcion sidebar_page (opcional)
        # 3. Asignar a la variable initial_page la funcion de la pagina a ocupar para que esta se muestre al ejecutarse
        initial_page = self.demo_libadapta1()

        self.split_view.set_content(initial_page)
        self.set_content(self.split_view)


    def sidebar_page(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_vexpand(True)
        sidebar_listbox = Gtk.ListBox()
        sidebar_listbox.add_css_class("navigation-sidebar")
        sidebar_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        # Si necesita agregar mas filas, tomar de muestra cada linea y la seccion otro_row
        # ActionRow para una seccion de instrucciones
        instruction_row = Adw.ActionRow()
        instruction_row.set_title("Demo 1")
        instruction_icon = Gtk.Image.new_from_icon_name("xsi-auth-face-symbolic")
        instruction_row.add_prefix(instruction_icon)
        sidebar_listbox.append(instruction_row)

        # ActionRow para la seccion de Serial Monitor
        monitor_row = Adw.ActionRow()
        monitor_row.set_title("Demo 2")
        monitor_icon = Gtk.Image.new_from_icon_name("xsi-avatar-default-symbolic")
        monitor_row.add_prefix(monitor_icon)
        sidebar_listbox.append(monitor_row)

        ## ActionRow para una 3a seccion en adelante
        #otro_row = Adw.ActionRow()
        #otro_row.set_title("Otro row")
        #otro_icon = Gtk.Image.new_from_icon_name("preferences-other-symbolic")
        #otro_row.add_prefix(otro_icon)
        #sidebar_listbox.append(otro_row)

        # Manejo de la navegacion por cada ActionRow definido
        # Si necesita mostrar otras secciones, continuar la sentencia elif y agregar los 
        # ActionRow previamente definidos. Adicionalmente, definir funciones nuevas para 
        # cada seccion o utilizar un menu existente para pruebas
        def on_row_selected(listbox, row):
            if row is instruction_row:
                self.split_view.set_content(self.demo_libadapta1())
            elif row is monitor_row:
                self.split_view.set_content(self.demo_libadapta2())
            #elif row is otro_row:
            #    self.split_view.set_content(self.demo_libadapta())
            #elif row is otro_row:
            #    self.split_view.set_content(self.other_page())

        # Conectando la accion de mostrar el menu en base a la seleccion de la fila
        sidebar_listbox.connect("row-selected", on_row_selected)
        
        # Añadiendo el ListBox creado junto con cada uno de los menus
        sidebar_box.append(sidebar_listbox)

        # Añadiendo la cabecera del menu lateral y las filas del menu
        sidebar_toolbar = Adw.ToolbarView()
        sidebar_toolbar.add_top_bar(Adw.HeaderBar())
        sidebar_toolbar.set_content(sidebar_box)

        self.navigation_sidebar_page = Adw.NavigationPage()
        self.navigation_sidebar_page.set_title("Opciones")
        self.navigation_sidebar_page.set_child(sidebar_toolbar)

        return self.navigation_sidebar_page
    
    def not_found_page(self):
        # Boton para alternar visibilidad de menu lateral
        nf_toggle_btn = Gtk.ToggleButton()
        nf_toggle_btn.set_icon_name("sidebar-show-symbolic")
        nf_toggle_btn.set_active(True)
        nf_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        nf_header = Adw.HeaderBar()
        nf_header.pack_start(nf_toggle_btn)

        nf_content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        nf_status_page = Adw.StatusPage()
        nf_status_page.set_title("Puerto serial no detectado")
        nf_status_page.set_description("No se ha detectado un puerto serie en el equipo, favor de verificar y abrir el programa nuevamente")
        nf_status_page.set_icon_name("action-unavailable-symbolic")

        nf_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        nf_box.append(nf_status_page)

        nf_content_box.append(nf_box)

        nf_toolbar = Adw.ToolbarView()
        nf_toolbar.add_top_bar(nf_header)
        nf_toolbar.set_content(nf_content_box)

        nf_page = Adw.NavigationPage()
        nf_page.set_title("Error RS232")
        nf_page.set_child(nf_toolbar)

        return nf_page

    def demo_libadapta1(self):
        # Boton para alternar visibilidad de menu lateral
        demo_toggle_btn = Gtk.ToggleButton()
        demo_toggle_btn.set_icon_name("xsi-sidebar-show-symbolic")
        demo_toggle_btn.set_active(True)
        demo_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        demo_header = Adw.HeaderBar()
        demo_header.pack_start(demo_toggle_btn)

        # Create the content page
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        status_page = Adw.StatusPage()
        status_page.set_title("Python libAdapta Demo 1")
        status_page.set_description("Split navigation view, xapp symbolic icon (xsi) and a calendar widget to feature the accent color.")
        status_page.set_icon_name("xsi-auth-face-symbolic")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        calendar = Gtk.Calendar()
        box.append(status_page)
        box.append(calendar)
        content_box.append(box)

        # For Mint libAdapta demo, uncomment line 487 and comment line 486
        content_toolbar = Adw.ToolbarView()
        #content_toolbar.add_top_bar(Adw.HeaderBar())
        content_toolbar.add_top_bar(demo_header)
        content_toolbar.set_content(content_box)
        content_page = Adw.NavigationPage(title="Page")

        content_page.set_child(content_toolbar)

        # Next 3 lines are commented due to being used on the original demo of libAdapta and not here
        #split_view.set_sidebar(sidebar_page)
        #split_view.set_content(content_page)
        
        #self.set_content(split_view)
        return content_page
    
    def demo_libadapta2(self):
        # Boton para alternar visibilidad de menu lateral
        demo_toggle_btn = Gtk.ToggleButton()
        demo_toggle_btn.set_icon_name("xsi-sidebar-show-symbolic")
        demo_toggle_btn.set_active(True)
        demo_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        demo_header = Adw.HeaderBar()
        demo_header.pack_start(demo_toggle_btn)

        # Create the content page
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        status_page = Adw.StatusPage()
        status_page.set_title("Python libAdapta Demo 1")
        status_page.set_description("Split navigation view, xapp symbolic icon (xsi) and a calendar widget to feature the accent color.")
        status_page.set_icon_name("xsi-avatar-default-symbolic")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        calendar = Gtk.Calendar()
        box.append(status_page)
        box.append(calendar)
        content_box.append(box)

        # For Mint libAdapta demo, uncomment line 487 and comment line 486
        content_toolbar = Adw.ToolbarView()
        #content_toolbar.add_top_bar(Adw.HeaderBar())
        content_toolbar.add_top_bar(demo_header)
        content_toolbar.set_content(content_box)
        content_page = Adw.NavigationPage(title="Page")

        content_page.set_child(content_toolbar)

        # Next 3 lines are commented due to being used on the original demo of libAdapta and not here
        #split_view.set_sidebar(sidebar_page)
        #split_view.set_content(content_page)
        
        #self.set_content(split_view)
        return content_page

    # Alterna la visibilidad del sidebar y cambia el icono del boton.
    def on_toggle_sidebar(self, button):
        sidebar_visible = button.get_active()
        self.split_view.set_show_sidebar(sidebar_visible)

        if sidebar_visible:
            button.set_icon_name("xsi-sidebar-show-symbolic")
        else:
            button.set_icon_name("xsi-sidebar-show-right-symbolic")

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
