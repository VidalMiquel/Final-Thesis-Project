import os
import json
import urllib.request
import sys

def obtener_nombre_experimento():
    # Verificar si se proporcionaron los argumentos adecuados
    print(sys.argv)
    if len(sys.argv) != 2:
        print(
            "Por favor, proporcione los valores para CompetitionName, CompetitionYear, CompetitionGender, y Club."
        )
        return None

    # Obtener los valores de los argumentos
    experimentName = sys.argv[1]

    return experimentName

nombre_experimento = obtener_nombre_experimento()

# Obtener la ruta del directorio donde se ejecuta el script
ruta_actual = os.path.abspath(os.path.dirname(__file__))

# Ruta al archivo 'id_matches.json' desde TFG/Code/FirstStage/
ruta_id_matches = os.path.join(ruta_actual, '..', '..', 'Data', nombre_experimento, 'FirstStage', 'Middle_files', 'id_matches.json')

# Ruta donde se guardarán los archivos descargados
ruta_output = os.path.join(ruta_actual, '..', '..', 'Data', nombre_experimento, 'FirstStage', 'Target_files')

# Verificar si el archivo 'id_matches.json' existe
if os.path.exists(ruta_id_matches):
    # Abrir el archivo 'id_matches.json' y cargar los datos JSON
    with open(ruta_id_matches, 'r') as archivo_id_matches:
        datos_id_matches = json.load(archivo_id_matches)
    
    # Iterar a través de las claves (números de jornada) y valores (listas de partidos) en 'id_matches.json'
    for jornada, partidos in datos_id_matches.items():
        for partido_id in partidos:
            # Construir la URL con el partido_id actual
            #url = f'https://github.com/statsbomb/open-data/blob/master/data/events/{partido_id}.json'
            url = f'https://raw.githubusercontent.com/VidalMiquel/Statsbomb/master/data/events/{partido_id}.json'
            
            # Nombre del archivo a guardar, usando el partido_id
            nombre_archivo = 'Football_day_{}.json'.format(jornada)
            
            # Ruta completa donde se guardará el archivo
            ruta_archivo_guardado = os.path.join(ruta_output, nombre_archivo)
            
            # Descargar el archivo desde la URL y guardarlo en la ruta especificada
            try:
                urllib.request.urlretrieve(url, ruta_archivo_guardado)
                print(f"Archivo {nombre_archivo} descargado correctamente.")
            except Exception as e:
                print(f"No se pudo descargar el archivo {nombre_archivo}. Error: {e}")
else:
    print("El archivo 'id_matches.json' no fue encontrado en la ubicación especificada.")
