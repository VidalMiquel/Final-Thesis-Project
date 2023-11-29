import json
import os

def filtrar_partidos_por_equipo(ruta_fichero_season_id, nombre_equipo):
    # Obtener la ruta del directorio donde se ejecuta el script
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_output = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))
    ruta_season_id = os.path.join(ruta_output, ruta_fichero_season_id)

    with open(ruta_season_id, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    partidos_seleccionados = {}

    for partido in datos:
        equipo_local = partido['home_team']['home_team_name']
        equipo_visitante = partido['away_team']['away_team_name']

        if nombre_equipo.lower() == equipo_local.lower() or nombre_equipo.lower() == equipo_visitante.lower():
            jornada = partido['match_week']
            partido_id = partido['match_id']

            if jornada not in partidos_seleccionados:
                partidos_seleccionados[jornada] = []

            partidos_seleccionados[jornada].append(partido_id)

    ruta_salida = os.path.join(ruta_output, 'id_matches.json')
    with open(ruta_salida, 'w') as archivo_salida:
        json.dump(partidos_seleccionados, archivo_salida, indent=4)

# Obtener el nombre del equipo ingresado por el usuario por terminal
while True:
    nombre_equipo_usuario = input("Introduce el nombre del equipo: ")

    # Obtener los match_id y guardarlos en el archivo JSON en la carpeta 'TFG/Data/FirstStage'
    filtrar_partidos_por_equipo('season_id.json', nombre_equipo_usuario)

    # Verificar si hay partidos seleccionados leyendo el archivo 'id_matches.json'
    ruta_output = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data', 'FirstStage','Middle_files'))
    ruta_identificadores = os.path.join(ruta_output, 'id_matches.json')
    
    with open(ruta_identificadores, 'r') as archivo_identificadores:
        partidos_seleccionados = json.load(archivo_identificadores)
    
    # Si hay partidos seleccionados, salir del bucle
    if partidos_seleccionados:
        break
    else:
        print(f"No se encontraron partidos para el equipo '{nombre_equipo_usuario}'. Inténtalo de nuevo.")

print("Partidos encontrados y guardados en 'id_matches.json'.")
