import subprocess


# Ejecutar start_FirstStage.py
print("\nCreando lso directorios necessarios con start_FirstStage.py...")
subprocess.run(["python", "start_FirstStage.py"])

# Ejecutar get_season_information.py
print("\nEjecutando get_season_information.py...")
subprocess.run(["python", "get_season_information.py"])

# Ejecutar get_season_id_json.py
print("\nEjecutando get_season_id_json.py...")
subprocess.run(["python", "get_season_id_json.py"])

# Ejecutar get_id_matches.py
print("\nEjecutando get_id_matches.py...")
subprocess.run(["python", "get_id_matches.py"])

# Ejecutar get_target_files.py
print("\nEjecutando get_target_files.py...")
subprocess.run(["python", "get_target_files.py"])

print("\nProceso completado. Directorios creados y ficheros de las jornadas obtenidos")
