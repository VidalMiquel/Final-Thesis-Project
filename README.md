# TFG Miquel Vidal Cortés

Funcionament del TFG

#Estructura de carpetes per a cada etapa:

Tant la secció "Code" com la secció "Data" contenen carpetes anomenades FirstStage, SecondStage, etc., per a cada etapa del desenvolupament. Aquesta estructura permet una organització clara i separació de codi i dades per a cada fase específica del projecte.

#Relació entre les carpetes Code i Data per a cada etapa:

Carpeta Data: La carpeta Data/nStage conté subcarpetes com Middle_files i Target_files. En Middle_files, es troben els fitxers que són processats pel codi en la carpeta Code. Els resultats o fitxers generats pel codi es guarden a la carpeta Target_files dins de la mateixa etapa (nStage) de la carpeta Data.

Carpeta Code: Dins de cada carpeta d'etapa (FirstStage, SecondStage, etc.), es troba el codi necessari per generar i manipular els fitxers que es guarden a la carpeta Data/nStage/middle_files.

#Interacció entre Code i Data en cada etapa:

El codi a la carpeta Code (per exemple, FirstStage) processa, manipula o genera fitxers que resideixen a Data/FirstStage/middle_files. Els fitxers generats per aquest codi es desen a Data/nStage/Target_files, proporcionant una ruta clara des del codi fins als resultats o fitxers de sortida.

#Beneficis d'aquesta organització:

Aquesta estructura permet una clara separació entre codi i dades per a cada etapa del projecte. Millora la mantenibilitat del codi, facilita la gestió dels resultats i ajuda a entendre quina part del codi està involucrada en la generació de quins resultats.

#Flux de treball iteratiu:

A mesura que el projecte avança a través de les diferents etapes, el codi en les carpetes Code evoluciona i pot generar nous resultats que es desen en les carpetes Data corresponents a cada etapa específica del projecte.

#User:

La carpeta Data i tot el seu contingut es crea dinàmicament gràcies a un fitxer anomenat start_nStage.py (crea per etapa), present a Code/nStage. Per tant, es crea de manera dinàmica. L'únic que ha de tenir l'usuari final en compte és la carpeta Code. El de més en genera dinàmicament. D'aquí a que el fitxer .gitignore tingui especificat ignorar la carpeta /Data.

Aquest enfocament proporciona una manera dinàmica i flexible de gestionar l'estructura del projecte, permetent que l'usuari final només necessiti preocupar-se de la carpeta Code, ja que la resta de l'estructura es genera de manera automàtica mitjançant l'execució dels fitxers específics de cada etapa.