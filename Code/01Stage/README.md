Aquesta primera etapa (01Stage) del TFG té com a objectiu obtenir els fitxers que emmagatzemen la infromació dels partits els quals vols estudiar.

Aquesta decisió d'estudi es vol deixar en mans de l'usuari, és a dir, per terminal indicarà quin club (clubName), quina és la temporada (seasonName), quina és la competició (competitionName) i quin futbol vol analitzar, si el masculí o el femení (competitionGender). Amb aquestes quatre dades executam "getSeasonInformation.py". El resultat és els valors de competiton_id i season_id, emmagatzemats a "chosen_season_data.json" obtinguts gràcies a una crida a un fitxer i als tres valors obtinguts per teclat. 

En segon lloc, amb els valors presents a "chosenSeasonData.json", executam "getSeasonInformation.py". L'objectiu es obtenir mitjançant una crida formada a partir de competiton_id i seaseon_id el fitxer "season_id.jsons". Aquest fitxer conté tots els partits de la temporada i competició desitjada.

En tercer lloc, i amb "seasonId.json" en local,  és el moment de que l'usuari, usant la terminal, indiqui quin clob vol treballar. tota aquesta lògica es troba a "getIdMatches.py". Per tant, amb aquesta dada recorrem "seasonId.json" i cercam els partits en els quals l'equip indicat jugui com a local o visitam. Per a les correspondències positives, emmagatzemam a "id_matches.json", "id_match" corresponents.

En quart lloc, i amb els identificadors de totes les jorandes. Executam "getTargetFiles.py". Aquest fitxer llegeix els identificadors de cada jornada de "idMatches.json" i realitza la cridada per descarregar cada un dels fitxers que emmagatzemen les dades del partit corresponent. Tots aquestes es troben dins la carpeta TargetFiles, que servirà de conexió entre la primera etapa (01Stage) i la següent (02Stage). 

Finalment, recordar que tant la creació del directori "Data" i les seves subcarpetes referents a First Stage es generen de manera dinàmica executant startData.py. Les execusions dels fitxers anomenats son unificades dins el fixter main01Stage.py, per simplificar la comprensió i la complexitat del codi.

*****************************************************************************************************************************************************************************************

Adjunt el directori que forma aquesta primera etapa:

TFG
├── Code
│   └── 00Stage
│   └── 01Stage
│       ├── getIdMatches.py
│       ├── getSeasonIdJSON.py
│       ├── getSeasonInformation.py
│       ├── getTargetFiles.py
│       ├── main01Stage.sh
│       └── README.md
|   └── main.sh
└── Data
    └── experimentName
        └──01Stage
            ├── MiddleFiles
            │   ├── chosenSeasonData.json
            │   ├── idMatches.json
            │   └── seasonId.json
            └── TargetFiles
                ├── 1_footballDay.json
                ├── {}
                └── 364_footballDay.json

