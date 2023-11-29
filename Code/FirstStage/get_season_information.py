import json
import urllib.request
import os

# Función para leer un archivo JSON desde una URL
def leer_json_desde_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data  # Devolver el contenido del archivo JSON
    except Exception as e:
        print(f'Error al leer el archivo desde la URL: {e}')
        return None

# Función para buscar correspondencia en los datos
def buscar_correspondencia(data, competition_name, competition_gender, season_name):
    resultados = []
    for competition in data:
        if (competition['competition_name'] == competition_name and
            competition['competition_gender'] == competition_gender):
                if competition['season_name'] == season_name:
                    resultados.append({
                        'competition_id': competition['competition_id'],
                        'season_id': competition['season_id']
                    })
    return resultados

# Función para obtener la ruta de salida
def obtener_ruta_output():
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_output = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))
    return ruta_output

# Función para guardar datos con metadatos en un archivo JSON en la carpeta de salida
def guardar_datos_json(resultados_busqueda, competition_name, competition_gender, season_name):
    nombre_archivo = 'chosen_season_data.json'
    ruta_output = obtener_ruta_output()
    ruta_archivo_completa = os.path.join(ruta_output, nombre_archivo)

    try:
        if not os.path.exists(ruta_output):
            os.makedirs(ruta_output)

        # Crear un diccionario para almacenar los metadatos
        metadatos = {
            'metadatos': {
                'competition_name': competition_name,
                'competition_gender': competition_gender,
                'season_name': season_name
            },
            'resultados': resultados_busqueda
        }

        with open(ruta_archivo_completa, 'w', encoding='utf-8') as file:
            json.dump(metadatos, file, indent=4)
        print(f'Los datos se han guardado en el archivo "{nombre_archivo}" en la carpeta de salida correctamente.')
    except Exception as e:
        print(f'Error al guardar el archivo JSON: {e}')

# URL del archivo competitions.json
url_competitions_json = 'https://github.com/VidalMiquel/Statsbomb/raw/master/data/competitions.json'

# Leer el contenido del archivo competitions.json desde la URL
contenido_json = leer_json_desde_url(url_competitions_json)

if contenido_json is not None:
    while True:
        competition_name = input('Ingresa el nombre de la competición: ')
        competition_gender = input('Ingresa el género de la competición: ')
        season_name = input('Ingresa el nombre de la temporada: ')

        resultados_busqueda = buscar_correspondencia(contenido_json, competition_name, competition_gender, season_name)

        if resultados_busqueda:
            guardar_datos_json(resultados_busqueda, competition_name, competition_gender, season_name)
            break
        else:
            print('No se encontraron correspondencias para los valores proporcionados.')
