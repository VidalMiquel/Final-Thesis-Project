import json
import urllib.request
import os
import sys


def get_season_information():
    # Verificar si se proporcionaron los argumentos adecuados
    print(sys.argv)
    if len(sys.argv) != 6:
        print(
            "Por favor, proporcione los valores para CompetitionName, CompetitionYear, CompetitionGender, y Club."
        )
        return None

    # Obtener los valores de los argumentos
    competition_name = sys.argv[1]
    competition_year = sys.argv[2]
    competition_gender = sys.argv[3]
    club = sys.argv[4]
    experimentName = sys.argv[5]

    return competition_name, competition_year, competition_gender, club, experimentName


# Función para leer un archivo JSON desde una URL
def leer_json_desde_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data  # Devolver el contenido del archivo JSON
    except Exception as e:
        print(f"Error al leer el archivo desde la URL: {e}")
        return None


# Función para buscar correspondencia en los datos
def buscar_correspondencia(data, competition_name, competition_gender, season_name):
    resultados = []
    for competition in data:
        if (
            competition["competition_name"] == competition_name
            and competition["competition_gender"] == competition_gender
        ):
            if competition["season_name"] == season_name:
                resultados.append(
                    {
                        "competition_id": competition["competition_id"],
                        "season_id": competition["season_id"],
                    }
                )
    return resultados


# Función para obtener la ruta de salida
def obtener_ruta_output():
    ruta_actual = os.path.abspath(os.path.dirname(__file__))
    ruta_output = os.path.abspath(
        os.path.join(ruta_actual, "..", "..", "Data", experimentName, "FirstStage", "Middle_files")
    )
    return ruta_output


# Función para guardar datos con metadatos en un archivo JSON en la carpeta de salida
def guardar_datos_json(
    resultados_busqueda, competition_name, competition_gender, season_name, club, experimentName
):
    nombre_archivo = "chosen_season_data.json"
    ruta_output = obtener_ruta_output()
    ruta_archivo_completa = os.path.join(ruta_output, nombre_archivo)

    try:
        if not os.path.exists(ruta_output):
            os.makedirs(ruta_output)

        # Crear un diccionario para almacenar los metadatos
        metadatos = {
            "metadatos": {
                "competition_name": competition_name,
                "competition_gender": competition_gender,
                "season_name": season_name,
                "club": club,
                "experimentName": experimentName
            },
            "resultados": resultados_busqueda,
        }

        with open(ruta_archivo_completa, "w", encoding="utf-8") as file:
            json.dump(metadatos, file, indent=4)
        print(
            f'Los datos se han guardado en el archivo "{nombre_archivo}" en la carpeta de salida correctamente.'
        )
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")


# URL del archivo competitions.json
url_competitions_json = (
    "https://github.com/VidalMiquel/Statsbomb/raw/master/data/competitions.json"
)

# Leer el contenido del archivo competitions.json desde la URL
contenido_json = leer_json_desde_url(url_competitions_json)

if contenido_json is not None:
    try:
        values = get_season_information()

        if values:
            competition_name, competition_year, competition_gender, club, experimentName = values

            # Utilizar los valores obtenidos como sea necesario
            print("Competition Name:", competition_name)
            print("Competition Year:", competition_year)
            print("Competition Gender:", competition_gender)
            print("Club:", club)
            print("experimentName", experimentName)

            # Aquí podrías usar estos valores para realizar más operaciones en tu script
            # ...

            # Por ejemplo, si quieres pasar estos valores a otras funciones o realizar alguna lógica específica
            # puedes hacerlo a partir de aquí utilizando estas variables.

        resultados_busqueda = buscar_correspondencia(
            contenido_json, competition_name, competition_gender, competition_year
        )

        if resultados_busqueda:
            guardar_datos_json(
                resultados_busqueda,
                competition_name,
                competition_gender,
                competition_year,
                club,
                experimentName
            )
        else:
            print("No se encontraron correspondencias para los valores proporcionados.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
