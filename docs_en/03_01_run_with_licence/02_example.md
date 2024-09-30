# Setting file examples

For details, see ["How to describe a configuration file"](../06_config/01_how_to_write.md)

## Example 1: Target period is one day (a single day)

Target Period (delivery date): April 1, 2016

```yaml
config_name: "Example 1"
start_date: "2016-04-01"
```

In all, three optimizations will be performed: day-ahead scheduling on April 1, 2016, intra-day scheduling on April 1, 2016, and day-ahead scheduling on April 2, 2016.

## Example 2: Target period is multiple days

Target Period (Delivery Date): 3 days from April 1 to 3, 2016

```yaml
config_name: "Example 2"
start_date: "2016-04-01"
end_date: "2016-04-03"
```

In all, seven optimizations will be performed: day-ahead scheduling on April 1, 2016, intra-day scheduling on April 1, 2016, day-ahead scheduling on April 2, 2016, intra-day scheduling on April 2, 2016, day-ahead scheduling on April 3, 2016, intra-day scheduling on April 3, 2016, and day-ahead scheduling on April 4, 2016.

## Example 3: Specifying the target period in months

Target Period (Delivery Date): April 2016 (from April 1, 2016 to April 30, 2016)

```yaml
config_name: "Example 3"
start_month: "2016-04"
```

## Example 4: Target period is for more than one month

Target Period (Delivery Date): 4 months from April to July 2016 (April 1, 2016 to July 31, 2016)

```yaml
config_name: "Example 4"
start_month: "2016-04"
end_month: "2016-07"
```

## Example 5: Direct description of an optimization list

The rolling optimization can be executed by being listed directly in the setting file as the followings.
The details of the description method are explained in ["iv. Rolling optimized list settings"](../06_config/04_rolling_optimization_list.md) in "6. List of setting values"
Below is a description of the case where the same optimization as in Example 1 is performed.

```yaml
config_name: "Example 5"
rolling_opt_list:
  - name: "2016-04-01_day-ahead_scheduling"
    start_time: "2016-03-31 13:00:00"
    end_time: "2016-04-02 00:00:00"
    pre_period_hours: 24
    pv_value:
      "2016-03-31 13:00:00": "ACT"
      "2016-04-01 01:00:00": "FCST"
    wf_value:
      "2016-03-31 13:00:00": "ACT"
      "2016-04-01 01:00:00": "FCST"
    pickup_start_time_in_result_file: "2016-04-01 01:00:00"
  - name: "2016-04-01_intra-day_scheduling"
    start_time: "2016-04-01 01:00:00"
    end_time: "2016-04-02 0:00:00"
    pre_period_hours: 24
    pv_value:
      "2016-04-01 01:00:00": "ACT"
    wf_value:
      "2016-04-01 01:00:00": "ACT"
    fix_tie_margin_to_zero: True
    fix_required_tertiary_reserve_to_zero: True
  - name: "2016-04-02_day-ahead_scheduling"
    start_time: "2016-04-01 13:00:00"
    end_time: "2016-04-03 00:00:00"
    pre_period_hours: 24
    pv_value:
      "2016-04-01 13:00:00": "ACT"
      "2016-04-02 01:00:00": "FCST"
    wf_value:
      "2016-04-01 13:00:00": "ACT"
      "2016-04-02 01:00:00": "FCST"
    pickup_start_time_in_result_file: "2016-04-02 01:00:00"
```

## Example 6: Selection of areas to be optimized

Areas covered: "Area_A" only

```yaml
config_name: "Example 6"
start_date: "2016-04-01"
areas:
  - "Area_A"
```

## Example 7: ESS operational settings, Part 1

Changing constraints to scheduled energy storage operation (default is "energy balancing constraint between starting and ending times")

```yaml
config_name: "Example 7"
start_date: "2016-04-01"
set_e_ess_schedule_constrs: True
```

## Example 8: ESS operational settings, Part 2

After considering the energy balancing constraint between starting and ending times, they are overridden by the energy scheduling constraint at designated times.

```yaml
config_name: "Example 8"
start_date: "2016-04-01"
set_e_ess_schedule_constrs: True
set_e_ess_balance_constrs: True
```

## Example 9: Removal of constraints of nuclear generation must-run operation

```yaml
config_name: "Example 9"
start_date: "2016-04-01"
set_must_run_operation_of_nucl_constrs: False

```

## Example 10: Output calculation results for each generation and ESS to an Excel file

```yaml
config_name: "Example 10"
start_date: "2016-04-01"
export_xlsx_file:
  generation: True
  ESS: True
```

## Example 11: MPS file output

```yaml
config_name: "Example 11"
start_date: "2016-04-01"
export_mps_file: True
```

## Example 12: Change the time granularity to 30 minutes

```yaml
config_name: "Example 12"
start_date: "2016-04-01"
time_series_granularity: 30
```

## Example 13: Change the time granularity to 2 hours (120 minutes)

```yaml
config_name: "Example 13"
start_date: "2016-04-01"
time_series_granularity: 120
```