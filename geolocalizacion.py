import requests
import urllib.parse

# URLs base de Graphhopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# API Key de Graphhopper integrada
key = "bc4c811d-3b0b-407e-81f5-cc15dcda721c"

while True:
    print("\n--- Planificador de Rutas ---")
    # Textos en español y opción para salir
    origen = input("Ingrese la ciudad de origen (o ingrese 's' o 'salir' para terminar): ")
    if origen.lower() in ['s', 'salir']:
        print("Cerrando el programa de rutas...")
        break

    destino = input("Ingrese la ciudad de destino (o ingrese 's' o 'salir' para terminar): ")
    if destino.lower() in ['s', 'salir']:
        print("Cerrando el programa de rutas...")
        break

    # Geocodificación para el Origen
    url_geocoding_origen = f"{geocode_url}q={urllib.parse.quote(origen)}&key={key}"
    res_origen = requests.get(url_geocoding_origen)
    datos_origen = res_origen.json()

    # Geocodificación para el Destino
    url_geocoding_destino = f"{geocode_url}q={urllib.parse.quote(destino)}&key={key}"
    res_destino = requests.get(url_geocoding_destino)
    datos_destino = res_destino.json()

    if res_origen.status_code == 200 and res_destino.status_code == 200 and len(datos_origen["hits"]) > 0 and len(datos_destino["hits"]) > 0:
        lat_origen = datos_origen["hits"][0]["point"]["lat"]
        lng_origen = datos_origen["hits"][0]["point"]["lng"]
        lat_destino = datos_destino["hits"][0]["point"]["lat"]
        lng_destino = datos_destino["hits"][0]["point"]["lng"]

        # Cálculo de la ruta con locale=es para narrativa en español
        url_ruta = f"{route_url}point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&locale=es&vehicle=car&key={key}"
        res_ruta = requests.get(url_ruta)
        datos_ruta = res_ruta.json()

        if res_ruta.status_code == 200:
            distancia_km = datos_ruta['paths'][0]['distance'] / 1000
            tiempo_min = datos_ruta['paths'][0]['time'] / (1000 * 60)

            print("\nResumen del viaje:")
            # Valores numéricos con máximo de dos decimales
            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"Tiempo estimado: {tiempo_min:.2f} minutos")
            print("\nInstrucciones paso a paso:")

            for instruccion in datos_ruta['paths'][0]['instructions']:
                dist_instruccion = instruccion['distance']
                print(f"- {instruccion['text']} ({dist_instruccion:.2f} m)")
            print("\n" + "="*40)
        else:
            print("Error al calcular la ruta.")
    else:
        print("No se encontraron las ciudades. Verifique los nombres ingresados.")