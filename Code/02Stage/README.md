Aquesta segona etapa (02Stage) del TFG té com a objectiu dividir els fitxers ubicats a Data/ExperimentName/01Stage/TargetFiles
per a cada vegada que hi ha hagut un gol al partit. De tal manera que el resultat son les divisons realitzades sobre un mateix partit. Identificam cada partit ammb el nom del arxiu origen i, afegim el nombre de subdivisió que representa "x_n_footballDay.json". Aquests fitxers son emmagatzemats a Data/ExperimentName/02Stage/MiddleFiles

A més, i per començar a encarar el que serà l'anàlisi en base a l'equip introduït per l'usuari, filtram el fitxers resultats del desdoblament segons el club corresponent. Es generen aixi els arxius amb nom "x_n_footballDayFiltered.json.json". Aquests fitxers son emmagatzemats a Data/ExperimentName/02Stage/TargetFiles


*****************************************************************************************************************************************************************************************


Adjunt el directori que forma aquesta segona etapa:
"""
TFG
├── Code
│   └── 00Stage
│   └── 01Stage
│   └── 02Stage
│       ├── filterByTeam.py
│       ├── splitByGoals.py
│       ├── main02Stage.sh
│       └── README.md
|   └── main.sh
└── Data
    └── experimentName
        └── 00Stage
        └── 01Stage
        └── 02Stage
            ├── MiddleFiles
            │   ├── 1_1_footballDay.json
            │   ├── {}
            │   └── 364_n_footballDay.json
            └── TargetFiles
                ├── 1_1_footballDayFiltered.json
                ├── {}
                └── 364_n_footballDayFiltered.json
"""