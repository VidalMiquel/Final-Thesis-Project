import os

def crear_carpeta_ruta_absoluta(ruta):
    try:
        os.makedirs(ruta)
        print(f"Creada la carpeta en {ruta}")
    except FileExistsError:
        print(f"La carpeta en {ruta} ya existe.")

def crear_estructura_carpetas():
    # Obtener la ruta absoluta del directorio actual
    ruta_actual = os.path.abspath(os.path.dirname(__file__))

    # Construir la ruta absoluta de TFG/Data
    ruta_data = os.path.abspath(os.path.join(ruta_actual, '..', '..', 'Data'))

    # Nombre de la carpeta "FirstStage"
    nombre_carpeta_first_stage = 'FirstStage'

    # Ruta completa para la carpeta "FirstStage" dentro de "Data"
    ruta_first_stage = os.path.join(ruta_data, nombre_carpeta_first_stage)

    # Ruta completa para la carpeta "Middle_files" dentro de "FirstStage"
    ruta_middle_files = os.path.join(ruta_first_stage, 'Middle_files')

    # Ruta completa para la carpeta "Target_files" dentro de "FirstStage"
    ruta_target_files = os.path.join(ruta_first_stage, 'Target_files')

    # Crear la carpeta "Data" si no existe
    crear_carpeta_ruta_absoluta(ruta_data)

    # Crear la carpeta "FirstStage" dentro de "Data" si no existe
    crear_carpeta_ruta_absoluta(ruta_first_stage)

    # Crear la carpeta "Middle_files" dentro de "FirstStage" si no existe
    crear_carpeta_ruta_absoluta(ruta_middle_files)

    # Crear la carpeta "Target_files" dentro de "FirstStage" si no existe
    crear_carpeta_ruta_absoluta(ruta_target_files)

# Llamar a la función para crear la estructura de carpetas
crear_estructura_carpetas()
