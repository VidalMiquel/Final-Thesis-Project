import os

# Obtener la ruta absoluta del directorio actual
ruta_actual = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta absoluta de TFG/Data
ruta_data = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data'))

# Nombre de la carpeta "FirstStage"
nombre_carpeta_first_stage = 'FirstStage'

# Ruta completa para la carpeta "FirstStage" dentro de "Data"
ruta_first_stage = os.path.join(ruta_data, nombre_carpeta_first_stage)

try:
    os.makedirs(ruta_first_stage)  # Crear directorio y directorios padres si no existen
    print(f"Creada la carpeta '{nombre_carpeta_first_stage}' dentro de 'Data' en {ruta_data}")
except FileExistsError:
    print(f"La carpeta '{nombre_carpeta_first_stage}' dentro de 'Data' en {ruta_data} ya existe.")
