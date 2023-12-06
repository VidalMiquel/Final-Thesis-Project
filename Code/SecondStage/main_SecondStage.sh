#!/bin/bash

experimentName="$1"
echo "El valor del nombre del experimento es: $experimentName"

# Obtener la ruta del directorio actual
current_directory=$(dirname "$0")

# Cambiar al directorio que contiene start_FirstStage.py
cd "$current_directory"

# Ejecutar start_SecondStage.py
echo "Creando los directorios necesarios con start_SecondStage.py..."
python start_SecondStage.py "$experimentName"

echo "" # Línea en blanco
echo "Proceso completado."echo ""
# Línea en blanco
