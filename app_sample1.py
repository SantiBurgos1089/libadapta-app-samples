#!/usr/bin/python3

import gi
import os
import re
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

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
app_id = "com.propladi.GtkSerialOperations"

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Operaciones RS232")
        self.set_default_size(800, 600)
        self.set_icon_name("application-x-firmware")

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
        initial_page = self.demo_libadapta()

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
        instruction_row.set_title("Instrucciones")
        instruction_icon = Gtk.Image.new_from_icon_name("x-office-address-book-symbolic")
        instruction_row.add_prefix(instruction_icon)
        sidebar_listbox.append(instruction_row)

        # ActionRow para la seccion de Serial Monitor
        monitor_row = Adw.ActionRow()
        monitor_row.set_title("Serial Monitor")
        monitor_icon = Gtk.Image.new_from_icon_name("network-receive-symbolic")
        monitor_row.add_prefix(monitor_icon)
        sidebar_listbox.append(monitor_row)

        ## ActionRow para la seccion de Websocket
        #ws_row = Adw.ActionRow()
        #ws_row.set_title("Serial Websocket")
        #ws_icon = Gtk.Image.new_from_icon_name("network-wired-symbolic")
        #ws_row.add_prefix(ws_icon)
        #sidebar_listbox.append(ws_row)

        ## ActionRow para una 3a seccion en adelante
        #otro_row = Adw.ActionRow()
        #otro_row.set_title("Otro row")
        #otro_icon = Gtk.Image.new_from_icon_name("preferences-other-symbolic")
        #otro_row.add_prefix(otro_icon)
        #sidebar_listbox.append(otro_row)

        # Manejo de la navegacion por cada ActionRow definido
        # Si necesita mostrar otras secciones, continuar la sentencia elif y agregar los ActionRow previamente definidos
        # Adicionalmente, definir funciones nuevas para cada seccion o utilizar un menu existente para pruebas
        def on_row_selected(listbox, row):
            if row is instruction_row:
                self.split_view.set_content(self.demo_libadapta())
            elif row is monitor_row:
                self.split_view.set_content(self.serial_monitor_page())
            #elif row is ws_row:
            #    self.split_view.set_content(self.websocket_page())
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
    

    def instructions_page(self):
        # Boton para alternar visibilidad de menu lateral
        self.ip_toggle_btn = Gtk.ToggleButton()
        self.ip_toggle_btn.set_icon_name("sidebar-show-symbolic")
        self.ip_toggle_btn.set_active(True)
        self.ip_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        self.ip_header = Adw.HeaderBar()
        self.ip_header.pack_start(self.ip_toggle_btn)

        # Seccion central donde iran todas las subsecciones correspondientes
        self.ip_central_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.ip_central_box.set_hexpand(True)
        self.ip_central_box.set_vexpand(True)

        # Seccion de contenido donde ira cada subseccion definida
        self.ip_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.ip_content_box.set_hexpand(True)
        self.ip_content_box.set_vexpand(True)

        # Creando la subseccion izquierda junto con sus controles
        # Subseccion izquierda
        self.ip_left_section_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.ip_left_section_box.set_hexpand(True)
        self.ip_left_section_box.set_vexpand(True)

        # Pagina de Status para mostrar instrucciones de la seccion "Serial Monitor"
        ip_left_status_page = Adw.StatusPage()
        ip_left_status_page.set_title("Seccion Serial Monitor")
        ip_left_status_page.set_description("Esta seccion permite realizar pruebas generales con el puerto serial RS232. \n" \
        "Puede configurar los parametros de lectura de su dispositivo serial segun el manual de su fabricante. \n" \
        "Una vez colocado los parametros, hacer clic en el boton de \"Iniciar lectura\" para comenzar a verificar datos")
        ip_left_status_page.set_icon_name("application-x-firmware")

        self.ip_left_section_box.append(ip_left_status_page)

        # Creando la subseccion derecha junto con sus controles
        # Subseccion derecha
        self.ip_right_section_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.ip_right_section_box.set_hexpand(True)
        self.ip_right_section_box.set_vexpand(True)

        # Pagina de Status para mostrar instrucciones de la seccion "Websocket Serial"
        ip_right_status_page = Adw.StatusPage()
        ip_right_status_page.set_title("Seccion Serial Websocket")
        ip_right_status_page.set_description("Esta seccion permite leer informacion de un puerto serial RS232 y enviarlo a un sitio web. \n" \
        "Puede configurar los parametros de lectura de su dispositivo serial segun el manual de su fabricante, \n" \
        "adicionalmente, debe configurar en su sitio web la direccion IP y el puerto ocupado segun su documentacion o manejo de dicho sitio \n" \
        "Una vez colocado los parametros, hacer clic en el boton de \"Iniciar WebSocket\" para comenzar a leer y enviar los datos respectivos")
        ip_right_status_page.set_icon_name("application-x-firmware")

        self.ip_right_section_box.append(ip_right_status_page)

        # Añadiendo las subsecciones izquierda y derecha a la seccion de contenido
        self.ip_content_box.append(self.ip_left_section_box)
        self.ip_content_box.append(self.ip_right_section_box)

        # Añadiendo la seccion de contenido al contenido principal
        self.ip_central_box.append(self.ip_content_box)

        # Añadiendo la cabecera de la pagina de instrucciones y la pagina de navegacion
        self.ip_toolbar = Adw.ToolbarView()
        self.ip_toolbar.add_top_bar(self.ip_header)
        self.ip_toolbar.set_content(self.ip_central_box)

        self.ip_page = Adw.NavigationPage()
        self.ip_page.set_title("Instrucciones")
        self.ip_page.set_child(self.ip_toolbar)

        return self.ip_page


    def serial_monitor_page(self):
        # Boton para alternar visibilidad de menu lateral
        self.sm_toggle_btn = Gtk.ToggleButton()
        self.sm_toggle_btn.set_icon_name("sidebar-show-symbolic")
        self.sm_toggle_btn.set_active(True)
        self.sm_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        self.sm_header = Adw.HeaderBar()
        self.sm_header.pack_start(self.sm_toggle_btn)

        # Seccion central donde iran todas las subsecciones correspondientes
        self.sm_central_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.sm_central_box.set_hexpand(True)
        self.sm_central_box.set_vexpand(True)

        # Seccion de contenido donde ira cada subseccion definida
        self.sm_content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.sm_content_box.set_hexpand(True)
        self.sm_content_box.set_vexpand(True)

        # Creando la subseccion izquierda junto con sus controles
        # Subseccion izquierda
        self.sm_left_section_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.sm_left_section_box.set_hexpand(True)
        self.sm_left_section_box.set_vexpand(True)

        # TextView para lectura de datos
        self.sm_data_textview = Gtk.TextView()
        self.sm_data_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.sm_data_textview.set_editable(False)
        self.sm_data_textview.set_hexpand(True)
        self.sm_data_textview.set_vexpand(True)
        
        # ScrolledWindow para que el TextView pueda mostrar barras de desplazamiento para mostrar los datos
        self.sm_scroll_textview = Gtk.ScrolledWindow()
        self.sm_scroll_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.sm_scroll_textview.set_hexpand(True)
        self.sm_scroll_textview.set_vexpand(True)
        self.sm_scroll_textview.set_child(self.sm_data_textview)

        # Label
        self.data_label = Gtk.Label()
        self.data_label.set_label("Lectura")

        # Añadiendo controles a la subseccion
        self.sm_left_section_box.append(self.data_label)
        self.sm_left_section_box.append(self.sm_scroll_textview)

        # Creando la subseccion derecha junto con sus controles
        # Subseccion derecha
        self.sm_right_section_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.sm_right_section_box.set_hexpand(True)
        self.sm_right_section_box.set_vexpand(True)

        # Label y DropDown para puertos disponibles
        self.sm_ports_label = Gtk.Label()
        self.sm_ports_label.set_label("Puertos disponibles")
        self.sm_port_string_list = Gtk.StringList.new()
        # Busco por puertos seriales, estos aparece como "/dev/ttyUSB0" o similares
        for port in os.listdir('/dev'):
            if re.match(r'^ttyUSB\d+$', port):
                self.sm_port_string_list.append(f"/dev/{port}")
        self.sm_port_dropdown = Gtk.DropDown.new(self.sm_port_string_list)

        # Label y DropDown para baudrate
        # Se deja 9600 por defecto por ser el valor mas utilizado en equipos
        self.sm_baudrate_label = Gtk.Label()
        self.sm_baudrate_label.set_label("Baudrate")
        self.sm_baudrate_string_list = Gtk.StringList.new(["100", "300", "600", "1200", "2400", "4800", "9600", "14400",
                     "19200", "38400", "56000", "57600", "115200", "128000", "256000"])
        self.sm_baudrate_dropdown = Gtk.DropDown.new(self.sm_baudrate_string_list)
        self.sm_baudrate_dropdown.set_selected(6)

        # Label y DropDown para data bits
        self.sm_databits_label = Gtk.Label()
        self.sm_databits_label.set_label("Data Bits")
        self.sm_databits_string_list = Gtk.StringList.new(["5", "6", "7", "8"])
        self.sm_databits_dropdown = Gtk.DropDown.new(self.sm_databits_string_list)

        # Label y DropDown para paridad
        # Se deja "Ninguna" por defecto por ser el valor mas utilizado en equipos
        self.sm_parity_label = Gtk.Label()
        self.sm_parity_label.set_label("Paridad")
        self.sm_parity_string_list = Gtk.StringList.new(["Ninguna", "Par", "Impar", "Espacio", "Marca"])
        self.sm_parity_dropdown = Gtk.DropDown.new(self.sm_parity_string_list)
        self.sm_parity_dropdown.set_selected(0)

        # Label y DropDown para bits de parada
        self.sm_stopbits_label = Gtk.Label()
        self.sm_stopbits_label.set_label("Bit parada")
        self.sm_stopbits_string_list = Gtk.StringList.new(["1", "1.5", "2"])
        self.sm_stopbits_dropdown = Gtk.DropDown.new(self.sm_stopbits_string_list)

        # Label y DropDown para control de flujo
        self.sm_flowcontrol_label = Gtk.Label()
        self.sm_flowcontrol_label.set_label("Control de flujo")
        self.sm_flowcontrol_string_list = Gtk.StringList.new(["Ninguno", "Hardware", "Xon/Xoff"])
        self.sm_flowcontrol_dropdown = Gtk.DropDown.new(self.sm_flowcontrol_string_list)

        # Boton para ejecutar el log de datos
        self.sm_log_data_button = Gtk.Button()
        self.sm_log_data_button.set_icon_name("media-playback-start-symbolic")
        self.sm_log_data_button.set_label("Iniciar Log")
        self.sm_log_data_button.connect("clicked", self.sm_log_data)
        
        # Boton para limpiar TextView
        self.sm_clear_data_button = Gtk.Button()
        self.sm_clear_data_button.set_icon_name("edit-clear-symbolic")
        self.sm_clear_data_button.set_label("Limpiar lectura")
        self.sm_clear_data_button.connect("clicked", self.sm_clear_data)

        # Añadiendo controles a la subseccion
        self.sm_right_section_box.append(self.sm_ports_label)
        self.sm_right_section_box.append(self.sm_port_dropdown)
        self.sm_right_section_box.append(self.sm_baudrate_label)
        self.sm_right_section_box.append(self.sm_baudrate_dropdown)
        self.sm_right_section_box.append(self.sm_databits_label)
        self.sm_right_section_box.append(self.sm_databits_dropdown)
        self.sm_right_section_box.append(self.sm_parity_label)
        self.sm_right_section_box.append(self.sm_parity_dropdown)
        self.sm_right_section_box.append(self.sm_stopbits_label)
        self.sm_right_section_box.append(self.sm_stopbits_dropdown)
        self.sm_right_section_box.append(self.sm_flowcontrol_label)
        self.sm_right_section_box.append(self.sm_flowcontrol_dropdown)
        self.sm_right_section_box.append(self.sm_log_data_button)
        self.sm_right_section_box.append(self.sm_clear_data_button)

        # Añadiendo las subsecciones izquierda y derecha a la seccion de contenido
        self.sm_content_box.append(self.sm_left_section_box)
        self.sm_content_box.append(self.sm_right_section_box)

        # Añadiendo la seccion de contenido al contenido principal
        self.sm_central_box.append(self.sm_content_box)

        # Añadiendo la cabecera de la pagina de serial monitor y la pagina de navegacion
        self.sm_toolbar = Adw.ToolbarView()
        self.sm_toolbar.add_top_bar(self.sm_header)
        self.sm_toolbar.set_content(self.sm_central_box)

        self.sm_page = Adw.NavigationPage()
        self.sm_page.set_title("Monitor RS232")
        self.sm_page.set_child(self.sm_toolbar)

        return self.sm_page

    
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

    
    def demo_libadapta(self):
        # Boton para alternar visibilidad de menu lateral
        demo_toggle_btn = Gtk.ToggleButton()
        demo_toggle_btn.set_icon_name("sidebar-show-symbolic")
        demo_toggle_btn.set_active(True)
        demo_toggle_btn.connect("toggled", self.on_toggle_sidebar)

        # HeaderBar libAdapta/libAdwaita con boton de visibilidad
        demo_header = Adw.HeaderBar()
        demo_header.pack_start(demo_toggle_btn)

        # Create the content page
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        status_page = Adw.StatusPage()
        status_page.set_title("Python libAdapta Example")
        status_page.set_description("Split navigation view, symbolic icon and a calendar widget to feature the accent color.")
        status_page.set_icon_name("document-open-recent-symbolic")
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
            button.set_icon_name("sidebar-show-symbolic")
        else:
            button.set_icon_name("sidebar-hide-symbolic-rtl")

    def sm_log_data(self, button):
        if not self.logging:
            self.logging = True
            button.set_label("Detener Log")
            self.serialSettings.send_notifications("Estado", "Iniciando log...")

            info_ports = self.sm_port_dropdown.get_selected()
            info_ports = self.sm_port_string_list.get_string(info_ports)

            info_baudrate = self.sm_baudrate_dropdown.get_selected()
            info_baudrate = self.sm_baudrate_string_list.get_string(info_baudrate)

            info_databits = self.sm_databits_dropdown.get_selected()
            info_databits = self.sm_databits_string_list.get_string(info_databits)

            info_parity = self.sm_parity_dropdown.get_selected()
            info_parity = self.sm_parity_string_list.get_string(info_parity)

            info_stopbits = self.sm_stopbits_dropdown.get_selected()
            info_stopbits = self.sm_stopbits_string_list.get_string(info_stopbits)

            info_flowcontrol = self.sm_flowcontrol_dropdown.get_selected()
            info_flowcontrol = self.sm_flowcontrol_string_list.get_string(info_flowcontrol)

            self.serialMonitor.logs_serial_monitor(self.show_in_textview, info_ports, info_baudrate, info_databits, 
                                               info_parity, info_stopbits, info_flowcontrol)
            
            # Seccion para pruebas de impresion de informacion obtenida en los formularios en consola
            # Descomentar seccion y comentar llamada a logs_serial_monitor para pruebas
            # Comentar seccion y descomentar llamada a logs_serial_monitor para produccion
            """ print(
                info_ports, "\n",
                info_baudrate, "\n",
                info_databits, "\n",
                info_parity, "\n",
                info_stopbits, "\n",
                info_flowcontrol, "\n"
            ) """
            
        else:
            self.logging = False
            button.set_label("Iniciar Log")
            self.serialMonitor.stop_read_serial()
            self.serialSettings.send_notifications("Estado", "Deteniendo log")


    def sm_clear_data(self, widget):
        buffer = self.sm_data_textview.get_buffer()
        buffer.set_text("")
        self.serialSettings.send_notifications("Estado", "Limpiando datos")

    def show_in_textview(self, text):
        buffer = self.sm_data_textview.get_buffer()
        buffer.insert(buffer.get_end_iter(), text + "\n")

    def ws_log_data(self):
        pass


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
