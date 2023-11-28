import subprocess


# Ejecutar obtener_informacion_temporada.py
print("\nCreando lso directorios necessarios con start.py...")
subprocess.run(["python", "start.py"])

# Ejecutar obtener_informacion_temporada.py
print("\nEjecutando obtener_informacion_temporada.py...")
subprocess.run(["python", "get_season_information.py"])

# Ejecutar obtener_season_id_json.py
print("\nEjecutando obtener_season_id_json.py...")
subprocess.run(["python", "get_season_id_json.py"])

# Ejecutar obtener_id_partidos.py
print("\nEjecutando obtener_id_partidos.py...")
subprocess.run(["python", "get_id_matches.py"])

print("\nProceso completado.")
