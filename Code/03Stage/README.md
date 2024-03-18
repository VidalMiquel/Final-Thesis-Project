Aquesta tercera etapa (Third Stage) del TFG té com a objectiu definir una estructura de tal manera que per cada columna només tenir un valor per fila. És a dir, el valor associat a una fila no pot ser un array d'objectes, sinó un únic objecte. Per això, usam la funció "flatten_json".

Una vegada tenim aquest tipus d'arquitectura, els guardam com a tipus csv. Això ens permet poder usar la llibreria "panda" sense cap tipus de restriccions ni complexitat.


******************************************************************************************************************************************

Adjunt el directori que forma aquesta segona etapa:

TFG
├── Code
│   └── FirstStage
│   └── SecondStage
│   └── ThirdStage
│       ├── flattenJSONfiles.py
│       ├── startThirdStage.py
│       ├── main_ThirdStage.sh
│       └── README.md
|   └── main.sh
└── Data
    └── experimentName
        └──FirstStage
        └──SecondStage
        └──ThirdStage
            ├── Middle_files
            │   ├── footballDayFlattened_1_1.csv
            │   ├── {}
            │   └── footballDayFlattened_38_n.csv
            └── Target_files
