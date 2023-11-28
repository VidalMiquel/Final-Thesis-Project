import json
import os

def leer_json(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data  # Devolver el contenido del archivo JSON
    except FileNotFoundError:
        print(f'El archivo "{ruta_archivo}" no fue encontrado.')
        return None
    except json.JSONDecodeError as e:
        print(f'Error al decodificar el archivo JSON: {e}')
        return None
    except Exception as e:
        print(f'Error al leer el archivo: {e}')
        return None

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

def obtener_ruta_actual():
    return os.path.dirname(os.path.abspath(__file__))


# Función para guardar datos en un archivo JSON
def guardar_datos_json(resultados_busqueda):
    nombre_archivo = 'datos_temporada_elegida.json'
    ruta_actual = obtener_ruta_actual()
    ruta_archivo_completa = os.path.join(ruta_actual, nombre_archivo)

    try:
        with open(ruta_archivo_completa, 'w', encoding='utf-8') as file:
            json.dump(resultados_busqueda, file, indent=4)
        print(f'Los datos se han guardado en el archivo "{nombre_archivo}" en el directorio actual correctamente.')
    except Exception as e:
        print(f'Error al guardar el archivo JSON: {e}')
        

# Uso de las funciones
ruta_competitions_json = 'competitions.json'  # Reemplazar con la ruta correcta al archivo

contenido_json = leer_json(ruta_competitions_json)

if contenido_json is not None:
    competition_name = input('Ingresa el nombre de la competición: ')
    competition_gender = input('Ingresa el género de la competición: ')
    season_name = input('Ingresa el nombre de la temporada: ')

    resultados_busqueda = buscar_correspondencia(contenido_json, competition_name, competition_gender, season_name)

    if resultados_busqueda:
        print('Correspondencias encontradas:')
        for resultado in resultados_busqueda:
            print(f'competition_id: {resultado["competition_id"]}, season_id: {resultado["season_id"]}')
            guardar_datos_json(resultados_busqueda)
    else:
        print('No se encontraron correspondencias para los valores proporcionados.')
