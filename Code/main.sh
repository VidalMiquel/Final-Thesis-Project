#!/bin/bash -e

# Prompt the user to enter the experiment name
echo "------------------------------------------"
echo "Enter the experiment name:"
read experimentName
echo ""

echo "Enter the club (club):"
read club
echo ""

# Directory where the stages are located (same level as main.sh)
directory=$(dirname "$0")

# Variable para controlar si ocurrió algún error
error_ocurrido=false

# Iterate over the directories at the same level as main.sh
for stage in "$directory"/*/; do
    stageName=$(basename "$stage")

    # Check if it is a valid stage directory (does not start with "_")
    if [[ $stageName != _* && -f "$stage/main_$stageName.sh" ]]; then

        # Ejecutar el script de la etapa
        bash "$stage/main_$stageName.sh" "$experimentName" "$club"

        # Verificar el código de salida del script anterior
        if [ $? -ne 0 ]; then
            echo "Error en main_$stageName.sh. Se detiene la ejecución."
            error_ocurrido=true
            break
        fi

        echo ""
    fi
done

# Verificar si ocurrió algún error durante la ejecución de los scripts
if [ "$error_ocurrido" = true ]; then
    echo "Se produjo un error durante la ejecución de los scripts. Se detiene la ejecución."
    exit 1
fi

# Continuar con el resto del script principal
echo "All executed correctly"
