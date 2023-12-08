from decimal import DivisionByZero
import sys
import os
import json
import pandas as pd

def getExperimentName():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("ExperimentName has not been provided as an argument.")
        sys.exit(1)

def generateDynamicPaths(experimentName):

    currentDir = os.path.abspath(os.path.dirname(__file__))   # Directorio actual del script
    print(currentDir)
    dataFolder = os.path.join(currentDir, '..', '..', 'Data', experimentName, 'FirstStage', 'Target_files')
    print(dataFolder)
    targetFolder = os.path.join(currentDir, '..', '..', 'Data', experimentName, 'SecondStage', 'Middle_files')
    print(targetFolder)

    if not os.path.exists(targetFolder):
        print(f"The folder {targetFolder} does not exist for experiment {experimentName}.")
        sys.exit(1)

    return dataFolder, targetFolder


def count_files_in_folder(folder_path):
    try:
        # Verificar si la ruta es un directorio válido
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            num_files = len(files)
            return num_files
        else:
            print(f"La ruta {folder_path} no es un directorio válido.")
            return None
    except OSError as e:
        print(f"Error al acceder al directorio: {e}")
        return None
    
import os

def iterate_and_check_files(currentPath, num_files):
    try:
        # Iterar sobre cada uno de los archivos en targetPath
        for i in range(1, num_files + 1):
            file_name = f"Football_day_{i}.json"
            file_path = os.path.join(currentPath, file_name)
            
            # Verificar si el archivo existe
            if os.path.exists(file_path) and os.path.isfile(file_path):
                print(f"El archivo '{file_name}' se encontró correctamente.")
            else:
                print(f"No se encontró el archivo '{file_name}'.")
    except OSError as e:
        print(f"Error al acceder a la ruta: {e}")

import os

def iterate_and_read_files(currentPath, targetPath, num_files):
    try:
        for i in range(1, num_files + 1):
            file_name = f"Football_day_{i}.json"
            file_path = os.path.join(currentPath, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    #print(file_path)
                    dFrame = pd.DataFrame(content)
                    splitList = get_division_indices(dFrame)
                    generate_division_files(splitList,dFrame,i, targetPath)
            except OSError as e:
                print(f"Error al leer el archivo '{file_name}': {e}")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON en '{file_name}': {e}")
    except OSError as e:
        print(f"Error al acceder a la ruta: {e}")


def get_division_indices(data):
    # Filter rows based on conditions
    auxiliar = data[data["type"].apply(lambda x: (x)['id'] == 23)]
    aux2 = auxiliar[auxiliar["goalkeeper"].apply(lambda x: (x)["type"]["id"] == 26)]

    # Check if 'aux2' is not empty before proceeding
    if not aux2.empty:
        # Get division indices
        division_indices = aux2.index.tolist()
        division_indices.insert(0, 0)  # Add initial index to divide the first segment
        division_indices.append(len(data))  # Add final index to divide the last segment
        print(division_indices)
        return division_indices
    else:
        print("There are no divisions in 'data' as aux2 is empty.")
        return None



def generate_division_files(indices_list, dataframe, jornada_value, target_path):
    try:
        # Iterar sobre los índices de división
        for i in range(len(indices_list) - 1):
            start_index = indices_list[i]
            end_index = indices_list[i + 1]

            # Obtener el segmento correspondiente en el DataFrame
            segment = dataframe.iloc[start_index:end_index]

            # Verificar si el segmento no está vacío antes de guardar
            if not segment.empty:
                # Nombre del archivo con el formato Football_day_n_m
                file_name = f"Football_day_{jornada_value}_{i+1}.json"
                file_path = os.path.join(target_path, file_name)

                # Guardar el segmento como un archivo JSON
                segment.to_json(file_path, orient='records')
                print(f"Archivo '{file_name}' generado exitosamente.")
            else:
                print(f"El segmento {i+1} para la jornada {jornada_value} está vacío, no se generará archivo.")
    except Exception as e:
        print(f"Error al generar archivos de división: {e}")



def main():
    experimentName = getExperimentName()
    #experimentName = "FCBarcelona"
    dataFolder, targetFolder = generateDynamicPaths(experimentName)
    numFootballDayFiles = count_files_in_folder(dataFolder)
    #numFootballDayFiles, footballDayFiles = countFootballDayFiles(targetFolder)

    print(f"ExperimentName value is: {experimentName}")
    print(f"Total number of Football_Day_n files is: {numFootballDayFiles}")

    #iterate_and_check_files(dataFolder, numFootballDayFiles)
    iterate_and_read_files(dataFolder, targetFolder, numFootballDayFiles)  
if __name__ == "__main__":
    main()
