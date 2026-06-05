import os
from rich.prompt import Prompt, IntPrompt
from menus import mostrar_menu_principal, mostrar_catalogo, mostrar_cuenta, mostrar_configuracion
from clase_Usuario import Usuario
from clase_Libro import Libro
from clase_Prestamo import Prestamo
from clase_Padre import data_usuarios_json

""" 
Archivo principal del sistema de biblioteca.

Una prueba rapida de como estará estructurado el programa,
aun queda mucho por implementar.
"""

programa = True
usuario = Usuario()


os.system("cls")

while programa:
    mostrar_menu_principal()
    
    respuesta = Prompt.ask("Selecciona una opcion:", choices=["1", "2", "3", "4"])
    
    os.system("cls")
    
    if respuesta == "1" and not data_usuarios_json["NoUser"]["admin"]:
            catalogo = True
            usuario.load(usuario.check())
            while catalogo:
                mostrar_catalogo()
                # Cambiamos las opciones: 1. Atrás, 2. Solicitar Préstamo
                respuesta = Prompt.ask("Selecciona una opción:", choices=["1", "2"])
                os.system("cls")
                
                if respuesta == "2":  # Solicitar Préstamo
                    # Regla de negocio: El usuario debe haber iniciado sesión para pedir libros
                    if not usuario.estado:
                        print("ERROR: Debes iniciar sesión en el menú de cuentas primero.")
                        input("\nPresiona Enter para regresar...")
                        os.system("cls")
                        continue
                    
                    mostrar_catalogo()
                    id_libro_prestamo = IntPrompt.ask("Ingresa el ID del libro que deseas pedir prestado")
                    
                    libro = Libro()
                    respuesta = libro.load(id_libro_prestamo)
                    if respuesta and libro.estado:
                        # Instanciamos el préstamo pasándole los datos requeridos
                        # (Deja que tu método save() o la API controlen las fechas internamente)
                        
                        usuario.crear_prestamo(id_libro_prestamo)
                        
                        os.system("cls")
                        # El método save() de Prestamo ya se encarga de validar si el libro está disponible
                        
                        
                        input("\nPresiona Enter para continuar...")
                        os.system("cls")
                    
                    else:
                        os.system("cls")
                        # El método save() de Prestamo ya se encarga de validar si el libro está disponible
                        print("Ese libro no existe o no esta disponible")
                        
                        input("\nPresiona Enter para continuar...")
                        os.system("cls")
                    
                if respuesta == "1":
                    catalogo = False
                    
    if respuesta == "1" and data_usuarios_json["NoUser"]["admin"]:
        os.system("cls")
        print("En el modo desarrollador no puedes entrar en el catalogo")
    
    if respuesta == "2" and not usuario.check() and not data_usuarios_json["NoUser"]["admin"]:
        cuenta = True
        while cuenta:
            mostrar_cuenta()
            respuesta = Prompt.ask("Selecciona una opcion:", choices=["1", "2", "3"])
            os.system("cls")
            
            if respuesta == "2":
                iniciar_sesion = True
                while iniciar_sesion:
                    mostrar_cuenta()
                    respuesta = IntPrompt.ask("Ingresa el ID de tu cuenta")
                    respuesta = usuario.load(respuesta)
                    if respuesta:
                        respuesta = Prompt.ask("Escribe la contraseña")
                        os.system("cls")
                        usuario.log_in(respuesta)
                        usuario.update()
                        cuenta = False
                        iniciar_sesion = False
                    else:
                        respuesta = Prompt.ask("¿Continuar?", choices=["Si", "No"])
                        if respuesta == "No":
                            iniciar_sesion = False
                        os.system("cls")
                                              
            if respuesta == "3":
                crear_cuenta = True
                while crear_cuenta:
                    mostrar_cuenta()
                    nombre = Prompt.ask("Elige un nombre")
                    contrasena = Prompt.ask("Elige una contraseña")
                    iD = IntPrompt.ask("Elige un ID")
                    usuario_new = Usuario(nombre, iD, contrasena, True)
                    respuesta = usuario_new.save()
                    if respuesta == True:
                        respuesta = Prompt.ask("¿Seguro que lo quieres crear?", choices=["Si", "No"])
                        if respuesta == "Si":
                            os.system("cls")
                            usuario.load(iD)
                            cuenta = False
                            crear_cuenta = False
                        if respuesta == "No":
                            usuario_new.destroy()
                            crear_cuenta = False
                            os.system("cls")
                    else:
                        respuesta = Prompt.ask("¿Continuar?", choices=["Si", "No"])
                        if respuesta == "No":
                            crear_cuenta = False
                        os.system("cls")   
                
            if respuesta == "1":
                cuenta = False
    
    if respuesta == "2" and usuario.check() and not data_usuarios_json["NoUser"]["admin"]:
        usuario.load(usuario.check())
        prestamoul = usuario.revisar_prestamos()
        os.system("cls")
        if prestamoul:
            cuenta = True
            os.system("cls")
            while cuenta:
                mostrar_cuenta()
                respuesta = Prompt.ask("Selecciona una opcion:", choices=["1", "2", "3"])
                os.system("cls")
                
                if respuesta == "2":
                    mostrar_cuenta()
                    respuesta = Prompt.ask("¿Seguro que quieres cerrar sesión?", choices=["Si","No"])
                    os.system("cls")
                    if respuesta == "Si":
                        usuario.load(usuario.check())
                        usuario.log_out()
                        usuario.update()
                        cuenta = False
                        
                if respuesta == "3":
                    mostrar_cuenta()
                    devolver = True
                    while devolver:
                        respuesta = IntPrompt.ask("¿Que libro quieres devolver?")
                        libro = Libro()
                        respuesta = libro.load(respuesta)
                        if respuesta:
                            os.system("cls")
                            usuario.load(usuario.check())
                            respuesta = usuario.devolver_libro(libro.id)
                            prestamo = Prestamo()
                            prestamo.load(respuesta)
                            os.system("cls")
                            prestamo.destroy()
                            devolver = False
                            os.system("cls")
                            cuenta = False
                        else:
                            respuesta = Prompt.ask("¿Continuar?", choices=["Si", "No"])
                            if respuesta == "No":
                                os.system("cls")
                                devolver = False
                        
                                                
                if respuesta == "1":
                    cuenta = False
        else:
            cuenta = True
            os.system("cls")
            while cuenta:
                mostrar_cuenta()
                respuesta = Prompt.ask("Selecciona una opcion:", choices=["1", "2"])
                os.system("cls")
                
                if respuesta == "2":
                    mostrar_cuenta()
                    respuesta = Prompt.ask("¿Seguro que quieres cerrar sesión?", choices=["Si","No"])
                    os.system("cls")
                    if respuesta == "Si":
                        usuario.load(usuario.check())
                        usuario.log_out()
                        usuario.update()
                        cuenta = False
                                                                        
                if respuesta == "1":
                    cuenta = False
    
    if respuesta == "2" and data_usuarios_json["NoUser"]["admin"]:
        os.system("cls")
        print("En el modo desarrollador no puedes entrar a tu cuenta")


    if respuesta == "3" and not data_usuarios_json["NoUser"]["admin"]:
        configurar = True
        while configurar:
            mostrar_configuracion()
            respuesta = Prompt.ask("Selecciones una opcion:", choices=["1", "2"])
            os.system("cls")
            if respuesta == "2":
                # modo desarrollador
                mostrar_configuracion()
                print("En el modo desarrollador solamente podras gestionar los libros de la biblioteca")
                respuesta = Prompt.ask("Escribe la contraseña")
                if respuesta == "Admin":
                    print("¡Contraseña correcta!")
                    respuesta = Prompt.ask("¿Seguro que quieres continuar?", choices=["Si", "No"])
                    if respuesta == "Si":
                        usuario.NoUsuario()
                        os.system("cls")
                        configurar = False
                        print("Entraste como desarrollador")
                    else:
                        os.system("cls")
                else:
                    os.system("cls")
                    print("¡Contraseña incorrecta!")
                
                  
                
            if respuesta == "1":
                configurar = False
    
    if respuesta == "3" and data_usuarios_json["NoUser"]["admin"]:
        configurar = True
        while configurar:
            mostrar_configuracion()
            respuesta = Prompt.ask("Selecciones una opcion:", choices=["1", "2", "3", "4", "5"])
            os.system("cls")
            if respuesta == "2":
                # modo desarrollador
                mostrar_configuracion()
                respuesta = Prompt.ask("¿Seguro que quieres continuar?", choices=["Si", "No"])
                if respuesta == "Si":
                    usuario.NoUsuario()
                    os.system("cls")
                    configurar = False
                    print("Saliste del modo desarrollador")
                else:
                    os.system("cls")
            
            if respuesta == "3":
                mostrar_configuracion()
                nombre = Prompt.ask("Escribe el nombre del libro")      
                autor = Prompt.ask("Escribe el nombre del autor")
                idioma = Prompt.ask("Escribe en que idioma esta el libro")
                iD = IntPrompt.ask("Escribe un ID unico para el libro")
                libro = Libro(nombre, autor, idioma, iD)
                respuesta = libro.save()
                if respuesta:
                    respuesta = Prompt.ask("¿Seguro que quieres continuar?", choices=["Si", "No"])
                    if respuesta == "Si":
                        os.system("cls")
                        print("Libro creado exitosamente")
                    else:
                        libro.destroy()
                        os.system("cls")
                else:
                    os.system("cls")
                    print("Ya existe un libro con ese ID")
                    
            if respuesta == "4":
                mostrar_configuracion()
                iD = IntPrompt.ask("Escribe el ID del libro")
                libro = Libro()
                respuesta = libro.load(iD)
                if respuesta and libro.estado:
                    nombre = Prompt.ask("Escribe el nuevo nombre del libro (presiona enter para no modificarlo)", default=libro.titulo)      
                    autor = Prompt.ask("Escribe el nuevo nombre del autor (presiona enter para no modificarlo)", default=libro.autor)
                    idioma = Prompt.ask("Escribe en que idioma esta el libro (presiona enter para no modificarlo)", default=libro.idioma)
                    libro.titulo = nombre
                    libro.autor = autor
                    libro.idioma = idioma
                    respuesta = Prompt.ask("¿Seguro que quieres continuar?", choices=["Si", "No"])
                    if respuesta == "Si":
                        os.system("cls")
                        libro.update()
                        print("Libro modificado exitosamente")
                    else:
                        os.system("cls")
                        print("No se modifico el libro")
                else:
                    os.system("cls")
                    print("No hay un libro con ese ID o no esta disponible")
                    
            if respuesta == "5":
                mostrar_configuracion()
                iD = IntPrompt.ask("Escribe el ID del libro")
                libro = Libro()
                respuesta = libro.load(iD)
                if respuesta and libro.estado:
                    respuesta = Prompt.ask("¿Seguro que quieres continuar?", choices=["Si", "No"])
                    if respuesta == "Si":
                        os.system("cls")
                        libro.destroy()
                        print("Libro eliminado exitosamente")
                    else:
                        os.system("cls")
                        print("No se elimino el libro")
                else:
                    os.system("cls")
                    print("No hay un libro con ese ID o no esta disponible")
                
            if respuesta == "1":
                configurar = False
        
    if respuesta == "4":
        programa = False
        print("Saliendo . . .")

