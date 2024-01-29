Aquesta segona etapa (Second Stage) del TFG té com a objectiu dividir els fitxers ubicats a Data/ExperimentName/FirstStage/Target_files
per a cada vegada que hi ha hagut un gol al partit. De tal manera que el resultat son les divisons realitzades sobre un mateix partit. Identificam cada partit ammb el nom nom del arxiu origen i, afegim el nombre de subdivisió que representa "footballDay_x_n.json".

A més, i per començar a encarar el que serà l'anàlisi en base a l'equip introduït per l'usuari, filtram el fitxers resultats del desdoblament segons el club corresponent. Es generen aixi els arxius amb nom "footballDayFiltered_x_n.json"

******************************************************************************************************************************************

Adjunt el directori que forma aquesta segona etapa:

TFG
├── Code
│   └── FirstStage
│   └── SecondStage
│       ├── filterByTeam.py
│       ├── splitByGoals.py
│       ├── start_SecondStage.py
│       ├── main_SecondStage.sh
│       └── README.md
|   └── main.sh
└── Data
    └── experimentName
        └──FirstStage
        └──SecondStage
            ├── Middle_files
            │   ├── footballDay_1_1.json
            │   ├── {}
            │   └── footballDay_38_n.json
            └── Target_files
                ├── footballDayFiltered_1_1.json
                ├── {}
                └── footballDayFiltered_38_n.json