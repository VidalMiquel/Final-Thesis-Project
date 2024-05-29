Aquesta tercera etapa (03Stage) del TFG té com a objectiu definir una estructura de fitxer de tal manera que per cada columna només tenir un valor per fila. És a dir, el valor associat a una fila no pot ser un array d'objectes, sinó un únic objecte. Per això, usam la funció "flatten_json".

Una vegada tenim aquest tipus d'arquitectura, els guardam com a tipus csv. Això ens permet poder usar la llibreria "pandas" sense cap tipus de restriccions ni complexitat.
*****************************************************************************************************************************************************************************************

Adjunt el directori que forma aquesta tercera etapa:
"""
TFG
├── Code
│   └── 00Stage
│   └── 01Stage
│   └── 02Stage
│   └── 03Stage
│       ├── flattenJSONfiles.py
│       ├── main03Stage.sh
│       └── README.md
|   └── main.sh
└── Data
    └── experimentName
        └── 00Stage
        └── 01Stage
        └── 02Stage
        └── 03Stage
            ├── MiddleFiles
            │   ├── 1_1_footballDay.json
            │   ├── {}
            │   └── 364_n_footballDay.json
            └── TargetFiles
                ├── 1_1_footballDayFlattened.json
                ├── {}
                └── 364_n_footballDayFlattened.json
"""