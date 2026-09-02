# Generator Data

> **Note**: The items on this page such as ΔkW / kWh / p^id are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

## Power Generator

**File name: generation.csv**

- Generation.csv describes the characteristics of each generator
- The data of hydroelectric generators and other generators are described into different tables because these generators require different types of data.
- The **`Used in delta-kW-bid`** column of the table indicates whether the item is exclusive to the ΔkW-value version (`formulation_type: "delta-kW-bid"`) (`✓ (only)`) or common to both modes (`Common`). Columns marked `✓ (only)` are not read in `delta-kW-no-market` (default); when `delta-kW-bid` is specified and the column is absent, it is filled with the default value stated in each row's Summary (e.g., `C_fuel_kWh_UP` becomes `C_fuel`, `C_fuel_kWh_DOWN` becomes `-1 × C_fuel`, and the other ΔkW/kWh columns become `0`).

| Index                                                                                                    | Value                                                               | Summary                                                                                                                                                                              | thermal or nuclear | hydro | Used in delta-kW-bid |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ----- | :------------------: |
| g_type                                                                                                   | character string                                                    | Power source type (must match g_type entries in generation_type.csv)                                                                                                               | ✓                  | ✓     | Common               |
| name                                                                                                     | character string                                                    | Generator name (including ESS, no duplicates allowed)<br />**Note**: Only ASCII characters (alphanumeric characters and symbols) are allowed. Non-ASCII characters such as Japanese are not allowed.                                                                                                                              | ✓                  | ✓     | Common               |
| P_MAX                                                                                                    | numeral                                                             | Maximum output (Transmission end)[MW]                                                                                                                                               | N.A.               | ✓     | Common               |
| P_MAX_GENE_END                                                                                           | numeral                                                             | Maximum output (Generating end)[MW]                                                                                                                                                | ✓                  | N.A.  | Common               |
| P_MIN                                                                                                    | numeral                                                             | Minimum output (Transmission end)[MW]                                                                                                                                               | N.A.               | ✓     | Common               |
| P_MIN_GENE_END                                                                                           | numeral                                                             | Minimum output (Generating end)[MW]                                                                                                                                                | ✓                  | N.A.  | Common               |
| C_fuel                                                                                                   | numeral                                                             | Coefficient of fuel cost function [Thousands of yen/MWh]                                                                                                                           | ✓                  | N.A.  | Common               |
| C_intc                                                                                                   | numeral                                                             | No-load cost [Thousands of yen/hour]                                                                                                                                               | ✓                  | N.A.  | Common               |
| Min_Up_Time                                                                                              | numeral                                                             | Minimum up time [hour]                                                                                                                                                             | ✓                  | N.A.  | Common               |
| Min_Down_Time                                                                                            | numeral                                                             | Minimum down time [hour]                                                                                                                                                           | ✓                  | N.A.  | Common               |
| C_startup                                                                                                | numeral                                                             | Startup cost [Thousands of yen]                                                                                                                                                    | ✓                  | N.A.  | Common               |
| ICR                                                                                                      | numeral                                                             | Internal consumption rate [%]                                                                                                                                                      | ✓                  | N.A.  | Common               |
| R_GF_LFC_MAX                                                                                             | numeral                                                             | Maximum reserve capacity [%MW]                                                                                                                                            | ✓                  | ✓     | Common               |
| R_RAMP_MAX                                                                                               | numeral                                                             | Output change rate constraint [%MW/min]                                                                                                                                            | ✓                  | ✓     | Common               |
| area                                                                                                     | character string                                                    | Name of the area where installed                                                                                                                                                  | ✓                  | ✓     | Common               |
| maintenance\_**_N_** <br />(**_N_** is an integer of one or more digits: maintenance_1, maintenance_2,...) | Start month and date 4 digits(MMDD)-End month and date 4 digits（MMDD）<br />（notation example: 0401-0525） | Maintenance period<br />（If blank or not in accordance with the left cell notation, maintenance will not be performed）<br />Identical to the all-day outage designation in planned outage described below | ✓                  | N.A.  | Common               |
| HR_MIN                                                                                                   | numeral                                                             | Heat rate (at minimum output) [Mcal/MWh]                                                                                                                                           | ✓                  | N.A.  | Common               |
| HR_MAX                                                                                                   | numeral                                                             | Heat rate (at maximum output)[Mcal/MWh]                                                                                                                                            | ✓                  | N.A.  | Common               |
| M                                                                                                        | numeral                                                             | Per-unit inertia constant [MW$\cdot$s/MVA]                                                                                                                                                  | ✓                  | N.A.  | Common               |
| C_Delta_kW_UP                                                                                            | numeral                                                             | Up-direction reserve capacity (ΔkW) unit price [Thousands of yen/MWh/h] <br />If the column does not exist, 0 is entered as the initial value                                       | ✓                  | ✓     | ✓ (only)             |
| C_Delta_kW_DOWN                                                                                          | numeral                                                             | Down-direction reserve capacity (ΔkW) unit price [Thousands of yen/MWh/h] <br />If the column does not exist, 0 is entered as the initial value                                     | ✓                  | ✓     | ✓ (only)             |
| C_fuel_kWh_UP                                                                                            | numeral                                                             | Up-direction reserve energy (kWh) unit price for thermal and nuclear [Thousands of yen/MWh] <br />For thermal and nuclear, the value before considering the internal consumption rate is entered<br />If the column does not exist, C_fuel is entered   | ✓                  | N.A.  | ✓ (only)             |
| C_fuel_kWh_DOWN                                                                                          | numeral                                                             | Down-direction reserve energy (kWh) unit price for thermal and nuclear [Thousands of yen/MWh] <br />For thermal and nuclear, the value before considering the internal consumption rate is entered<br />If the column does not exist, -1 × C_fuel is entered | ✓                  | N.A.  | ✓ (only)             |
| C_kWh_UP                                                                                                 | numeral                                                             | Up-direction reserve energy (kWh) unit price for hydro [Thousands of yen/MWh] <br />If the column does not exist, 0 is entered                                                      | N.A.               | ✓     | ✓ (only)             |
| C_kWh_DOWN                                                                                               | numeral                                                             | Down-direction reserve energy (kWh) unit price for hydro [Thousands of yen/MWh] <br />If the column does not exist, 0 is entered                                                    | N.A.               | ✓     | ✓ (only)             |

#### Detailed explanation of reserve cost-related columns

**Difference between reserve capacity (ΔkW) and reserve energy (kWh)**

- **Reserve capacity (ΔkW)**: Charged against the capacity (kW) of the reserve. The unit price when a generator or ESS secures reserve capacity.
- **Reserve energy (kWh)**: Charged against the energy actually generated, or the energy whose generation is suppressed (kWh). Charged against the actual variation in energy.

**Reserve energy of thermal and nuclear generators**

- `C_fuel_kWh_UP`: The unit price when a thermal or nuclear generator provides up-direction reserve energy. Charged against the energy actually generated (kWh). For thermal and nuclear generators, the value before considering the internal consumption rate is entered.
- `C_fuel_kWh_DOWN`: The unit price when a thermal or nuclear generator provides down-direction reserve energy. Charged against the energy whose generation is actually suppressed (kWh). For thermal and nuclear generators, the value before considering the internal consumption rate is entered.

**Reserve energy of hydro generators**

- `C_kWh_UP`: The unit price when a hydro generator provides up-direction reserve energy. Charged against the energy actually generated (kWh).
- `C_kWh_DOWN`: The unit price when a hydro generator provides down-direction reserve energy. Charged against the energy whose generation is actually suppressed (kWh).

### Example

[data_set/data-example/generation/generation\_\_01_thermal.csv](../../data_set/data-example/generation/generation__01_thermal.csv)

[data_set/data-example/generation/generation\_\_02_nuclear.csv](../../data_set/data-example/generation/generation__02_nuclear.csv)

[data_set/data-example/generation/generation\_\_03_hydro.csv](../../data_set/data-example/generation/generation__03_hydro.csv)

[data_set/data-mini/generation/generation.csv](../../data_set/data-mini/generation/generation.csv)

| g_type | name   | P_MAX_GENE_END | P_MIN_GENE_END | C_fuel      | C_intc      | Min_Up_Time | Min_Down_Time | C_startup | ICR  | R_GF_LFC_MAX | area   | maintenance_1 | HR_MIN  | HR_MAX  | M   |
| :----- | :----- | :------------- | :------------- | :---------- | :---------- | :---------- | :------------ | :-------- | :--- | :----------- | :----- | :------------ | :------ | :------ | :-- |
| COAL   | COAL_A | 1000           | 300            | 2.923872003 | 271.865997  | 4           | 8             | 1500      | 2    | 5            | Area_A |               | 2397    | 2000    | 8   |
| GAS    | LNG_A  | 685            | 274            | 8.456009136 | 1475.527266 | 1           | 4             | 166.68    | 1.83 | 5            | Area_A |               | 2043.52 | 1566.48 | 8   |
| COAL   | COAL_B | 700            | 105            | 2.960482807 | 163.8621239 | 4           | 8             | 728       | 5    | 5            | Area_B |               | 2829.44 | 1999.27 | 8   |
| GAS    | LNG_B  | 569            | 228            | 8.511733471 | 1238.270164 | 1           | 4             | 154.36    | 2    | 5            | Area_B |               | 2058.52 | 1577.98 | 8   |
| ...    | ...    | ...            | ...            | ...         | ...         | ...         | ...           | ...       | ...  | ...          | ...    | ...           | ...     | ...     | ... |

###

## Generator Type

**File name: generation_type.csv**

- generation_type.csv records the characteristics that each generator type has.

| Index                    | Value                   | Summary                                                                     |
| :----------------------- | ----------------------- | --------------------------------------------------------------------------- |
| g_type                   | character string        | Power source type (no duplicates allowed)                                   |
| EF                       | numeral                 | Emission factor [tCO2/kl or t]<br />OIL is kl, GAS and COAL are t           |
| fuel_cnsmp_per_unit_Mcal | numeral                 | Fuel consumption per unit calorific value [kl or t/Mcal]<br />OIL is kl, GAS and COAL are t |
| EF_startup               | numeral                 | Startup emission factor [tCO2/kl]                                           |
| fuel_price_startup       | numeral                 | Fuel unit price at startup [Thousands of yen/kl or t]                       |
| kind                     | hydro, nuclear, thermal | Type specification (whether hydro, nuclear, or thermal)                     |

### Example

[data_set/data-example/generation/generation_type.csv](../../data_set/data-example/generation/generation_type.csv)

[data_set/data-mini/generation/generation_type.csv](../../data_set/data-mini/generation/generation_type.csv)

| name  | EF   | fuel_cnsmp_per_unit_Mcal | EF_startup | fuel_price_startup | kind    |
| :---- | :--- | :----------------------- | :--------- | :----------------- | :------ |
| HYDRO |      |                          |            |                    | hydro   |
| NUCL  |      |                          |            |                    | nuclear |
| COAL  | 2.33 | 0.0001628                | 2.71       | 133.46             | thermal |
| GAS   | 2.7  | 0.00007663               | 2.71       | 133.46             | thermal |
| OIL   | 2.62 | 0.0001095                | 2.71       | 133.46             | thermal |
| ...   | ...  | ...                      | ...        | ...                |         |

## Energy Storage Systems

**File name: ESS.csv**

- ESS.csv describes settings for each energy storage system.

| Index           | Value            | Summary                                                                                                                        |
| :-------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| name            | character string | Generator name (including generators, no duplicates allowed)<br />**Note**: Only ASCII characters (alphanumeric characters and symbols) are allowed. Non-ASCII characters such as Japanese are not allowed.                                                                   |
| E_CAP           | numeral          | Storage capacity [MWh]                                                                                                          |
| P_d_MAX         | numeral          | Maximum power generation capacity [MW]                                                                                          |
| P_d_MIN         | numeral          | Minimum power generation capacity [MW]                                                                                          |
| P_c_MAX         | numeral          | Maximum charging capacity [MW]                                                                                                  |
| P_c_MIN         | numeral          | Minimum charging capacity [MW]                                                                                                  |
| R_GF_LFC_MAX    | numeral          | Maximum reserve capacity [%]                                                                                           |
| area            | character string | Name of the area where installed                                                                                               |
| E_R_MAX         | numeral          | Storage upper limit [%]                                                                                                         |
| E_R_MIN         | numeral          | Storage lower limit [%]                                                                                                         |
| E_R_base        | numeral          | Time boundary condition value for energy storage [%]                                                                           |
| eta             | numeral          | Overall efficiency during power generation operation [%]                                                                        |
| gamma           | numeral          | Overall efficiency during energy storage operation [%]                                                                         |
| M               | numeral          | Per-unit inertia constant [MW$\cdot$s/MVA]                                                                                              |
| C_ess_short     | numeral          | Penalty factor for storage capacity shortage [Thousands of yen/KWh]                                                             |
| C_ess_surplus   | numeral          | Penalty factor for storage capacity surplus [Thousands of yen/KWh]                                                             |
| C_Delta_kW_UP   | numeral          | Up-direction reserve capacity (ΔkW) unit price [Thousands of yen/MWh/h] <br />If the column does not exist, 0 is entered as the initial value   |
| C_Delta_kW_DOWN | numeral          | Down-direction reserve capacity (ΔkW) unit price [Thousands of yen/MWh/h] <br />If the column does not exist, 0 is entered as the initial value |
| C_kWh_UP        | numeral          | Up-direction reserve energy (kWh) unit price [Thousands of yen/MWh] <br />If the column does not exist, 0 is entered as the initial value        |
| C_kWh_DOWN      | numeral          | Down-direction reserve energy (kWh) unit price [Thousands of yen/MWh] <br />If the column does not exist, 0 is entered as the initial value      |

#### Detailed explanation of ESS reserve energy

The ESS reserve energy (`C_kWh_UP`, `C_kWh_DOWN`) is calculated as the difference from the day-ahead plan.

**`C_kWh_UP` (up-direction reserve energy)**

- If the day-ahead plan was generation (discharge): the amount by which the actual discharge exceeds the day-ahead planned discharge.
- If the day-ahead plan was charging: the amount by which the actual charge is reduced below the day-ahead planned charge (suppression of charging). In addition, the amount actually generated (discharged) is also included (planned charge amount + actual generation amount).

**`C_kWh_DOWN` (down-direction reserve energy)**

- If the day-ahead plan was charging: the amount by which the actual charge exceeds the day-ahead planned charge.
- If the day-ahead plan was generation (discharge): the amount by which the actual discharge is reduced below the day-ahead planned discharge (suppression of discharging). In addition, the amount actually charged is also included (planned generation amount + actual charge amount).

### Example

[data_set/data-example/ESS/ESS.csv](../../data_set/data-example/ESS/ESS.csv)

[data_set/data-mini/ESS.csv](../../data_set/data-mini/ESS.csv)

| name           | E_CAP | P_d_MAX | P_d_MIN | P_c_MAX | P_c_MIN | R_GF_LFC_MAX | area   | E_R_MAX | E_R_MIN | E_R_base | eta    | gamma  | M   | C_ess_short | C_ess_surplus |
| :------------- | :---- | :------ | :------ | :------ | :------ | :----------- | :----- | :------ | :------ | :------- | :----- | :----- | :-- | :---------- | :------------ |
| PUMPED_HYDRO_A | 2800  | 350     | 175     | 350     | 350     | 20           | Area_A | 90      | 10      | 50       | 83.666 | 83.666 | 8   | 10000       | 10000         |
| PUMPED_HYDRO_B | 1600  | 200     | 100     | 230     | 120     | 20           | Area_B | 90      | 10      | 50       | 83.666 | 83.666 | 8   | 10000       | 10000         |
| ...            | ...   | ...     | ...     | ...     | ...     | ...          | ...    | ...     | ...     | ...      | ...    | ...    | ... | ...         | ...           |

## Planned Outage

**File name: planned_outage.csv**

- planned_outage.csv represents planned shutdowns of large generators or ESS.
- start_time and end_time are expressed in minutes. Note that this differs from the Hour end notation of the optimization time series. Conversion is performed within "ucgrb".

  - Example: If you want to stop between 2:00~4:00 in Hour end notation
    - start_time: 30 minutes before and after 1:00 (0:30~1:29)
    - end_time: 30 minutes before and after 4:00 (3:30~4:29)

   <img src="../img/05/just_time_hour_end.png" width="700" alt="Just time and hour end">

| Index      | Value            | Summary                          |
| ---------- | ---------------- | -------------------------------- |
| name       | character string | Name of target generator or ESS<br />**Note**: Only ASCII characters (alphanumeric characters and symbols) are allowed. Non-ASCII characters such as Japanese are not allowed.  |
| start_time | YYYY/MM/DD HH:MM | Planned outage start time        |
| end_time   | YYYY/MM/DD HH:MM | Planned outage end time          |

### Example

[data_set/data-example/planned_outage.csv](../../data_set/data-example/planned_outage.csv)

| name    | start_time     | end_time       |
| :------ | :------------- | :------------- |
| 3SODEG1 | 2016/4/1 1:00  | 2016/4/2 0:00  |
| 3SODEG1 | 2016/4/3 1:00  | 2016/4/4 0:00  |
| 3SOGA   | 2016/4/2 11:00 | 2016/4/3 18:00 |
| ...     | ...            | ...            |

## Power Decrease

**CSV file name: descent.csv**

- Represents output reduction of large generators or ESS.
- For ESS, the maximum value is reduced for both generation and charging capacity.
- If output reduction is specified for the same generator (or ESS) during the same time period, the setting with the larger reduction takes priority.
- start_time and end_time are expressed in minutes. Note that this differs from the Hour end notation of the optimization time series. On "ucgrb", it is calculated as the average value within a unit time.
  - Example: If output is reduced by 100 MW between 2:30~4:15
    - Output reduction at 3:00: **50MW**
      - (0MW × 30 min + 100MW × 30 min) / 60 min
    - Output reduction at 4:00: **100MW**
    - Output reduction at 5:00: **25MW**
      - (100MW × 15 min + 0MW × 45 min) / 60 min

| Index      | Value            | Summary                          |
| ---------- | ---------------- | -------------------------------- |
| name       | character string | Name of target generator or ESS<br />**Note**: Only ASCII characters (alphanumeric characters and symbols) are allowed. Non-ASCII characters such as Japanese are not allowed.  |
| P_des      | numeral          | Output reduction amount [MW]     |
| start_time | YYYY/MM/DD HH:MM | Planned reduction start time     |
| end_time   | YYYY/MM/DD HH:MM | Planned reduction end time       |

### Example

[data_set/data-example/descent.csv](../../data_set/data-example/descent.csv)

| name     | P_des | start_time     | end_time       |
| :------- | :---- | :------------- | :------------- |
| 3ISOGN2L | 300   | 2016/4/1 9:00  | 2016/4/1 20:00 |
| 3JFEOG1A | 100   | 2016/4/1 17:20 | 2016/4/2 17:44 |
| 3JFEOG1A | 1000  | 2016/4/2 1:00  | 2016/4/3 1:00  |
| ...      | ...   | ...            | ...            |
