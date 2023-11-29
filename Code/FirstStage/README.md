Aquesta primera etapa (FirstStage) del TFG té com a objectiu obtenir els fitxers que emmagatzemen la infromació dels partits els quals vols estudiar.

Aquesta decisió d'estudi es vol deixar en mans de l'usuari, és a dir, per terminal indicarà quina és la temporada (season_name), quina és la competició (competition_name) i quin futbol vol analitzar, si el masculí o el femení (competition_gender). Amb aquestes tres primeres dades executam "get_season_information.py". El resultat és els valors de competiton_id i season_id, emmagatzemats a "chosen_season_data.json" obtinguts gràcies a una crida a un fitxer i als tres valors obtinguts per teclat. 

En segon lloc, amb els valors presents a "chosen_season_data.json", executam "get_season_id_json.py". L'objectiu es obtenir mitjançant una crida formada a partir de competiton_id i seaseon_id el fitxer "season_id.jsons". Aquest fitxer conté tots els partits de la temporada i competició desitjada.

En tercer lloc, i amb "season_id.json" en local,  és el moment de que l'usuari, usant la terminal, indiqui quin clob vol treballar. tota aquesta lògica es troba a ""get_id_matches.py". Per tant, amb aquesta dada recorrem "season_id.json" i cercam els partits en els quals l'equip indicat jugui com a local o visitam. Per a les correspondències positives, emmagatzemam a "id_matches.json", "id_match" corresponents.

En quart lloc, i amb els identificadors de totes les jorandes. Executam "get_target_files.py". Aquest fitxer llegeix els identificadors de cada jornada de "id_matches.json" i realitza la cridada per descarregar cada un dels fitxers que emmagatzemen les dades del partit corresponent. Tots aquestes es troben dins la carpeta Target_files, que servirà de conexió entre la primera etapa (FirstStage) i la següent (SecondStage). 

Finalment, recordar que tant la creació del directori "Data" i les seves subcarpetes referents a First Stage es generen de manera dinàmica executant start_FirstStage.py. Tant aquesta execusió com la de tots els fitxers anomenats son unificades dins el fixter main_FirstStage.py, per simplificar la comprensió i la complexitat del codi.

******************************************************************************************************************************************

Adjunt el directori que forma aquesta primera etapa:

TFG
├── Code
│   └── FirstStage
│       ├── get_id_matches.py
│       ├── get_season_id_json.py
│       ├── get_season_information.py
│       ├── get_target_files.py
│       ├── main_FirstStage.py
│       ├── start_FirstStage.py
│       └── README.md
└── Data
    └── FirstStage
        ├── Middle_files
        │   ├── chosen_season_data.json
        │   ├── id_matches.json
        │   └── season_id.json
        └── Target_files
            ├── 1.json
            ├── 2.json
            └── 38.json

