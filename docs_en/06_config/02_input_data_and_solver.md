# Optional settings for input data and solver

## Name of the configuration file

### config_name

- **Type: string**

The name provided to identify the configuration file.

**Example: If you want to name the configuration file "Case_A"**

```yaml
config_name: "Case_A"
```

## Optional values for input data

### csv_data_dir

- **Type: string or array**

- **default value: `"data"`**

Directory path containing power system data written in CSV format. Multiple directories can be specified in list format.

**Example: When CSV data is stored in separate directories "data1" and "data2"**

```yaml
csv_data_dir:
  - "data1"
  - "data2"
```

### time_series_granularity

- **Type: numeral**

- **default value: `60`**

Optimization time granularity. Expressed in minutes. If it is 60 or less, it must be a divisor of 60.
If the value is greater than 60, it must be a divisor or multiple of 1440 (minutes in 24 hours).

### time_series_to_be_linearly_interpolated

- **Type: array**

- **default value: `["demand", "PV_ACT", "PV_FCST_L", "PV_FCST_M", "PV_FCST_U", "WF_ACT", "WF_FCST_L", "WF_FCST_M", "WF_FCST_U", "others"]`**

If the input time series is coarser than the set time granularity, interpolation is automatically performed. Specify the time series name for which the interpolation method is linear.
Time series not specified in this item will be rectangular interpolation.

**Example:**

```yaml
time_series_to_be_linearly_interpolated:
    - "demand"
    - "PV_ACT"
    - "PV_FCST_L"
    - "PV_FCST_M"
    - "PV_FCST_U"
    - "WF_ACT"
    - "WF_FCST_L"
    - "WF_FCST_M"
    - "WF_FCST_U"
    - "others"
```

or

```yaml
time_series_to_be_linearly_interpolated: ["demand", "PV_ACT", "PV_FCST_L", "PV_FCST_M", "PV_FCST_U", "WF_ACT", "WF_FCST_L", "WF_FCST_M", "WF_FCST_U", "others"]
```

### time_series_not_to_be_interpolated

- **Type: array**

- **default value: `["E_R_plan"]`**

If the input time series is coarser than the set time granularity, interpolation is automatically performed. Specify the time series name for which interpolation is not performed.
Time series not specified in this item will be rectangular or linear interpolation.

**Example:**

```yaml
time_series_not_to_be_interpolated:
    - "E_R_plan"
```

or

```yaml
time_series_not_to_be_interpolated: ["E_R_plan"]
```

### areas

- **Type: string or array**

- **default value: `"ALL"`**

areas show an array of areas to be optimized; if you want to target all areas listed in the CSV data, enter `ALL`.

### nuclear_and_thermal_generation_type

- **Type: string or array**

- **default value: `["NUCL", "COAL", "GAS", "OIL"]`**

Type names corresponding to nuclear and thermal generators.

### nuclear_generation_type

- **Type: string or array**

- **default value: `["NUCL"]`**

The name of the type corresponding to a nuclear power generator.

### hydro_generation_type

- **Type: string or array**

- **default value: `["HYDRO"]`**

Name of the type corresponding to a hydroelectric generator.

**Example:**

```yaml
areas:
    - "Hokkaido"
    - "Tohoku"
    - "Tokyo"
    - "Chubu"
    - "Hokuriku"
    - "Kansai"
    - "Chugoku"
    - "Shikoku"
    - "Kyushu"
```

or

```yaml
areas: ["Hokkaido", "Tohoku", "Tokyo", "Chubu", "Hokuriku", "Kansai", "Chugoku", "Shikoku", "Kyushu"]
```

### setting_method_of_TTC_and_Margin

- **Type: string**
- **default value: `"fixed"`**

Variable that determines how the operational capacity and margin of the tie line are considered. The following three types can be selected.

- `"fixed"` : Fixed value for the whole period (default value)
- `"season"`: Specify by month or time zone
- `"timeline"`: Set by optimization time granularity

## Gurobi Solver parameter settings

### grb_MIPGap

- **Type: numeral**

- **default value: `0.01`**

Setting of the Gurobi model parameter MIP optimization relative gap "[MIPGap](https://www.gurobi.com/documentation/9.5/refman/mipgap.html)".

### grb_MIPGapAbs

- **Type: numeral**

- **default value: `0.01`**

Setting of the Gurobi model parameter MIP optimization absolute gap "[MIPGapAbs](https://www.gurobi.com/documentation/9.5/refman/mipgapabs.html)".

### grb_IntegralityFocus

- **Type: numeral**

- **default value: `1`**

Setting of the Gurobi model parameter integrality focus "[IntegralityFocus](https://www.gurobi.com/documentation/9.5/refman/integralityfocus.html)".

### grb_FeasibilityTol

- **Type: numeral**

- **default value: `1.0e-6`**

Setting of the Gurobi model parameter Feasibility Tolerance "[FeasibilityTol](https://www.gurobi.com/documentation/9.5/refman/feasibilitytol.html)".

### grb_FeasibilityTol_for_Pi_calc

- **Type: numeral**

- **default value: `1.0e-5`**

Setting of the Gurobi model parameter Feasibility Tolerance for shadow price calculation "[FeasibilityTol](https://www.gurobi.com/documentation/9.5/refman/feasibilitytol.html)".

### grb_NodefileStart

- **Type: numeral**

- **default value: half of the physical memory of the running computer (GB)**

Setting of the Gurobi model parameter Node file start (the amount of memory at which MIP nodes begin to be written to disk) "[NodefileStart](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#nodefilestart)".

The default value is set by automatically detecting the physical memory on each of the Windows, Mac, and Linux operating systems and using half of that value (in GB). If physical memory detection fails, 8.0 GB is used as the default value.

### grb_Threads

- **Type: integer**

- **default value: `0` (automatic setting)**

Setting of the Gurobi model parameter number of CPU threads "[Threads](https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html#threads)".

If `0` is specified, Gurobi automatically detects and uses the number of available CPU cores.
