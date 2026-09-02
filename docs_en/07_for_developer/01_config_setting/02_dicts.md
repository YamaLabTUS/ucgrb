# Setting options for dictionary type data creation

### make_area_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether the class "UCDicts" generates the list of areas "area" and the parameter value "area_para" for each value.

### make_generation_type_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the "generation_type" list of generator types and various parameter values "generation_type_para" are generated in the class "UCDicts".

### make_generation_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines if the class "UCDicts" will generate a list of generators "generation" and parameter values "generation_para" for each generator.

### make_ess_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables that determine if the class "UCDicts" will generate a list of energy storage systems "ess" and parameter values "ess_para" for each energy storage system.

### make_tie_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the list of interconnection lines "tie" and the parameter value "tie_para" for each line are generated in the class "UCDicts".

### make_whole_timeline_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether to generate a 'whole_timeline' time series for all optimization targets and a 'daily_whole_timeline' that stores the time series separately for each day in the class 'UCDicts'.

### make_demand_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not the class "UCDicts" generates a time-series list of electricity demand "demand" and parameter values "demand_para" for each time period and area.

### make_pv_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines if the class "UCDicts" generates a time series list of PV "pv" and parameter values "pv_para" for each time period and area.

### make_wf_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not the class "UCDicts" generates a time series list of wind power "wf" and parameter values "wf_para" for each time period and area.

### make_tie_operation_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether the class "UCDicts" generates the list of interconnection line operations "tie_operation" and the parameter values "tie_operation_para" for each operation.

### make_maintenance_dicts

- **Type: Boolean value**
- **default value: `True`**

In the class "UCDicts", a variable that determines whether or not a planned outage time series is created from the data of the repair period and stored in the "planned_outage" of uc_data.

### make_planned_outage_dicts

- **Type: Boolean value**
- **default value: `True`**

In class "UCDicts", a variable that determines whether the timeline of planned outages is created and stored in "planned_outage" or not.

### make_descent_dicts

- **Type: Boolean value**
- **default value: `True`**

In the class "UCDicts", a variable that determines whether or not to create a timeline of output degradation and store it in "P_des".

### make_e_ess_plan_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables in class "UCDicts" that determine whether or not to generate dictionary type data for operating constraints of stored energy schedule of energy storage system.


### make_others_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to generate output time series lists for other generating facilities in the class "UCDicts".

### make_timeline_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to generate the time series 'timeline' to be optimized each time in the class 'UCDicts'.

### update_pv_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables in the class "UCDicts" that determine whether or not to generate the required PV data (output values, maximum predicted values, minimum predicted values) for each round of optimization.

### update_wf_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables in the class "UCDicts" that determine whether or not to generate the necessary wind power data (output values, maximum predicted values, minimum predicted values) for each round of optimization.

### make_max_energy_dicts

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to generate dictionary type data regarding the upper generation limit constraint for every N days in the class "UCDicts".

### make_constants_depend_on_scheduling_kind_dicts

- **Type: Boolean value**
- **default value: `True`**

Variables in the class "UCDicts" that determine whether or not to generate constants that are determined dependent on the type of plan.

### calculate_C_coef

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not a output proportionality coefficient in fuel cost function is generated from the Fuel cost proportionality coefficient and the Internal consumption rate in the class "UCDicts".

### calculate_P_MAX

- **Type: Boolean value**
- **default value: `True`**

Variables in class "UCDicts" that determine whether or not the maximum output at the transmission end is generated from the maximum output at the generation end and the Internal consumption rate.

### calculate_P_MIN

- **Type: Boolean value**
- **default value: `True`**

Variables in class "UCDicts" that determine whether or not the minimum transmission end output is generated from the minimum generation end output and the Internal consumption rate.

### calculate_C_coef_CO2

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to generate CO2 emissions per unit output in the class "UCDicts".

### calculate_C_intc_CO2

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to generate CO2 emissions per unit time in the class "UCDicts".

### calculate_C_startup_CO2

- **Type: Boolean value**
- **default value: `True`**

Variables in class "UCDicts" that determine whether or not to generate CO2 emissions per startup.

### calculate_Min_Up_Time

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to modify the minimum up time to match the optimization time granularity in the class "UCDicts".

### calculate_Min_Down_Time

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to modify the minimum down time to match the optimization time granularity in the class "UCDicts".
