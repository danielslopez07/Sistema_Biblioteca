#Version 3.2 volvi el metodo .write() y .load() en un metodo concreto de la clase Padre.
from clase_Padre import Padre, data_lib_json
import json

"""
Clase libro que puede guardar, cargar y eliminar libros
"""
class Libro(Padre):
    data_json = data_lib_json
    tipo = "Libro"
    """
    Los libros puede ser instanciados sin especificar los valores
    pero despues tendran que cargar sus valores en un archivo
    """
    def __init__(self, titulo=None, autor=None, idioma=None, id=None, estado=True):
        self.titulo = titulo
        self.autor = autor
        self.idioma = idioma
        super().__init__(id)
        self.estado = estado
        
    """
    Guarda el libro en el archivo solamente si no existe un libro con el mismo ID
    y si el libro que se intenta guardar no esta vacio
    """
    def save(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion en este libro")
        else:
            if data_lib_json.get(f"{self.id}"):
                print("Ya existe un libro con ese ID")
            else:
                data_lib_json.update(self.write())
                with open("data_lib.json", "w", encoding="utf-8") as archivo:
                    json.dump(data_lib_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                print("Libro guardado exitosamente")

    """
    Metodo para eliminar un libro del archivo
    solo si ese libro se encuentra guardado en el archivo
    """
    def destroy(self):
        if data_lib_json.get(f"{self.id}"):
            data_lib_json.pop(f"{self.id}")
            with open("data_lib.json", "w", encoding="utf-8") as archivo:
                json.dump(data_lib_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
            print("Libro eliminado exitosamente")
        else:
            print("No existe un libro con ese ID")
        
    """
    Metodo para actualizar los valores de un libro del archivo
    solo si ese libro se encuentra guardado en el archivo
    """
    def update(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion en este libro")
        else:
            if data_lib_json.get(f"{self.id}"):
                data_lib_json.update(self.write())
                with open("data_lib.json", "w", encoding="utf-8") as archivo:
                    json.dump(data_lib_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                print("Libro actualizado exitosamente")
            else:
                print("No existe un libro con ese ID")
    
    """
    Metodo pensado para la clase prestamo
    se utiliza para cambiar el valor del parametro estado
    despues se tendra que ajustar el cambio con el metodo "update"
    """
    def prestamo(self):
        if self.estado:
            self.estado = False
        else:
            self.estado = True
