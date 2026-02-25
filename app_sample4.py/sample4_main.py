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
from sample4_libadapta import DemoLibadapta

# Application ID
app_id = "xyz.agatinos.app_sample4"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Informacion general de la ventana de aplicacion e icono opcional
        self.set_title("App Sample 4")
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
        initial_page = DemoLibadapta.get_widget(self)

        self.split_view.set_content()
        #self.split_view.set_content(initial_page)
        self.set_content(self.split_view)

    def sidebar_page(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_vexpand(True)

        sidebar_listbox = Gtk.ListBox()
        sidebar_listbox.add_css_class("navigation-sidebar")
        sidebar_listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        # Si necesita agregar mas filas, tomar de muestra cada linea y la seccion otro_row
        # ActionRow para la seccion demostracion 1
        demo1_row = Adw.ActionRow()
        demo1_row.set_title("Demo 1")
        instruction_icon = Gtk.Image.new_from_icon_name("xsi-auth-face-symbolic")
        demo1_row.add_prefix(instruction_icon)
        sidebar_listbox.append(demo1_row)

        ## ActionRow para la seccion demostracion 2
        #demo2_row = Adw.ActionRow()
        #demo2_row.set_title("Demo 2")
        #monitor_icon = Gtk.Image.new_from_icon_name("xsi-avatar-default-symbolic")
        #demo2_row.add_prefix(monitor_icon)
        #sidebar_listbox.append(demo2_row)

        ## ActionRow para la seccion demostracion 3
        #demo3_row = Adw.ActionRow()
        #demo3_row.set_title("Demo 3")
        #monitor_icon = Gtk.Image.new_from_icon_name("xsi-computer-fail-symbolic")
        #demo3_row.add_prefix(monitor_icon)
        #sidebar_listbox.append(demo3_row)

        ## ActionRow para añadir mas secciones en adelante
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
            if row is demo1_row:
                #self.split_view.set_content(self.demo_libadapta1())
                self.split_view.set_content(DemoLibadapta.get_widget(self))
            #elif row is demo2_row:
            #    self.split_view.set_content(self.demo_libadapta2())
            #elif row is demo3_row:
            #    self.split_view.set_content(self.demo3())
            ##elif row is otro_row:
            ##    self.split_view.set_content(self.other_page())

        # Conectando la accion de mostrar el menu en base a la seleccion de la fila
        sidebar_listbox.connect("row-selected", on_row_selected)
        
        # Añadiendo el ListBox creado junto con cada uno de los menus
        sidebar_box.append(sidebar_listbox)

        # Añadiendo la cabecera del menu lateral y las filas del menu
        sidebar_toolbar = Adw.ToolbarView()
        sidebar_toolbar.add_top_bar(Adw.HeaderBar())
        sidebar_toolbar.set_content(sidebar_box)

        self.navigation_sidebar_page = Adw.NavigationPage()
        self.navigation_sidebar_page.set_title("Options")
        self.navigation_sidebar_page.set_child(sidebar_toolbar)

        return self.navigation_sidebar_page
    
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
    #main()
    app = MyApp(application_id=app_id)
    app.run(None)