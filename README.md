# TFG Miquel Vidal Cortés

Funcionament del TFG

#Estructura de carpetes per a cada etapa:

EL directori "TFG" conté les dues carpetes a partir de les quals es genera tot el projecte: "Code" i "Data". La funció principal de Code es emmagatzemar el codi necessari per poder generar tot el contingut de Data. L'objectiu és fer feina nómes amb el codi, i que gràcies a aquest, es generin el conjunt de dades (fitxers) que ens permeten dur a terme l'estudi. 

A més, per poder simplificar la comprensió del projecte, està dividit per etapes. Presents a les ambdues carpetes anomenades anteriorment. Cada etapa representa un conjunt fitat d'objectius. Tenen per nom "FirstSatge", "SecondStage", "nStage"... Aquesta estructura permet una organització clara i separació de codi i dades per a cada fase específica del projecte. A més, i amb l'objectiu de separar diferentes experiments, aquestes subcarpetes es troben situades a una d'altra anomenada "experiementName". Així podem fer feina amb diferents estudis.

#Relació entre les carpetes Code i Data per a cada etapa:

Carpeta Data: La carpeta Data/experimentName/nStage conté subcarpetes, anomenades Middle_files i Target_files. En Middle_files, es troben els fitxers que són processats pel codi situat en la carpeta Code/nStage. Els resultats o fitxers generats pel codi es guarden a la carpeta Target_files dins de la mateixa etapa (nStage) del directori Data/experimentName.

Carpeta Code: Dins de cada carpeta d'etapa (FirstStage, SecondStage, etc.), es troba el codi necessari per generar i manipular els fitxers que es guarden a la carpeta Data/experimentName/nStage/middle_files o Data/experimentName/nStage/target_files.

#Interacció entre Code i Data en cada etapa:

El codi a la carpeta Code (per exemple, Code/FirstStage) processa, manipula o genera fitxers que resideixen a Data/experimentName/FirstStage/middle_files. Els fitxers generats per aquest codi es desen a Data/nStage/Target_files, proporcionant una ruta clara des del codi fins als resultats o fitxers de sortida.

#Beneficis d'aquesta organització:

Aquesta estructura permet una clara separació entre codi i dades per a cada etapa del projecte. Millora la mantenibilitat del codi, facilita la gestió dels resultats i ajuda a entendre quina part del codi està involucrada en la generació de quins resultats.

#Flux de treball iteratiu:

A mesura que el projecte avança a través de les diferents etapes, el codi en les carpetes Code evoluciona i pot generar nous resultats que es desen en les carpetes Data corresponents a cada etapa específica del projecte.

#User:

La carpeta Data i tot el seu contingut es crea dinàmicament gràcies a un fitxer anomenat start_nStage.sh (crea per etapa), present a Code/nStage. Per tant, es crea de manera dinàmica. L'únic que ha de tenir l'usuari final en compte és la carpeta Code. El de més en genera dinàmicament. D'aquí a que el fitxer .gitignore tingui especificat ignorar la carpeta /Data.

Aquest enfocament proporciona una manera dinàmica i flexible de gestionar l'estructura del projecte, permetent que l'usuari final només necessiti preocupar-se de la carpeta Code, ja que la resta de l'estructura es genera de manera automàtica mitjançant l'execució dels fitxers específics de cada etapa.

ACLARACIONS

1- Totes les dades amb les quals estic fent feina han estat descarregades de la següent font d'informació: Statsbomb. Esteim fent feina amb l'apartat accesible per a estudiants.

2-En cas de que l'usuari introdueixi per teclat dades sense correspondència amb la font de dades amb la qual feim feina, l'execusió serà interrompuda i l'usuari serà notificat.
