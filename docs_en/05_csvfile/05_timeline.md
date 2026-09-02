# Time Series Data

CSV files with "time" in column A of the first row are treated as time series data.

- Column A represents the target time for values in subsequent columns. Time is expressed in Hour End notation, with a day represented from 1:00 to 0:00.
  - Example 1: "2040/8/2 1:00:00" refers to the period from 2040/8/2 0:00 to 1:00.
  - Example 2: "2040/8/3 0:00:00" refers to the period from 2040/8/2 23:00 to 8/3 0:00. **Note that data for 8/3 0:00 corresponds to 8/2.**

## Power Demand

**File name: demand.csv**

- demand.csv represents power demand for each area.
- Unit: MW.

### Example
[data_set/data-example/demand/demand.csv](../../data_set/data-example/demand/demand.csv)

[data_set/data-mini/demand/demand.csv](../../data_set/data-mini/demand/demand.csv)

| time           | Area_A      | Area_B      | ...  |
| :------------- | :---------- | :---------- | :--- |
| 2016/3/31 1:00 | 3516.309047 | 1755.790946 | ...  |
| 2016/3/31 2:00 | 3358.573043 | 1804.286827 | ...  |
| 2016/3/31 3:00 | 3315.617801 | 1854.290312 | ...  |
| ...            | ...         | ...         | ...  |

## Short-term Power Demand Variation (GF&LFC Component) Forecast Error Rate

**File name: demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv**

- demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv describe the short-term (GF&LFC component) variation forecast error rate of power demand for each area.
- Two files are required: one for up-reserve and one for down-reserve.
- Unit: Percentage of actual demand [%].

### Example

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

## Minimum Required System Inertia

**File name: demand_M_req.csv**

- demand_M_req.csv shows the minimum required system inertia for each area.
- Unit: Coefficient relative to actual demand [MW·s/MVA].

### Example
[data_set/data-example/demand/demand_M_req.csv](../../data_set/data-example/demand/demand_M_req.csv)

[data_set/data-mini/demand/demand_M_req.csv](../../data_set/data-mini/demand/demand_M_req.csv)

| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 1      | 1      | ...  |
| 2016/3/31 2:00 | 1      | 1      | ...  |
| 2016/3/31 3:00 | 1      | 1      | ...  |
| ...            | ...    | ...    | ...  |
## PV Output Actual Value


**File name: PV_ACT.csv**

- PV_ACT.csv shows the actual output value of PV generation for each area.
- Unit: Per unit capacity output (p.u.).

### Example

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

## PV Output Maximum Forecast Value

**File name: PV_FCST_U.csv**

## PV Output Forecast Value

**File name: PV_FCST_M.csv**

## PV Output Minimum Forecast Value

**File name: PV_FCST_L.csv**

- PV_FCST_L.csv represents the forecast output values of PV generation for each area.
- FCST_U data is treated as the maximum forecast value for day-ahead scheduling, FCST_M data as the forecast value for day-ahead scheduling, and FCST_L data as the minimum forecast value for day-ahead scheduling.
- Unit: Per unit capacity output (p.u.).

### Example
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

## PV Output Short-term Variation (GF&LFC Component) Forecast Error Rate

**File name: PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv**

- PV_R_GF_LFC_UP.csv and PV_R_GF_LFC_DOWN.csv describe the short-term (GF&LFC component) variation forecast error rate of PV generation for each area.
- Two files are required: one for up-reserve and one for down-reserve.
- Unit: Percentage relative to the value after subtracting suppression from generation [%].


### Example
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

## WF Output Actual Value

**File name: WF_ACT.csv**

- WF_ACT.csv shows the actual output value of WF generation for each area.
- Unit: Per unit capacity output (p.u.).

### Example

[data_set/data-example/WF/WF_ACT.csv](../../data_set/data-example/WF/WF_ACT.csv)

[data_set/data-mini/WF/WF_ACT.csv](../../data_set/data-mini/WF/WF_ACT.csv)

| time           | Area_A      | Area_B      | ...  |
| :------------- | :---------- | :---------- | :--- |
| 2016/3/31 1:00 | 0.293882979 | 0.321685393 | ...  |
| 2016/3/31 2:00 | 0.233297872 | 0.314494382 | ...  |
| 2016/3/31 3:00 | 0.161595745 | 0.313033708 | ...  |
| 2016/3/31 4:00 | 0.122340426 | 0.328876404 | ...  |
| ...            | ...         | ...         | ...  |

## WF Output Maximum Forecast Value

**File name: WF_FCST_U.csv**

## WF Output Forecast Value

**File name: WF_FCST_M.csv**

## WF Output Minimum Forecast Value

**File name: WF_FCST_L.csv**

- WF_FCST_L.csv represents the forecast output values of WF generation for each area.
- FCST_U data is treated as the maximum forecast value for day-ahead scheduling, FCST_M data as the forecast value for day-ahead scheduling, and FCST_L data as the minimum forecast value for day-ahead scheduling.
- Unit: Per unit capacity output (p.u.).

### Example
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

## WF Output Short-term Variation (GF&LFC Component) Forecast Error Rate

**File name: WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv**

- WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv show the short-term (GF&LFC component) variation forecast error rate of WF generation for each area.
- Two files are required: one for up-reserve and one for down-reserve.
- Unit: Percentage relative to the value after subtracting suppression from generation [%].


### Example
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

## Tie Line Operation Capacity and Margin

**File name: TTC_forward.csv, TTC_counter.csv, Margin_forward.csv, Margin_counter.csv**

- TTC_forward.csv, TTC_counter.csv, Margin_forward.csv, Margin_counter.csv describe the forward and counter direction operation capacity and margin for each tie line.
- Unit: MW.
- Used when **setting_method_of_TTC_and_Margin**=`timeline`.

### Example
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

## Maximum Interchange Adjustment Amount

**File name:**
**GF_LFC_UP_forward_MAX.csv,**
**GF_LFC_UP_counter_MAX.csv,**
**GF_LFC_DOWN_forward_MAX.csv,**
**GF_LFC_DOWN_counter_MAX.csv,**
**Tert_UP_forward_MAX.csv,**
**Tert_UP_counter_MAX.csv,**
**Tert_DOWN_forward_MAX.csv,**
**Tert_DOWN_counter_MAX.csv**


- These csv files represent the maximum interchange adjustment amount for each type of control capacity in forward and counter directions for each tie line.
- Unit: MW.
- Used when **setting_method_of_TTC_and_Margin**=`timeline` and **consider_maximum_reserve_constraint_for_tie**=`true`.

### Example
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


## Calculation Sections of Tie Line Operation Capacity and Margin for Each Period

**File name: tie_calculation_section_day.csv, tie_calculation_section_of_the_clock.csv**

- Indicates the seasonal classification for setting the tie line operation capacity.
- Used when **setting_method_of_TTC_and_Margin**=`season`.
- The 365-day data indicating the month and whether each day is a weekday or holiday is provided in tie_calculation_section_day.csv, and the 24-hour data indicating whether the time is day or night is provided in tie_calculation_section_of_the_clock.csv. That is, two files in total are required.

| Index              | Value         | Summary                                                                                     | tie_calculation_section_date | tie_calculation_section_of_the_clock |
| ------------------------- | ---------- | ---------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------ |
| day                       | yyyy/mm/dd | Date                                                                                     | ✓                            | N.A.                                 |
| of_the_clock              | hh:mm:ss   | Hours.                                                                                     | N.A.                         | ✓                                    |
| month_section             | character string     | Indicates the division of the season; the division listed in month_section of tie_operation.csv must be used. | ✓                            | N.A.                                 |
| of_the_clock_section_pre  | character string     | Time zones are divided into two categories: weekdays and holidays.<br />"weekday": Weekdays, "holiday": holiday            | ✓                            | N.A.                                 |
| of_the_clock_section_post | character string     | Divide the time of day into two time periods: day and night.<br />"day":Noon, "night": evening                          | N.A.                         | ✓                                    |


### Example
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

## Energy Storage System Planned Storage Amount

**File name: E_R_plan.csv**

- E_R_plan.csv adds constraints for the planned storage amount of each energy storage system at each time period.
- Unit: Percentage of storage capacity [%].

### Example
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

## Generator's N-day Maximum Energy Output Constraints

**File name: E_1_day_MAX.csv**

- E_1_day_MAX.csv sets N-day maximum energy output for thermal, nuclear, and hydroelectric generators.
- The number ***N*** in "E\_***N***\_day_MAX.csv" specifies the constraint period length (e.g., E_2_day_MAX.csv, E_3_day_MAX.csv).
  - N-day maximum energy output is used to specify upper limits for fuel consumption or water usage. Constraints may be based on factors such as LNG tank capacity or precipitation amount.
- Unit: MWh.
- Column A in row 1 is "start_day" and specifies the start date of the constraint period.
  - Example: In E_3_day_MAX.csv, a value in the row with start_day 2016/4/1 indicates "the maximum energy output for the 3-day period from 2016/4/1 to 2016/4/3".
- If blank, the constraint period starting from that date is not considered.

### Example
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

## Output of Other Generation Facilities

**File name: others.csv**

- others.csv shows the output values of other generation facilities for each area and time period.
- Unit: MW.


### Example
[data_set/data-example/others.csv](../../data_set/data-example/others.csv)

[data_set/data-mini/others.csv](../../data_set/data-mini/others.csv)


| time           | Area_A | Area_B | ...  |
| :------------- | :----- | :----- | :--- |
| 2016/3/31 1:00 | 125    | 167.4  | ...  |
| 2016/3/31 2:00 | 125    | 184.5  | ...  |
| 2016/3/31 3:00 | 125    | 200.1  | ...  |
| 2016/3/31 4:00 | 126    | 219.9  | ...  |
| ...            | ...    | ...    | ...  |
