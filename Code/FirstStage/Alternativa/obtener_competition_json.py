import os
import urllib.request
from urllib.parse import urlparse

# URL del archivo que deseas descargar
url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json'

# Obtener el nombre del archivo de la URL
nombre_archivo = os.path.basename(urlparse(url).path)

# Ruta absoluta del directorio actual
directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Ruta completa del archivo a descargar
ruta_archivo = os.path.join(directorio_actual, nombre_archivo)

try:
    urllib.request.urlretrieve(url, ruta_archivo)
    print(f'El archivo "{nombre_archivo}" ha sido descargado exitosamente en el directorio actual!')
except Exception as e:
    print(f'Error al descargar el archivo: {e}')
