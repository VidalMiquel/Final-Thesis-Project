import json
import os


def filtrar_partidos_por_equipo(ruta_fichero_season_id, nombre_equipo):
    # Obtener la ruta del directorio donde se ejecuta el script
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_output = os.path.abspath(os.path.join(
        ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))
    # Ruta del archivo de la temporada
    ruta_season_id = os.path.join(ruta_output, ruta_fichero_season_id)

    # Abrir el archivo JSON que contiene los datos de la temporada
    with open(ruta_season_id, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)  # Cargar los datos JSON

    # Diccionario para almacenar los partidos seleccionados por el equipo
    partidos_seleccionados = {}

    # Iterar a través de los datos para filtrar los partidos del equipo proporcionado por el usuario
    for partido in datos:
        equipo_local = partido['home_team']['home_team_name']
        equipo_visitante = partido['away_team']['away_team_name']

        # Verificar si el nombre del equipo coincide con el equipo local o visitante del partido
        if nombre_equipo.lower() == equipo_local.lower() or nombre_equipo.lower() == equipo_visitante.lower():
            # Obtener el número de jornada del partido
            jornada = partido['match_week']
            partido_id = partido['match_id']  # Obtener el ID del partido

            if jornada not in partidos_seleccionados:
                # Inicializar la lista de partidos si es la primera vez que se encuentra esa jornada
                partidos_seleccionados[jornada] = []

            # Agregar el ID del partido a la lista de partidos seleccionados para esa jornada
            partidos_seleccionados[jornada].append(partido_id)

    # Ruta para guardar el archivo de partidos seleccionados
    ruta_salida = os.path.join(ruta_output, 'id_matches.json')

    # Escribir los partidos seleccionados en un archivo JSON
    with open(ruta_salida, 'w') as archivo_salida:
        # Guardar los datos en el archivo JSON con formato
        json.dump(partidos_seleccionados, archivo_salida, indent=4)


# Obtener el nombre del equipo ingresado por el usuario por terminal
while True:
    nombre_equipo_usuario = input("Introduce el nombre del equipo: ")

    # Filtrar los partidos del equipo ingresado y guardar los IDs en un archivo JSON
    filtrar_partidos_por_equipo('season_id.json', nombre_equipo_usuario)

    # Verificar si se encontraron partidos leyendo el archivo 'id_matches.json'
    ruta_output = os.path.abspath(os.path.join(os.path.dirname(
        __file__), '..', '..', 'Data', 'FirstStage', 'Middle_files'))
    ruta_identificadores = os.path.join(ruta_output, 'id_matches.json')

    with open(ruta_identificadores, 'r') as archivo_identificadores:
        partidos_seleccionados = json.load(archivo_identificadores)

    # Si se encuentran partidos, salir del bucle
    if partidos_seleccionados:
        break
    else:
        print(f"No se encontraron partidos para el equipo '{ nombre_equipo_usuario}'. Inténtalo de nuevo.")

print("Partidos encontrados y guardados en 'id_matches.json'.")
