#!/bin/bash

# Solicitar al usuario el nombre del experimento
echo "Ingrese el nombre del experimento:"
read nombre_experimento

# Directorio donde se encuentran las etapas (mismo nivel que main.sh)
directorio=$(dirname "$0")
echo $directorio

# Iterar sobre los directorios presentes en el mismo nivel que main.sh
for etapa in "$directorio"/*/; do
    nombre_etapa=$(basename "$etapa")
    echo $nombre_etapa
    # Verificar si es un directorio de etapa válido (no comienza con "_")
    if [[ $nombre_etapa != _* && -f "$etapa/main_$nombre_etapa.sh" ]]; then
        echo "Ejecutando $nombre_etapa..."
        bash "$etapa/main_$nombre_etapa.sh" "$nombre_experimento"
    fi
done
