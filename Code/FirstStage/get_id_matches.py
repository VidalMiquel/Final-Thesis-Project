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

# Función para leer datos de la temporada desde un archivo JSON
def obtener_chosen_season_data_json(nombre_archivo):
    with open(nombre_archivo, 'r') as file:  # Abre el archivo en modo lectura
        data = json.load(file)  # Carga los datos JSON desde el archivo
    return data

def obtener_parametros(data):
    resultados = data['metadatos']  # Obtiene la lista de resultados
    return resultados[0]['club']# Devuelve el club



def obtener_valor_club():
    try:
        # Obtener la ruta del directorio actual
        ruta_actual = os.path.abspath(os.path.dirname(__file__))
    
        # Definir las rutas de entrada y salida
        ruta_archivo = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files', 'chosen_season_data.json'))

        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no fue encontrado.")

        # Leer el archivo JSON
        with open(ruta_archivo, 'r') as file:
            data = json.load(file)

            # Obtener el valor de 'club' del archivo JSON
            club = data['metadatos']['club']
            return club

    except FileNotFoundError as e:
        return str(e)
    except KeyError:
        return "El valor 'club' no está presente en el archivo JSON."

def main():
    # Llamar a la función para obtener el valor de 'club'
    valor_club = obtener_valor_club()
    # Filtrar los partidos del equipo ingresado y guardar los IDs en un archivo JSON
    filtrar_partidos_por_equipo('season_id.json', valor_club)
    # Imprimir el valor de 'club' obtenido del archivo JSON
    print(f"Valor de 'club' obtenido: {valor_club}")

if __name__ == "__main__":
    main()
