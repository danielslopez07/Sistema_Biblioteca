from clase_Padre import Padre, data_usuarios_json, data_lib_json, data_prestamos_json
from clase_Libro import Libro
from datetime import datetime, timedelta
import json
import requests


class Prestamo(Padre):
    data_json = data_prestamos_json
    tipo = "Prestamo"
    """ 
    Agregue dos atributos a la clase prestamo, la fecha_prestamo y la fecha_devolucion
    el programa le dara valores cuando el usuario pida un prestamo

    """
    def __init__(self,  id=None, id_libro=None, id_usuario=None, estado=True, fecha_prestamo = None, fecha_devolucion = None, vigencia = None):
        super().__init__(id)
        self.id_libro = id_libro
        self.id_usuario = id_usuario
        self.estado = estado
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.vigencia = vigencia
    """ 
    Metodo .libro()
    Semejante al metodo .prestamo() de la clase Libro, esta hecho para interactuar
    con la otra clase. En este caso para cambiar el valor del atributo "estado"
    de la clase Libro.
    """
    def libro(self):
        libro = Libro()
        libro.load(self.id_libro)
        libro.prestamo()
        libro.update()

    def save(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion para estre prestamo")
        else:
            if data_prestamos_json.get(f"{self.id}"):
                print("Ya existe un prestamo con ese ID")
            else:
                if data_lib_json.get(f"{self.id_libro}"):
                    if data_usuarios_json.get(f"{self.id_usuario}"):
                        if data_lib_json[f"{self.id_libro}"]["estado"] == False:
                            print("El libro no esta disponible")
                        else:
                            self.libro()                      
                            data_prestamos_json.update(self.write())
                            with open("data_prestamos.json", "w", encoding="utf-8") as archivo:
                                json.dump(data_prestamos_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                            print("Prestamo guardado exitosamente")
                    else:
                        print("No existe un usuario con ese ID")
                else:
                    print("No existe un libro con ese ID")

    def destroy(self):
        if data_prestamos_json.get(f"{self.id}"):
            self.libro()
            data_prestamos_json.pop(f"{self.id}")
            with open("data_prestamos.json", "w", encoding="utf-8") as archivo:
                json.dump(data_prestamos_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
            print("Prestamo eliminado exitosamente")
        else:
            print("No existe un prestamo con ese ID")
            
    def update(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion para estre prestamo")
        else:
            if data_prestamos_json.get(f"{self.id}"):
                if data_lib_json.get(f"{self.id_libro}"):
                    if data_usuarios_json.get(f"{self.id_usuario}"):
                        if data_lib_json[f"{self.id_libro}"]["estado"] == False:
                            print("El libro no esta disponible")
                        else:
                            self.libro()                      
                            data_prestamos_json.update(self.write())
                            with open("data_prestamos.json", "w", encoding="utf-8") as archivo:
                                json.dump(data_prestamos_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                            print("Prestamo guardado exitosamente")
                    else:
                        print("No existe un usuario con ese ID")
                else:
                    print("No existe un libro con ese ID")
            else: 
                print("No hay prestamos con ese id")
