import requests
from datetime import datetime

def obtener_fecha_actual():
        url = "https://timeapi.io/api/Time/current/zone?timeZone=America/Tijuana"

        respuesta = requests.get(url, timeout=10)

        respuesta.raise_for_status()

        datos = respuesta.json()

        fecha = datetime(
            datos["year"],
            datos["month"],
            datos["day"],
            datos["hour"],
            datos["minute"],
            datos["seconds"]
            )
        return fecha