#!/bin/bash

experimentName="$1"
echo "El valor del nombre del experimento es: $experimentName"

# Obtener la ruta del directorio actual
current_directory=$(dirname "$0")

# Cambiar al directorio que contiene start_FirstStage.py
cd "$current_directory"

# Ejecutar start_FirstStage.py
echo "Creando los directorios necesarios con start_FirstStage.py..."
python start_FirstStage.py "$experimentName"


# Solicitar al usuario los valores de CompetitionName, CompetitionYear, CompetitionGender y Club
echo "Ingrese el nombre de la competición (competitionName):"
read competitionName

echo "Ingrese el año de la competición (competitionYear):"
read competitionYear

echo "Ingrese el género de la competición (competitionGender):"
read competitionGender

echo "Ingrese el club (club):"
read club




#Agregar líneas en blanco para separar las secciones
echo "" # Línea en blanco
echo "Ejecutando get_season_information.py con los parámetros proporcionados..."
python get_season_information.py "$competitionName" "$competitionYear" "$competitionGender" "$club" "$experimentName"


#Agregar más líneas en blanco si se desea
echo "" # Otra línea en blanco

#Ejecutar get_season_id_json.py
echo "" # Línea en blanco
echo "Ejecutando get_season_id_json.py..."
python get_season_id_json.py "$experimentName"
echo "" # Línea en blanco

#Ejecutar get_id_matches.py
echo "" # Línea en blanco
echo "Ejecutando get_id_matches.py..."
python get_id_matches.py "$experimentName"
echo "" # Línea en blanco

#Ejecutar get_target_files.py
echo "" # Línea en blanco
echo "Ejecutando get_target_files.py..."
python get_target_files.py "$experimentName"
echo "" # Línea en blanco

# Agregar una línea en blanco al final del proceso
echo "" # Última línea en blanco
echo "Proceso de recopilación de datos completado."
echo "" # Línea en blanco

echo "" # Línea en blanco
echo "Proceso completado."echo ""
# Línea en blanco
