# Area Data

## Area

CSVfile: area.csv

- Area.csv represents information about each area.

| Index  | Value     | Summary                                 |
| ------------- | ------ | ------------------------------------ |
| name          | character string | Name (duplication prohibited)<br />**Note**: Only ASCII characters (alphanumeric characters and symbols) are allowed. Non-ASCII characters such as Japanese are not allowed.                     |
| PV_cap        | numeral   | Total solar power generation capacity [MW]                |
| WF_cap        | numeral   | Total wind power generation capacity [MW]                  |
| C_short       | numeral   | Supply shortage cost [Thousands of yen/MWh]            |
| C_surplus     | numeral   | Supply surplus cost [Thousands of yen/MWh]            |
| C_Tert_short  | numeral   | Tertiary reserve shortage cost [Thousands of yen/MWh]      |
| C_PV_suppr    | numeral   | Solar power output suppression cost  [Thousands of yen/MWh] |
| C_WF_suppr    | numeral   | Wind power output suppression cost  [Thousands of yen/MWh]   |
| R_PV_res_UP   | numeral   | Solar power up-reserve availability rate [%]   |
| R_PV_res_DOWN | numeral   | Solar power down-reserve availability rate [%]   |
| R_WF_res_UP   | numeral   | Wind power up-reserve availability rate [%]     |
| R_WF_res_DOWN | numeral   | Wind power down-reserve availability rate [%]     |

### Example

[data_set/data-example/area.csv](../../data_set/data-example/area.csv)

[data_set/data-mini/area.csv](../../data_set/data-mini/area.csv)

| name   | PV_cap | WF_cap | C_short | C_surplus | C_Tert_short | C_PV_suppr | C_WF_suppr | R_PV_res_UP | R_PV_res_DOWN | R_WF_res_UP | R_WF_res_DOWN |
| :----- | :----- | :----- | :------ | :-------- | :----------- | :--------- | :--------- | :---------- | :------------ | :---------- | :------------ |
| Area_A | 7580   | 1880   | 100000  | 100000    | 1000         | 0          | 0          | 50          | 50            | 50          | 50            |
| Area_B | 5220   | 2670   | 100000  | 100000    | 1000         | 0          | 0          | 50          | 50            | 50          | 50            |
| ...    | ...    | ...    | ...     | ...       | ...          | ...        | ...        | ...         | ...           | ...         | ...           |
