from abc import ABC, abstractmethod
import json

""" 
Clase Padre.
    Alberga todos los metods en comun que tienen las clases hijas: Libro, Usuario y Prestamo.
    Implementa las que son iguales para todos.
"""

try:
    with open("data_lib.json", "r", encoding="utf-8") as archivo:
        data_lib_json = json.load(archivo)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    data_lib_json = {}

try:
    with open("data_usuarios.json", "r", encoding="utf-8") as archivo:
        data_usuarios_json = json.load(archivo)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    data_usuarios_json = {}

try:
    with open("data_prestamos.json", "r", encoding="utf-8") as archivo:
        data_prestamos_json = json.load(archivo)
except (json.decoder.JSONDecodeError, FileNotFoundError):
    data_prestamos_json = {}

class Padre(ABC):
    # Elementos utilizados para el metodo load()
    data_json = None
    tipo = ""
    
    # Todas las clases tienen un ID para identificarce a si mismas
    def __init__(self, id):
        self.id = id
    
    # Le da formato a los diccionarios de los archivos .json
    def write(self):
        diccionario = {
            f"{self.id}" : self.__dict__
        }
        return diccionario
    
    # Guarda los objetos
    @abstractmethod
    def save(self):
        pass
    
    # Carga los objetos del archivo
    def load(self, ID):
        if self.data_json.get(f"{ID}"):
            self.__dict__.update(self.data_json[f"{ID}"])
            print(f"{self.tipo} cargado exitosamente")
            return True
        else:
            print(f"No existe un {self.tipo.lower()} con ese ID")
            return False
    
    # Elimina los objetos del archivo
    @abstractmethod
    def destroy(self):
        pass