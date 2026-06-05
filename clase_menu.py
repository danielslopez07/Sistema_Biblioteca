from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
from clase_Libro import data_lib_json
from clase_Usuario import data_usuarios_json
from clase_Usuario import Usuario
from clase_Prestamo import data_prestamos_json


""" 
Este es el archivo.py donde se guardara todas las funciones que esten
relacionadas con la impresion de pantalla.

El nombre del archivo esta sujeto a cambios, ya que aun no esta definido
si se manejara como una clase o no.

Primera version (V1) aun faltan muchos cambios, pero lo escencial ya esta pavimentado.
"""

consola = Console()

def mostrar_menu_principal():
    titulo = r"""
$$$$$$$\  $$\ $$\       $$\ $$\            $$\                                  
$$  __$$\ \__|$$ |      $$ |\__|           $$ |                                 
$$ |  $$ |$$\ $$$$$$$\  $$ |$$\  $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$$\ $$$$$$\  
$$$$$$$\ |$$ |$$  __$$\ $$ |$$ |$$  __$$\\_$$  _|  $$  __$$\ $$  _____|\____$$\ 
$$  __$$\ $$ |$$ |  $$ |$$ |$$ |$$ /  $$ | $$ |    $$$$$$$$ |$$ /      $$$$$$$ |
$$ |  $$ |$$ |$$ |  $$ |$$ |$$ |$$ |  $$ | $$ |$$\ $$   ____|$$ |     $$  __$$ |
$$$$$$$  |$$ |$$$$$$$  |$$ |$$ |\$$$$$$  | \$$$$  |\$$$$$$$\ \$$$$$$$\\$$$$$$$ |
\_______/ \__|\_______/ \__|\__| \______/   \____/  \_______| \_______|\_______|
    """

    titulo_panel = Panel.fit(
        f"[bold bright_green]{titulo}[/bold bright_green]",
        border_style="green"
    )

    tabla_opciones = Table(border_style="cyan")
    tabla_opciones.add_column("[cyan]Opcion[/]", style="blue", justify="center")
    tabla_opciones.add_column("[cyan]Accion[/]", style="blue")
    tabla_opciones.add_row("1.", "Catalogo")
    tabla_opciones.add_row("2.", "Cuenta")
    tabla_opciones.add_row("3.", "Configurar")
    tabla_opciones.add_row("4.", "Salir")

    opciones_panel = Panel(
        tabla_opciones,
        title="[bold bright_blue]Opciones[/]",
        border_style="blue"
    )

    opciones_panel_centrado = Align.center(opciones_panel)

    grupo = Group(
        titulo_panel,
        opciones_panel_centrado
    )
    
    menu = Panel.fit(grupo, title="[bold bright_yellow]Sistema de biblioteca[/]", border_style="yellow")

    consola.print(menu)

def mostrar_catalogo():    
    titulo_rule = Rule("[bold bright_green]Catalogo[/]", style="green")
    
    tabla_libros = Table(border_style="cyan")
    tabla_libros.add_column("[cyan]ID[/]", style="blue")
    tabla_libros.add_column("[cyan]Titulo[/]", style="blue")
    tabla_libros.add_column("[cyan]Autor[/]", style="blue")
    tabla_libros.add_column("[cyan]Idioma[/]", style="blue")    
    tabla_libros.add_column("[cyan]Estado[/]", style="blue")
    for x in data_lib_json:
        if data_lib_json[f"{x}"]["estado"]:
            estado = "Disponible"
        else:
            estado = "No disponible"
        tabla_libros.add_row(
            f"{data_lib_json[f"{x}"]["id"]}", 
            f"{data_lib_json[f"{x}"]["titulo"]}", 
            f"{data_lib_json[f"{x}"]["autor"]}", 
            f"{data_lib_json[f"{x}"]["idioma"]}", 
            f"{estado}"
        )
        
    libros_panel = Panel(
        tabla_libros,
        title="[bold bright_blue]Libros[/]",
        border_style="blue"
    )
    
    tabla_opciones = Table(border_style="red")
    tabla_opciones.add_column("[red]Opcion[/]", style="red", justify="center")
    tabla_opciones.add_column("[red]Accion[/]", style="red")
    tabla_opciones.add_row("1.", "Atras")
    tabla_opciones.add_row("2.", "Prestamo")
        
    opciones_panel = Panel(
        tabla_opciones,
        title="[bold bright_red]Opciones[/]",
        border_style="red"
    )
        
    opciones_panel_centrado = Align.center(opciones_panel)
    
    grupo = Group(
        titulo_rule,
        libros_panel,
        opciones_panel_centrado
    )
    
    menu = Panel.fit(grupo, title="[bold yellow]Sistema de biblioteca[/]", border_style="yellow")
    
    consola.print(menu)

def mostrar_cuenta():
    usuario = Usuario()
    id = usuario.check()
    if id:
        usuario.load(id)
        prestamoul = usuario.revisar_prestamos()
        if prestamoul:
            titulo = Panel(
                Text(f"{data_usuarios_json[f"{id}"]["nombre"]} - {data_usuarios_json[f"{id}"]["id"]}", justify="center", style="bold bright_green"),
                title="[green]Cuenta[/]",
                border_style="green"
            )
            
            tabla_prestamos = Table(border_style="cyan")
            tabla_prestamos.add_column("[cyan]ID[/]", style="blue")
            tabla_prestamos.add_column("[cyan]Titulo[/]", style="blue")
            tabla_prestamos.add_column("[cyan]Fecha de devolucion[/]", style="blue", justify="center")
            

            for x in prestamoul:
                libro = data_prestamos_json[f"{x}"]["id_libro"]
                tabla_prestamos.add_row(
                    f"{data_lib_json[f"{libro}"]["id"]}",
                    f"{data_lib_json[f"{libro}"]["titulo"]}",
                    f"{data_prestamos_json[f"{x}"]["fecha_devolucion"]} {data_prestamos_json[f"{x}"]["vigencia"]}"
                )
                        
            prestamos_panel = Panel(
                tabla_prestamos,
                title="[bold bright_blue]Prestamos[/]",
                border_style="blue"
            )
            
            tabla_opciones = Table(border_style="red")
            tabla_opciones.add_column("[red]Opcion[/]", style="red", justify="center")
            tabla_opciones.add_column("[red]Accion[/]", style="red")
            tabla_opciones.add_row("1.", "Atras")
            tabla_opciones.add_row("2.", "Cerrar sesión")
            tabla_opciones.add_row("3.", "Devolver libro")
            
            opciones_panel = Panel(
                tabla_opciones,
                title="[bold bright_red]Opciones[/]",
                border_style="red"
            )
            
            opciones_panel_centrado = Align.center(opciones_panel)
            
            grupo = Group(
                titulo,
                prestamos_panel,
                opciones_panel_centrado
            )
            
            menu = Panel.fit(grupo, title="[bold yellow_red]Sistema de biblioteca[/]", border_style="yellow")
            
            consola.print(menu)
        else:
            titulo = Panel(
                Text(f"{data_usuarios_json[f"{id}"]["nombre"]} - {data_usuarios_json[f"{id}"]["id"]}", justify="center", style="bold bright_green"),
                title="[green]Cuenta[/]",
                border_style="green"
            )
            
            rule = Rule("No tienes prestamos", style="blue")
                        
            prestamos_panel = Panel(
                rule,
                title="[bold bright_blue]Prestamos[/]",
                border_style="blue"
            )
            
            tabla_opciones = Table(border_style="red")
            tabla_opciones.add_column("[red]Opcion[/]", style="red", justify="center")
            tabla_opciones.add_column("[red]Accion[/]", style="red")
            tabla_opciones.add_row("1.", "Atras")
            tabla_opciones.add_row("2.", "Cerrar sesión")
            
            opciones_panel = Panel(
                tabla_opciones,
                title="[bold bright_red]Opciones[/]",
                border_style="red"
            )
            
            opciones_panel_centrado = Align.center(opciones_panel)
            
            grupo = Group(
                titulo,
                prestamos_panel,
                opciones_panel_centrado
            )
            
            menu = Panel.fit(grupo, title="[bold yellow_red]Sistema de biblioteca[/]", border_style="yellow")
            
            consola.print(menu)
            
    else:
        titulo = Panel(
            Text(f"Inicia sesión o crea una cuenta", justify="center", style="bold bright_green"),
            title="[green]Cuenta[/]",
            border_style="green"
        )
                
        tabla_opciones = Table(border_style="red")
        tabla_opciones.add_column("[red]Opcion[/]", style="red", justify="center")
        tabla_opciones.add_column("[red]Accion[/]", style="red")
        tabla_opciones.add_row("1.", "Atras")
        tabla_opciones.add_row("2.", "Iniciar sesión")
        tabla_opciones.add_row("3.", "Crear cuenta")
        
        opciones_panel = Panel(
            tabla_opciones,
            title="[bold bright_red]Opciones[/]",
            border_style="red"
        )
        
        opciones_panel_centrado = Align.center(opciones_panel)
        
        grupo = Group(
            titulo,
            opciones_panel_centrado
        )
        
        menu = Panel.fit(grupo, title="[bold yellow_red]Sistema de biblioteca[/]", border_style="yellow")
        
        consola.print(menu)

def mostrar_configuracion():
    if data_usuarios_json["NoUser"]["admin"]:
        titulo = Panel.fit(
            f"[bold bright_green]Configuración del sistema[/bold bright_green]",
            title="[green]Configuración[/]",
            border_style="green"
        )
        
        titulo_centrado = Align.center(titulo)
        
        mensaje = Text(
            """Actualmente esta en modo administrador, por lo que 
no podrá utilizar varias de las funciones de la 
biblioteca, solamente podrá configurar esta misma.""",
            justify="center",
            style="red"
        )

        tabla_opciones = Table(border_style="cyan")
        tabla_opciones.add_column("[cyan]Opcion[/]", style="blue", justify="center")
        tabla_opciones.add_column("[cyan]Accion[/]", style="blue", justify="center")
        tabla_opciones.add_row("1.", "Atras")
        tabla_opciones.add_row("2.", "Salir del modo administrador")

        opciones_panel = Panel(
            tabla_opciones,
            title="[bold bright_blue]Opciones[/]",
            border_style="blue"
        )

        opciones_panel_centrado = Align.center(opciones_panel)

        grupo = Group(
            titulo_centrado,
            mensaje,
            opciones_panel_centrado
        )
        
        menu = Panel.fit(grupo, title="[bright_yellow]Sistema de biblioteca[/]", border_style="yellow")

        consola.print(menu)
    else:
        titulo = Panel.fit(
            f"[bold bright_green]Configuración del sistema[/bold bright_green]",
            title="[green]Configuración[/]",
            border_style="green"
        )
        
        titulo_centrado = Align.center(titulo)
        
        mensaje = Text(
            """¡Atención! Se necesita entrar como 
desarrollador para configurar el sistema""",
        justify="center",
        style="red"
        )

        tabla_opciones = Table(border_style="cyan")
        tabla_opciones.add_column("[cyan]Opcion[/]", style="blue", justify="center")
        tabla_opciones.add_column("[cyan]Accion[/]", style="blue", justify="center")
        tabla_opciones.add_row("1.", "Atras")
        tabla_opciones.add_row("2.", "Entrar como administrador")

        opciones_panel = Panel(
            tabla_opciones,
            title="[bold bright_blue]Opciones[/]",
            border_style="blue"
        )

        opciones_panel_centrado = Align.center(opciones_panel)

        grupo = Group(
            titulo_centrado,
            mensaje,
            opciones_panel_centrado
        )
        
        menu = Panel.fit(grupo, title="[bright_yellow]Sistema de biblioteca[/]", border_style="yellow")

        consola.print(menu)
