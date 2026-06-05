from clase_Padre import Padre, data_lib_json, data_prestamos_json, data_usuarios_json
from clase_Prestamo import Prestamo 
from api_fecha import obtener_fecha_actual
from datetime import datetime, timedelta
import json
import requests

class Usuario(Padre):
    data_json = data_usuarios_json
    tipo = "Usuario"
    
    """
    Los usuarios pueden ser instanciados sin especificar los valores,
    pero después tendrán que cargar sus valores en un archivo
    """
    def __init__(self, nombre=None, id=None, password=None, estado=False):
        self.nombre = nombre
        super().__init__(id)
        self.__password = password #Cuando se inicia sesion, se necesita una contraseña, y al crear la cuenta tambien.
        self.estado = estado #El parametro estado, es para controlar con que cuenta se esta utilizando la biblioteca.
    
    @property
    def password(self):
        return self.__password
    
    def write(self):
        return {
            f"{self.id}": {
                "nombre": self.nombre,
                "id": self.id,
                "password": self.__password,
                "estado": self.estado
            }
        }
    
    def load(self, ID):
        if data_usuarios_json.get(f"{ID}"):

            self.nombre = data_usuarios_json[f"{ID}"]["nombre"]
            self.id = data_usuarios_json[f"{ID}"]["id"]
            self.__password = data_usuarios_json[f"{ID}"]["password"]
            self.estado = data_usuarios_json[f"{ID}"]["estado"]

            print("Usuario cargado exitosamente")
            return True

        else:
            print("No existe un usuario con ese ID")
            return False

    def save(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion en este usuario")
            return False
        else:
            if data_usuarios_json.get(f"{self.id}"):
                print("Ya existe un usuario con ese ID")
                return False
            else:
                data_usuarios_json.update(self.write())
                with open("data_usuarios.json", "w", encoding="utf-8") as archivo:
                    json.dump(data_usuarios_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                print("Usuario guardado exitosamente")
                return True
        
    def destroy(self):
        if data_usuarios_json.get(f"{self.id}"):
            data_usuarios_json.pop(f"{self.id}")
            with open("data_usuarios.json", "w", encoding="utf-8") as archivo:
                json.dump(data_usuarios_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
            print("Usuario eliminado exitosamente")
        else:
            print("No existe un usuario con ese ID")

    
    #Ahora con este metodo se puede actualizar el usuario en el archivo.
    def update(self):
        if None in self.__dict__.values():
            print("ERROR: Falta informacion en este usuario")
        else:
            if data_usuarios_json.get(f"{self.id}"):
                data_usuarios_json.update(self.write())
                with open("data_usuarios.json", "w", encoding="utf-8") as archivo:
                    json.dump(data_usuarios_json, archivo, indent=4, separators=(", ", " : "), ensure_ascii=False)
                print("Usuario actualizado exitosamente")
            else:
                print("No existe un usuario con ese ID")
    
    #Verifica que no haya otra cuenta que ya este activa.
    def check(self):
        resultado = None
        for x in data_usuarios_json:
            if data_usuarios_json[f"{x}"]["estado"]:
                resultado = data_usuarios_json[f"{x}"]["id"]
        return resultado
    
    #Inicia sesion, solo si: aun no esta iniciado sesion,
    #no haya otra cuenta iniciada sesion,
    #y si la contraseña es correcta.
    def log_in(self, password):
        if self.estado:
            print("Ya iniciaste sesión")
        else:
            if self.check():
                print("Cierra sesión para iniciar sesión en otra cuenta")
            else:
                if password == self.password:
                    self.estado = True
                    print(f"Iniciaste sesión en la cuenta {self.nombre} - {self.id}")
                else:
                    print("¡Contraseña incorrecta!")
    
    #Cierra sesion solo si la cuenta esta activa.
    def log_out(self):
        if self.estado:
            self.estado = False
            print("Sesión cerrada")
        else:
            print("Esta cuenta no esta activa")

    def crear_prestamo(self, id_libro): #metodo para crear pretamos
        if self.estado == False: 
            print("inicia sesion primero") #por si no tiene iniciada sesion
            return 
        try:
            fecha_prestamo = obtener_fecha_actual() #se guarda la fecha actual con la api
            fecha_devolucion = fecha_prestamo + timedelta(days=2)#la fecha actual + 2 dias
            prestamo = Prestamo( #se crea un objeto de prestamo con los datos necesarioa
                id= len(data_prestamos_json)+1, 
                id_libro=id_libro, 
                id_usuario= self.id,
                fecha_prestamo= fecha_prestamo.strftime("%d/%m/%Y"), #se pasan a un tipo string con formato 04/06/2026
                fecha_devolucion= fecha_devolucion.strftime("%d/%m/%Y"),
                vigencia = "Vigente"
                )
            prestamo.save() #se guarda en el archivo y se verifica que el libro si este disponible
        except (
            requests.exceptions.ConnectionError, 
            requests.exceptions.Timeout, 
             requests.exceptions.HTTPError, 
            requests.exceptions.ConnectTimeout, 
            requests.exceptions.MissingSchema
            ):
            print("error al cargar")

        
    def revisar_prestamos(self): #asi el usuario puede revisar sus prestamos
        if self.estado == False: 
            print("inicia sesion primero") #por si no tiene iniciada sesion
            return 
        coincidencias = False
        lista_prestamos = []
        for prestamo in data_prestamos_json.values(): #recorre los prestamos guardados en el json
            if prestamo["id_usuario"] == self.id: #busca coincidencias en el id
                coincidencias = True
                lista_prestamos = lista_prestamos + [prestamo['id']] 
                fecha_limite = datetime.strptime(prestamo['fecha_devolucion'],"%d/%m/%Y")
                if datetime.now().date() > fecha_limite.date():
                    prestamo['vigencia'] = "Expirado"
                    with open("data_prestamos.json", "w", encoding="utf-8") as archivo:
                        json.dump(
                            data_prestamos_json,
                                archivo,
                                indent=4,
                                separators=(", ", " : "),
                                ensure_ascii=False
                                )
        if coincidencias == False: #si no tiene prestamos a su id
            print("No tienes prestamos registrados")
        return lista_prestamos
    
    def devolver_libro(self, id_libro):
        resultado = None
        for x in data_prestamos_json:
            if data_prestamos_json[f"{x}"]["id_libro"] == id_libro:
                resultado = data_prestamos_json[f"{x}"]["id"]
        return resultado
        


