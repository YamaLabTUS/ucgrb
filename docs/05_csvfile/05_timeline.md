# 時系列データ

1行A列が「time」のcsvファイルは時系列データとして扱う。

- A列目はB列目以降の値の対象時間。Hour End表記で，一日を1:00～0:00で表す。
  - 例1: 「2040/8/2 1:00:00」は，2040/8/2 0:00～1:00 を指す。
  - 例2: 「2040/8/3 0:00:00」は，2040/8/2 23:00～8/3 0:00 を指す。**8/3 0:00 のデータは，8/2を対象としていることに注意。**

## 電力需要

**ファイル名: demand.csv**

- 各地域の電力需要を示す。
- 単位はMW。

### 例
[data_set/data-example/demand/demand.csv](../../data_set/data-example/demand/demand.csv)

[data_set/data-mini/demand/demand.csv](../../data_set/data-mini/demand/demand.csv)

| time           | Area_A      | Area_B      | ...  |
| :------------- | :---------- | :---------- | :--- |
| 2016/3/31 1:00 | 3516.309047 | 1755.790946 | ...  |
| 2016/3/31 2:00 | 3358.573043 | 1804.286827 | ...  |
| 2016/3/31 3:00 | 3315.617801 | 1854.290312 | ...  |
| ...            | ...         | ...         | ...  |

## 電力需要短周期（GF&LFC成分）変動予測誤差率

**ファイル名: demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv**

- 各地域の電力需要の短周期（GF&LFC成分）変動予測誤差率を示す。
- 上げ調整力と下げ調整力、計２つのファイルが必要となる。
- 単位は実需要に対する割合[%]。

### 例

[data_set/data-example/demand/demand_R_GF_LFC_UP.csv](../../data_set/data-example/demand/demand_R_GF_LFC_UP.csv)

[data_set/data-example/demand/demand_R_GF_LFC_DOWN.csv](../../data_set/data-example/demand/demand_R_GF_LFC_DOWN.csv)

[data_set/data-mini/demand/demand_R_GF_LFC_UP.csv](../../data_set/data-mini/demand/demand_R_GF_LFC_UP.csv)

[data_set/data-mini/demand/demand_R_GF_LFC_DOWN.csv](../../data_set/data-mini/demand/demand_R_GF_LFC_DOWN.csv)


| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 2      | 2      | ...  |
| 2016/3/31 2:00 | 2      | 2      | ...  |
| 2016/3/31 3:00 | 2      | 2      | ...  |
| ...            | ...    | ...    | ...  |

## 最低確保単位系統慣性

**ファイル名: demand_M_req.csv**

- 各地域の最低確保単位系統慣性を示す。
- 単位は実需要に対する係数 [MW·s/MVA]。

### 例
[data_set/data-example/demand/demand_M_req.csv](../../data_set/data-example/demand/demand_M_req.csv)

[data_set/data-mini/demand/demand_M_req.csv](../../data_set/data-mini/demand/demand_M_req.csv)

| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 1      | 1      | ...  |
| 2016/3/31 2:00 | 1      | 1      | ...  |
| 2016/3/31 3:00 | 1      | 1      | ...  |
| ...            | ...    | ...    | ...  |
## 太陽光発電実出力

**ファイル名: PV_ACT.csv**

- 各地域の太陽光発電実出力値を示す。
- 単位は単位容量あたりの出力(p.u.)。

### 例

[data_set/data-example/PV/PV_ACT.csv](../../data_set/data-example/PV/PV_ACT.csv)

[data_set/data-mini/PV/PV_ACT.csv](../../data_set/data-mini/PV/PV_ACT.csv)

| time            | Area_A | Area_B | ...  |
| :-------------- | :----- | :----- | :--- |
| 2016/3/31 1:00  | 0      | 0      | ...  |
| 2016/3/31 2:00  | 0      | 0      | ...  |
| 2016/3/31 3:00  | 0      | 0      | ...  |
| 2016/3/31 4:00  | 0      | 0      | ...  |
| 2016/3/31 5:00  | 0      | 0      | ...  |
| 2016/3/31 6:00  | 0.011  | 0.029  | ...  |
| 2016/3/31 7:00  | 0.132  | 0.154  | ...  |
| 2016/3/31 8:00  | 0.284  | 0.278  | ...  |
| 2016/3/31 9:00  | 0.425  | 0.381  | ...  |
| 2016/3/31 10:00 | 0.552  | 0.494  | ...  |
| 2016/3/31 11:00 | 0.587  | 0.567  | ...  |
| 2016/3/31 12:00 | 0.648  | 0.625  | ...  |
| 2016/3/31 13:00 | 0.633  | 0.644  | ...  |
| 2016/3/31 14:00 | 0.518  | 0.582  | ...  |
| 2016/3/31 15:00 | 0.337  | 0.482  | ...  |
| 2016/3/31 16:00 | 0.181  | 0.322  | ...  |
| 2016/3/31 17:00 | 0.103  | 0.179  | ...  |
| 2016/3/31 18:00 | 0.05   | 0.045  | ...  |
| 2016/3/31 19:00 | 0      | 0      | ...  |
| 2016/3/31 20:00 | 0      | 0      | ...  |
| 2016/3/31 21:00 | 0      | 0      | ...  |
| 2016/3/31 22:00 | 0      | 0      | ...  |
| 2016/3/31 23:00 | 0      | 0      | ...  |
| 2016/4/1 0:00   | 0      | 0      | ...  |
| ...             | ...    | ...    | ...  |

## 太陽光発電出力予測最大値

**ファイル名: PV_FCST_U.csv**

## 太陽光発電出力予測値

**ファイル名: PV_FCST_M.csv**

## 太陽光発電出力予測最小値

**ファイル名: PV_FCST_L.csv**

- 各地域の太陽光発電出力予測値を示す。
- FCST_U前日計画における予測最大値、FCST_Mのデータを前日計画における予測値、FCST_Lのデータを前日計画における予測最小値としてあつかう。
- 単位は単位容量あたりの出力(p.u.)。

### 例
[data_set/data-example/PV/PV_FCST_U.csv](../../data_set/data-example/PV/PV_FCST_U.csv)

[data_set/data-example/PV/PV_FCST_M.csv](../../data_set/data-example/PV/PV_FCST_M.csv)

[data_set/data-example/PV/PV_FCST_L.csv](../../data_set/data-example/PV/PV_FCST_L.csv)


| time            | Area_A   | Area_B   | ...  |
| :-------------- | :------- | :------- | :--- |
| 2016/3/31 1:00  | 0        | 0        | ...  |
| 2016/3/31 2:00  | 0        | 0        | ...  |
| 2016/3/31 3:00  | 0        | 0        | ...  |
| 2016/3/31 4:00  | 0        | 0        | ...  |
| 2016/3/31 5:00  | 0        | 0        | ...  |
| 2016/3/31 6:00  | 0        | 0.053144 | ...  |
| 2016/3/31 7:00  | 0.060234 | 0.183718 | ...  |
| 2016/3/31 8:00  | 0.122147 | 0.3434   | ...  |
| 2016/3/31 9:00  | 0.18189  | 0.490756 | ...  |
| 2016/3/31 10:00 | 0.327713 | 0.647265 | ...  |
| 2016/3/31 11:00 | 0.345588 | 0.693258 | ...  |
| 2016/3/31 12:00 | 0.348636 | 0.70164  | ...  |
| 2016/3/31 13:00 | 0.352143 | 0.652095 | ...  |
| 2016/3/31 14:00 | 0.345648 | 0.574678 | ...  |
| 2016/3/31 15:00 | 0.315152 | 0.466525 | ...  |
| 2016/3/31 16:00 | 0.147722 | 0.236084 | ...  |
| 2016/3/31 17:00 | 0.076444 | 0.100926 | ...  |
| 2016/3/31 18:00 | 0.017988 | 0.019326 | ...  |
| 2016/3/31 19:00 | 0        | 0        | ...  |
| 2016/3/31 20:00 | 0        | 0        | ...  |
| 2016/3/31 21:00 | 0        | 0        | ...  |
| 2016/3/31 22:00 | 0        | 0        | ...  |
| 2016/3/31 23:00 | 0        | 0        | ...  |
| 2016/4/1 0:00   | 0        | 0        | ...  |
| ...             | ...      | ...      | ...  |

## 太陽光発電短周期（GF&LFC成分）変動予測誤差率

**ファイル名: PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv**

- 各地域の太陽光発電の短周期（GF&LFC成分）変動予測誤差率を示す。
- 上げ調整力と下げ調整力、計２つのファイルが必要となる。
- 単位は発電量から抑制量を引いた値に対する割合(%)。


### 例
[data_set/data-example/PV/PV_R_GF_LFC_UP.csv](../../data_set/data-example/PV/PV_R_GF_LFC_UP.csv)

[data_set/data-example/PV/PV_R_GF_LFC_DOWN.csv](../../data_set/data-example/PV/PV_R_GF_LFC_DOWN.csv)

[data_set/data-mini/PV/PV_R_GF_LFC_UP.csv](../../data_set/data-mini/PV/PV_R_GF_LFC_UP.csv)

[data_set/data-mini/PV/PV_R_GF_LFC_DOWN.csv](../../data_set/data-mini/PV/PV_R_GF_LFC_DOWN.csv)

| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 10     | 10     | ...  |
| 2016/3/31 2:00 | 10     | 10     | ...  |
| 2016/3/31 3:00 | 10     | 10     | ...  |
| 2016/3/31 4:00 | 10     | 10     | ...  |
| ...            | ...    | ...    | ...  |

## 風力発電実出力

**ファイル名: WF_ACT.csv**

- 各地域の風力発電実出力値を示す。
- 単位は単位容量あたりの出力(p.u.)。

### 例

[data_set/data-example/WF/WF_ACT.csv](../../data_set/data-example/WF/WF_ACT.csv)

[data_set/data-mini/WF/WF_ACT.csv](../../data_set/data-mini/WF/WF_ACT.csv)

| time           | Area_A      | Area_B      | ...  |
| :------------- | :---------- | :---------- | :--- |
| 2016/3/31 1:00 | 0.293882979 | 0.321685393 | ...  |
| 2016/3/31 2:00 | 0.233297872 | 0.314494382 | ...  |
| 2016/3/31 3:00 | 0.161595745 | 0.313033708 | ...  |
| 2016/3/31 4:00 | 0.122340426 | 0.328876404 | ...  |
| ...            | ...         | ...         | ...  |
## 風力発電出力予測最大値

**ファイル名: WF_FCST_U.csv**

## 風力発電出力予測値

**ファイル名: WF_FCST_M.csv**

## 風力発電出力予測最小値

**ファイル名: WF_FCST_L.csv**

- 各地域の風力発電出力予測値を超過確率を示す。
- 単位は単位容量あたりの出力(p.u.)。

### 例
[data_set/data-example/WF/WF_FCST_U.csv](../../data_set/data-example/WF/WF_FCST_U.csv)

[data_set/data-example/WF/WF_FCST_M.csv](../../data_set/data-example/WF/WF_FCST_M.csv)

[data_set/data-example/WF/WF_FCST_L.csv](../../data_set/data-example/WF/WF_FCST_L.csv)

| time           | Area_A      | Area_B      | ...  |
| :------------- | :---------- | :---------- | :--- |
| 2016/3/31 1:00 | 0.575053191 | 0.716966292 | ...  |
| 2016/3/31 2:00 | 0.558457447 | 0.710224719 | ...  |
| 2016/3/31 3:00 | 0.42893617  | 0.700561798 | ...  |
| 2016/3/31 4:00 | 0.417925532 | 0.706179775 | ...  |
| ...            | ...         | ...         | ...  |

## 風力発電短周期（GF&LFC成分）変動予測誤差率 - WF_R_GF_LFC_UP, WF_R_GF_LFC_DOWN -

**CSVファイル名: WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv**

- 各地域の風力発電の短周期（GF&LFC成分）変動予測誤差率を示す。
- 上げ調整力と下げ調整力、計２つのファイルが必要となる。
- 単位は発電量から抑制量を引いた値に対する割合(%)。

### 例
[data_set/data-example/WF/WF_R_GF_LFC_UP.csv](../../data_set/data-example/WF/WF_R_GF_LFC_UP.csv)

[data_set/data-example/WF/WF_R_GF_LFC_DOWN.csv](../../data_set/data-example/WF/WF_R_GF_LFC_DOWN.csv)

[data_set/data-mini/WF/WF_R_GF_LFC_UP.csv](../../data_set/data-mini/WF/WF_R_GF_LFC_UP.csv)

[data_set/data-mini/WF/WF_R_GF_LFC_DOWN.csv](../../data_set/data-mini/WF/WF_R_GF_LFC_DOWN.csv)

| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 10     | 10     | ...  |
| 2016/3/31 2:00 | 10     | 10     | ...  |
| 2016/3/31 3:00 | 10     | 10     | ...  |
| ...            | ...    | ...    | ...  |

## **連系線運用容量・マージン**

**ファイル名: TTC_forward.csv, TTC_counter.csv, Margin_forward.csv, Margin_counter.csv**

- 各連系線の順方向、逆方向の運用容量・マージンを示す。
- 単位はMW。
- **setting_method_of_TTC_and_Margin**=`timeline`のときに用いられる。

### 例
[data_set/data-example/tie/timeline/TTC_forward.csv](../../data_set/data-example/tie/timeline/TTC_forward.csv)

[data_set/data-example/tie/timeline/TTC_counter.csv](../../data_set/data-example/tie/timeline/TTC_counter.csv)

[data_set/data-example/tie/timeline/Margin_forward.csv](../../data_set/data-example/tie/timeline/Margin_forward.csv)

[data_set/data-example/tie/timeline/Margin_counter.csv](../../data_set/data-example/tie/timeline/Margin_counter.csv)


| time           | Tie-Line | ...  |
| :------------- | :------- | :--- |
| 2016/3/31 1:00 | 300      | ...  |
| 2016/3/31 2:00 | 300      | ...  |
| 2016/3/31 3:00 | 300      | ...  |
| 2016/3/31 4:00 | 300      | ...  |
| 2016/3/31 5:00 | 300      | ...  |
| ...            | ...      | ...  |

## 融通調整量最大値

**ファイル名:**
**GF_LFC_UP_forward_MAX.csv,**
**GF_LFC_UP_counter_MAX.csv,**
**GF_LFC_DOWN_forward_MAX.csv,**
**GF_LFC_DOWN_counter_MAX.csv,**
**Tert_UP_forward_MAX.csv,**
**Tert_UP_counter_MAX.csv,**
**Tert_DOWN_forward_MAX.csv,**
**Tert_DOWN_counter_MAX.csv**


- 各連系線の各種融通調整量最大値を示す。
- 以下の3つの要素の組み合わせ数、つまり計8ファイルが必要となる。
  1. 短周期（GF&LFC成分）変動調整力か三次調整力か
  2. 上向き調整力か下向き調整力か
  3. 順方向か逆方向か
- 単位はMW。
- **setting_method_of_TTC_and_Margin**=`timeline`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる。

### 例
[data_set/data-example/tie/timeline/GF_LFC_UP_forward_MAX.csv](../../data_set/data-example/tie/timeline/GF_LFC_UP_forward_MAX.csv)

[data_set/data-example/tie/timeline/GF_LFC_UP_counter_MAX.csv](../../data_set/data-example/tie/timeline/GF_LFC_UP_counter_MAX.csv)

[data_set/data-example/tie/timeline/GF_LFC_DOWN_forward_MAX.csv](../../data_set/data-example/tie/timeline/GF_LFC_DOWN_forward_MAX.csv)

[data_set/data-example/tie/timeline/GF_LFC_DOWN_counter_MAX.csv](../../data_set/data-example/tie/timeline/GF_LFC_DOWN_counter_MAX.csv)

[data_set/data-example/tie/timeline/Tert_UP_forward_MAX.csv](../../data_set/data-example/tie/timeline/Tert_UP_forward_MAX.csv)

[data_set/data-example/tie/timeline/Tert_UP_counter_MAX.csv](../../data_set/data-example/tie/timeline/Tert_UP_counter_MAX.csv)

[data_set/data-example/tie/timeline/Tert_DOWN_forward_MAX.csv](../../data_set/data-example/tie/timeline/Tert_DOWN_forward_MAX.csv)

[data_set/data-example/tie/timeline/Tert_DOWN_counter_MAX.csv](../../data_set/data-example/tie/timeline/Tert_DOWN_counter_MAX.csv)


| time           | Tie-Line | ...  |
| :------------- | :------- | :--- |
| 2016/3/31 1:00 | 100      | ...  |
| 2016/3/31 2:00 | 100      | ...  |
| 2016/3/31 3:00 | 100      | ...  |
| ...            | ...      | ...  |


## 各時期連系線運用容量・マージン算出断面

**ファイル名: tie_calculation_section_day.csv, tie_calculation_section_of_the_clock.csv**

- 連系線の運用容量算出断面を示す。
- **setting_method_of_TTC_and_Margin**=`season`のときに用いられる。
- 月と平日か休日かを示した365日のデータを「tie_calculation_section_day.csv」に、昼か夜かの24時間のデータを「tie_calculation_section_of_the_clock.csv」に示す。つまり、計２ファイルが必要となる。

| インデックス              | 値         | 概要                                                                                     | tie_calculation_section_date | tie_calculation_section_of_the_clock |
| ------------------------- | ---------- | ---------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| day                       | yyyy/mm/dd | 日付                                                                                     | ✓                            | N.A.                                 |
| of_the_clock              | hh:mm:ss   | 時間                                                                                     | N.A.                         | ✓                                    |
| month_section             | 文字列     | 季節の区分を示す。tie_operation.csvのmonth_sectionに記載されている区分を用いなくてはいけない。 | ✓                            | N.A.                                 |
| of_the_clock_section_pre  | 文字列     | 時間帯を平日・休日の2つに区分する。<br />「weekday」: 平日、「holiday」: 休日            | ✓                            | N.A.                                 |
| of_the_clock_section_post | 文字列     | 時間帯を昼・夜の2つに区分する。<br />「day」: 昼、「night」: 夜                          | N.A.                         | ✓                                    |


### 例
[data_set/data-example/tie/season/tie_calculation_section_day.csv](../../data_set/data-example/tie/season/tie_calculation_section_day.csv)

| day       | month_section | of_the_clock_section_pre |
| :-------- | :------------ | :----------------------- |
| 2016/3/31 | Mar           | weekday                  |
| 2016/4/1  | Apr           | weekday                  |
| 2016/4/2  | Apr           | holiday                  |
| 2016/4/3  | Apr           | holiday                  |
| 2016/4/4  | Apr           | weekday                  |
| 2016/4/5  | Apr           | weekday                  |
| ...       | ...           | ...                      |


[data_set/data-example/tie/season/tie_calculation_section_of_the_clock.csv](../../data_set/data-example/tie/season/tie_calculation_section_of_the_clock.csv)

| of_the_clock | of_the_clock_section_post |
| :----------- | :------------------------ |
| 01:00:00     | night                     |
| 02:00:00     | night                     |
| 03:00:00     | night                     |
| 04:00:00     | night                     |
| 05:00:00     | night                     |
| 06:00:00     | night                     |
| 07:00:00     | night                     |
| 08:00:00     | night                     |
| 09:00:00     | day                       |
| 10:00:00     | day                       |
| 11:00:00     | day                       |
| 12:00:00     | day                       |
| 13:00:00     | day                       |
| 14:00:00     | day                       |
| 15:00:00     | day                       |
| 16:00:00     | day                       |
| 17:00:00     | day                       |
| 18:00:00     | day                       |
| 19:00:00     | day                       |
| 20:00:00     | day                       |
| 21:00:00     | day                       |
| 22:00:00     | day                       |
| 23:00:00     | night                     |
| 00:00:00     | night                     |

## エネルギー貯蔵システムの蓄電量計画運用 - E_R_plan -

**ファイル名: E_R_plan.csv**

- 各時間、各エネルギー貯蔵システムの蓄電量を計画値として制約に追加
- 単位は蓄電容量に対する割合[%]

### 例
[data_set/data-example/ESS/E_R_plan.csv](../../data_set/data-example/ESS/E_R_plan.csv)

| time          | 3IMAICH1 | 3AZUMI1 | 3KANN2 | 1KYOUGO1 | ...  |
| :------------ | :------- | :------ | :----- | :------- | :--- |
| 2016/4/1 0:00 | 26       | 26      | 26     | 26       | ...  |
| 2016/4/2 0:00 | 10       | 10      | 10     | 10       | ...  |
| 2016/4/3 0:00 | 50       | 50      | 50     | 50       | ...  |
| 2016/4/4 0:00 | 90       | 90      | 90     | 90       | ...  |
| 2016/4/5 0:00 | 74       | 74      | 74     | 74       | ...  |
| 2016/4/6 0:00 | 58       | 58      | 58     | 58       | ...  |
| 2016/4/7 0:00 | 42       | 42      | 42     | 42       | ...  |
| 2016/4/8 0:00 | 26       | 26      | 26     | 26       | ...  |
| ...           | ...      | ...     | ...    | ...      | ...  |

## 発電機の***N***日毎の発電量上限制約 - Maximum energy constraints -

**ファイル名: E_1_day_MAX.csv**

- 火力、原子力、水力発電機のN日毎の発電量上限値を設定
- "E\_***N***\_day_MAX.csv"の***N***の数字で、制約対象期間の長さを指定する（E_2_day_MAX.csv、E_3_day_MAX.csvなど）
  - N日間の発電量上限値は，燃料使用量や使用水量の上限を指定するために使用する。LNGタンクの容量や降水量などが制約値となる。
- 単位はMWh
- 1行A列は「start_day」であり、1行目には制約対象期間の始まりの日を指定する。
  - 例: E_3_day_MAX.csvでstart_dayが2016/4/1の行に記載されている値は、「2016/4/1から2016/4/3までの3日間の発電量上限値」を示している
- 空欄の場合、その日からの制約対象期間は考慮しない

### 例
[data_set/data-example/generation/E_1_day_MAX.csv](../../data_set/data-example/generation/E_1_day_MAX.csv)


| start_day | 3J-HYDR2 | 3SM-HYDR | 1J-HYDR2 | 1SM-HYDR | ...  |
| :-------- | :------- | :------- | :------- | :------- | :--- |
| 2016/3/31 | 15818.4  | 9711     | 6341.4   | 4914     | ...  |
| 2016/4/1  | 15818.4  | 2000     | 4500     | 3000     | ...  |
| 2016/4/2  | 15818.4  | 9711     | 6341.4   | 4914     | ...  |
| 2016/4/3  | 15818.4  | 9711     | 6341.4   | 4914     | ...  |
| 2016/4/4  | 15818.4  | 9711     | 6341.4   | 4914     | ...  |
| 2016/4/5  | 15818.4  | 9711     | 6341.4   | 4914     | ...  |
| ...       | ...      | ...      | ...      | ...      | ...  |

## その他の発電設備の出力値

**ファイル名: others.csv**

- 各地域、各時間における、その他の発電設備の出力値を示す
- 単位はMW


### 例
[data_set/data-example/others.csv](../../data_set/data-example/others.csv)

[data_set/data-mini/others.csv](../../data_set/data-mini/others.csv)


| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 125    | 167.4  | ...  |
| 2016/3/31 2:00 | 125    | 184.5  | ...  |
| 2016/3/31 3:00 | 125    | 200.1  | ...  |
| 2016/3/31 4:00 | 126    | 219.9  | ...  |
| ...            | ...    | ...    | ...  |
