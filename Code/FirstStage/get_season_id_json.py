import json  
import urllib.request  
import os  

# Función para leer datos de la temporada desde un archivo JSON
def obtener_chosen_season_data_json(nombre_archivo):
    with open(nombre_archivo, 'r') as file:  # Abre el archivo en modo lectura
        data = json.load(file)  # Carga los datos JSON desde el archivo
    return data

def obtener_parametros(data):
    resultados = data['resultados']  # Obtiene la lista de resultados
    return resultados[0]['competition_id'], resultados[0]['season_id']  # Devuelve el competition_id y season_id

# Función para construir la URL para descargar el archivo JSON
def construir_url(competition_id, season_id):
    return f'https://github.com/VidalMiquel/Statsbomb/raw/master/data/matches/{competition_id}/{season_id}.json'

# Función para descargar un archivo desde una URL
def descargar_archivo(url, nombre_archivo):
    try:
        urllib.request.urlretrieve(url, nombre_archivo)  # Descarga el archivo desde la URL
        print(f"El archivo {nombre_archivo} se ha descargado correctamente.")  # Imprime un mensaje si la descarga es exitosa
    except Exception as e:
        print(f"No se pudo descargar el archivo. Error: {e}")  # Captura cualquier excepción en caso de error durante la descarga

# Obtener la ruta del directorio donde se ejecuta el script
ruta_actual = os.path.abspath(os.path.dirname(__file__))

# Definir las rutas de entrada y salida
ruta_input = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))
ruta_output = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))

# Definir el nombre del archivo que contiene datos de temporada
nombre_archivo_temporada = 'chosen_season_data.json'
ruta_chosen_season_data = os.path.join(ruta_input, nombre_archivo_temporada)  # Ruta del archivo de datos de temporada

# Leer el competition_id y season_id desde el archivo de datos de temporada
data_frame = obtener_chosen_season_data_json(ruta_chosen_season_data)

competition_id, season_id = obtener_parametros(data_frame)

# Construir la URL para descargar el archivo JSON usando competition_id y season_id
url = construir_url(competition_id, season_id)

# Definir el nombre del archivo de descarga y su ruta de guardado
nombre_archivo_descarga = 'season_id.json'
ruta_archivo_guardado = os.path.join(ruta_output, nombre_archivo_descarga)

# Descargar el archivo desde la URL y guardarlo en la ruta especificada
descargar_archivo(url, ruta_archivo_guardado)
