# 地域データ

## 地域

CSVファイル: area.csv

- 各地域の情報を表す

| インデックス  | 値     | 概要                                 |
| ------------- | ------ | ------------------------------------ |
| name          | 文字列 | 名称（重複禁止）                     |
| PV_cap        | 数字   | 太陽光発電総容量 [MW]                |
| WF_cap        | 数字   | 風力発電総容量 [MW]                  |
| C_short       | 数字   | 供給不足処理費 [千円/MWh]            |
| C_surplus     | 数字   | 供給余剰処理費 [千円/MWh]            |
| C_Tert_short  | 数字   | 三次調整力不足処理費 [千円/MWh]      |
| C_PV_suppr    | 数字   | 太陽光発電出力抑制処理費  [千円/MWh] |
| C_WF_suppr    | 数字   | 風力発電出力抑制処理費  [千円/MWh]   |
| R_PV_res_UP   | 数字   | 太陽光発電上げ調整力提供可能率 [%]   |
| R_PV_res_DOWN | 数字   | 太陽光発電下げ調整力提供可能率 [%]   |
| R_WF_res_UP   | 数字   | 風力発電上げ調整力提供可能率 [%]     |
| R_WF_res_DOWN | 数字   | 風力発電下げ調整力提供可能率 [%]     |

### 例

[data_set/data-example/area.csv](../../data_set/data-example/area.csv)

[data_set/data-mini/area.csv](../../data_set/data-mini/area.csv)

| name   | PV_cap | WF_cap | C_short | C_surplus | C_Tert_short | C_PV_suppr | C_WF_suppr | R_PV_res_UP | R_PV_res_DOWN | R_WF_res_UP | R_WF_res_DOWN |
| :----- | :----- | :----- | :------ | :-------- | :----------- | :--------- | :--------- | :---------- | :------------ | :---------- | :------------ |
| Area_A | 7580   | 1880   | 100000  | 100000    | 1000         | 0          | 0          | 50          | 50            | 50          | 50            |
| Area_B | 5220   | 2670   | 100000  | 100000    | 1000         | 0          | 0          | 50          | 50            | 50          | 50            |
| ...    | ...    | ...    | ...     | ...       | ...          | ...        | ...        | ...         | ...           | ...         | ...           |
