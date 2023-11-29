import json
import urllib.request
import os

def leer_datos_temporada(nombre_archivo):
    with open(nombre_archivo, 'r') as file:
        data = json.load(file)
        resultados = data['resultados']
        return resultados[0]['competition_id'], resultados[0]['season_id']

def construir_url(competition_id, season_id):
    return f'https://github.com/VidalMiquel/Statsbomb/raw/master/data/matches/{competition_id}/{season_id}.json'

def descargar_archivo(url, nombre_archivo):
    try:
        urllib.request.urlretrieve(url, nombre_archivo)
        print(f"El archivo {nombre_archivo} se ha descargado correctamente.")
    except Exception as e:
        print(f"No se pudo descargar el archivo. Error: {e}")

# Obtener la ruta del directorio donde se ejecuta el script
ruta_actual = os.path.abspath(os.path.dirname(__file__))

# Definir las rutas de entrada y salida
ruta_input = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage','Middle_files'))
ruta_output = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))

nombre_archivo_temporada = 'chosen_season_data.json'
ruta_chosen_season_data = os.path.join(ruta_input, nombre_archivo_temporada)

competition_id, season_id = leer_datos_temporada(ruta_chosen_season_data)
url = construir_url(competition_id, season_id)
nombre_archivo_descarga = 'season_id.json'
ruta_archivo_guardado = os.path.join(ruta_output, nombre_archivo_descarga)

descargar_archivo(url, ruta_archivo_guardado)
