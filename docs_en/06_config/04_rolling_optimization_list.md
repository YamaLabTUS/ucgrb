# Rolling optimization list settings

There are two ways to configure the optimization list.

## Configuration method 1 -Direct description-

### rolling_opt_list

- **required fields**
- **Type: List format**

The settings for each round of optimization to be performed are described in list form.

The elements to be described in the list are as follows.

#### name

- **required fields**

- **Type: character string**

Name of the optimization to be performed.

#### start_time

- **required fields**
- **Type: `"YYYY-MM-DD hh:mm:ss"`**

Start time of the period to be optimized.

#### end_time

- **required fields**
- **Type: `"YYYY-MM-DD hh:mm:ss"`**

End time of the period to be optimized.

#### pre_period_hours

- **required fields**
- **Type: numeral**

The period for which the decision variables are prepared before the period to be optimized. Unit: hours.

#### pv_value

- **required fields**
- **Type: dictionary type**
  - **index: `"YYYY-MM-DD hh:mm:ss"`**
  - **value: `"ACT"` or `"FCST"`**

Select whether the PV output value for the time period on and after the index should be the actual output value (`"ACT"`) or the predicted value (`"FCST"`).

#### wf_value

- **required fields**
- **Type: dictionary type**
  - **index: `"YYYY-MM-DD hh:mm:ss"`**
  - **value: `"ACT"` or `"FCST"`**

Select whether the WF output value for the time period on and after the index should be the actual output value (`"ACT"`) or the predicted value (`"FCST"`).

#### E_MAX_start_time

- **Type: `"YYYY-MM-DD hh:mm:ss"`**

The time at which the every-N-days upper limit constraint on the power generation of large generators begins to be considered.

If this item is not specified, it shall be the first time of the day (1:00 when the time granularity is 1 hour), including the inherited period before the period to be optimized.

Example: Optimization period: April 30, 13:00 - May 2, 0:00, inherited period before the optimization period: 24 hours
→ Start time to take the upper power generation limit into account: 1:00 on April 30.

#### pickup_start_time_in_result_file

- **Type: `"YYYY-MM-DD hh:mm:ss"`**
- **default value: equivalent to start_time**

The start time for selecting and displaying a subset of the whole optimization period in the xlsx file that stores the results.

#### pickup_end_time_in_result_file

- **Type: `"YYYY-MM-DD hh:mm:ss"`**
- **default value: equivalent to end_time**

The end time for selecting and displaying a subset of the whole optimization period in the xlsx file that stores the results.

#### fix_tie_margin_to_zero

- **Type: Boolean value**
- **default value: `False`**

Select whether or not to fix the operational margin of the tie line to 0.

#### fix_required_tertiary_reserve_to_zero

- **Type: Boolean value**
- **default value: `False`**

Select whether or not to fix the required tertiary reserve to 0.

#### optimization_timing

- **Type: string (`"day-ahead"` or `"intra-day"`)**
- **default value: `"day-ahead"`**

The time axis of the schedule, indicating whether that round of optimization is day-ahead scheduling (`"day-ahead"`) or intra-day scheduling (`"intra-day"`).

In the ΔkW-value version ([`formulation_type: "delta-kW-bid"`](03_unit_commitment.md#formulation_type)), the tertiary-reserve formulation is switched according to this value (ΔkW value in day-ahead scheduling, kWh value in intra-day scheduling). It is not referenced in `delta-kW-no-market` (default).

> **About the old key `kind_of_formulation` (permanent alias)**
> This key was formerly named `kind_of_formulation`. After the rename to `optimization_timing`, the old key `kind_of_formulation` is **permanently** accepted (no deprecation planned). If an element has no `optimization_timing` and only `kind_of_formulation` is specified, it is automatically mapped to `optimization_timing` (info log only; no warning is issued). If both are specified, `optimization_timing` takes precedence.

**Description example: Day-ahead and intra-day scheduling for the delivery date of May 1, 2016, executed consecutively**

```yaml
rolling_opt_list:
  - name: "2016-05-01_day-ahead_scheduling"
    start_time: "2016-04-30 13:00:00"
    end_time: "2016-05-02 00:00:00"
    pre_period_hours: 24
    optimization_timing: "day-ahead"
    pv_value:
      "2016-04-30 13:00:00": "ACT"
      "2016-05-01 01:00:00": "FCST"
    wf_value:
      "2016-04-30 13:00:00": "ACT"
      "2016-05-01 01:00:00": "FCST"
    pickup_start_time_in_result_file: "2016-05-01 01:00:00"
  - name: "2016-05-01_intra-day_scheduling"
    start_time: "2016-05-01 01:00:00"
    end_time: "2016-05-02 0:00:00"
    pre_period_hours: 24
    optimization_timing: "intra-day"
    pv_value:
      "2016-05-01 01:00:00": "ACT"
    wf_value:
      "2016-05-01 01:00:00": "ACT"
    fix_tie_margin_to_zero: True
    fix_required_tertiary_reserve_to_zero: True
```

Note: `optimization_timing` may be omitted in `formulation_type: "delta-kW-no-market"` (defaults to `"day-ahead"`). It is assigned automatically to each entry by the auto-generation rule (configuration method 2).

## Configuration method 2 -Automatic generation-

Generate rolling_opt_list so that the operation for the target period (delivery date) is fixed.

### **Configuration method 2-1 -Specify by date-**

### start_date

- **required fields**
- **Type: `"YYYY-MM-DD"`**

The first day of the period to be optimized.

### end_date

- **Type: `"YYYY-MM-DD"`**

- **default value: same day as `start_date`**

The last day of the period to be optimized.

### **Configuration method 2-2 -Specify by year and month-**

### start_month

- **required fields**
- **Type: `"YYYY-MM"`**

The first month of the period to be optimized. The period begins on the first day (the 1st) of the target month.

### end_month

- **Type: `"YYYY-MM-DD"`**

- **default value: same month as `start_month`**

The last month of the period to be optimized. The period ends on the last day of the target month.

**Note: If "start_date"/"end_date" and "start_month"/"end_month" are specified together, the period written with "start_month"/"end_month" is optimized (deprecated).**

### rolling_opt_list_rule

- **Type: character string**
- **default value: `"default"`**

Rule for generating rolling_opt_list. Currently only 'default' can be set.

**default**

The optimization alternates between day-ahead scheduling, whose optimization period runs from 13:00 on the previous day to 0:00 the next day, and intra-day scheduling, from 1:00 on the day to 12:00 the next day. In order to fix the operation of the latter 12 hours of the last day, the day-ahead scheduling for the day after the last day is also carried out.

**Example: I want to select "Special" as the rule for generating rolling_opt_list.**

```yaml
rolling_opt_list_rule: "Special"
```
Note: This example does not work correctly because the "Special" rule does not exist in the current version.
This is a setting to be used when rules other than default are implemented in the future.
