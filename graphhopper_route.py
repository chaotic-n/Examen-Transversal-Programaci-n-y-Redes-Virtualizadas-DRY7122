import requests
import json
import time

API_KEY = "2f1b6f2a-82a3-4eb4-a8bc-f34108291d9b"

def geocode(ciudad):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": ciudad,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "ExamenTransversal/1.0 (test@example.com)"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200 or not response.json():
        print(f"Error: No se encontró la ciudad '{ciudad}' o servicio no disponible.")
        return None
    loc = response.json()[0]
    return f"{loc['lat']},{loc['lon']}"

while True:
    print("\n--- Planificador de Rutas con Geocoding + GraphHopper ---")
    origen = input("Ciudad de origen (o 's' para salir): ")
    if origen.lower() == "s":
        break

    destino = input("Ciudad de destino: ")
    transporte = input("Medio de transporte (car, bike, foot): ").lower()

    if transporte not in ["car", "bike", "foot"]:
        print("Transporte inválido. Usa 'car', 'bike' o 'foot'.")
        continue

    print("Buscando coordenadas de origen...")
    origen_coords = geocode(origen)
    time.sleep(1)

    print("Buscando coordenadas de destino...")
    destino_coords = geocode(destino)
    time.sleep(1)

    if not origen_coords or not destino_coords:
        print("No se pudieron obtener coordenadas, intenta con nombres más específicos (por ejemplo: Santiago, Chile).")
        continue

    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [origen_coords, destino_coords],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error en la petición. Código: {response.status_code}")
        try:
            print("Respuesta de la API:", response.json())
        except Exception:
            print("No se pudo decodificar respuesta.")
        continue

    data = response.json()

    if "paths" not in data or not data["paths"]:
        print("No se encontró ruta para los puntos indicados.")
        continue

    ruta = data["paths"][0]
    distancia_metros = ruta["distance"]
    duracion_segundos = ruta["time"] / 1000

    distancia_km = distancia_metros / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_min = duracion_segundos / 60

    horas = int(duracion_segundos // 3600)
    minutos = int((duracion_segundos % 3600) // 60)
    segundos = int(duracion_segundos % 60)

    print("\n=== Resultado del viaje ===")
    print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Duración aproximada: {horas}h:{minutos:02d}m:{segundos:02d}s\n")

    print("--- Instrucciones del viaje ---")
    for idx, instruccion in enumerate(ruta["instructions"]):
        texto = instruccion["text"]
        distancia_instr = instruccion["distance"] / 1000
        print(f"{idx + 1}. {texto} ({distancia_instr:.2f} km)")