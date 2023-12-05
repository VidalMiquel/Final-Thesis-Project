import os
import requests

# Función para obtener la ruta de salida
def obtener_ruta_output():
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_output = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data', 'FirstStage', 'Middle_files'))
    return ruta_output

def descargar_archivo(url, nombre_archivo, ruta_destino):
    # Obtener la ruta del directorio donde se ejecuta el script
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta completa de destino para guardar el archivo
    ruta_completa_destino = os.path.join(ruta_script, ruta_destino, nombre_archivo)
    
    # Descargar el archivo desde la URL
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Guardar el archivo en la ruta de destino
        with open(ruta_completa_destino, 'wb') as archivo:
            archivo.write(response.content)
        
        print(f"Archivo descargado y guardado en: {ruta_completa_destino}")
    else:
        print("No se pudo descargar el archivo.")

ruta_destino = obtener_ruta_output()

url_archivo = 'https://github.com/VidalMiquel/Statsbomb/raw/master/data/competitions.json'

nombre_archivo = "competitions.json"
# Llamar a la función para descargar y guardar el archivo
descargar_archivo(url_archivo, nombre_archivo, ruta_destino)
