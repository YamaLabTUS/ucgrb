# 設定ファイル記述例

詳細は[設定ファイルの記述方法](../06_config/01_how_to_write.md)を参照

## 例1: 対象期間が単一日の場合

対象期間（受渡日）: 2016年4月1日

```yaml
config_name: "Example 1"
start_date: "2016-04-01"
```

2016年4月1日の前日計画、当日計画、2016年4月2日の前日計画、全部で3回の最適化が実施される。

## 例2: 対象期間が複数日の場合

対象期間（受渡日）: 2016年4月1日から3日までの3日間

```yaml
config_name: "Example 2"
start_date: "2016-04-01"
end_date: "2016-04-03"
```

2016年4月1日の前日計画、当日計画、2016年4月2日の前日計画、当日計画、2016年4月3日の前日計画、当日計画、2016年4月4日の前日計画、全部で7回の最適化が実施される。

## 例3: 対象期間が月単位で指定する場合

対象期間（受渡日）: 2016年4月（2016年4月1日から2016年4月30日まで）

```yaml
config_name: "Example 3"
start_month: "2016-04"
```

## 例4: 対象期間が複数月の場合

対象期間（受渡日）: 2016年4月から7月までの4ヶ月間（2016年4月1日から2016年7月31日まで）

```yaml
config_name: "Example 4"
start_month: "2016-04"
end_month: "2016-07"
```

## 例5: 最適化リストの直接記述

例1と同一の最適化を実施する場合。

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

## 例6: 最適化対象地域の選択

対象地域: "Area_A"のみ

```yaml
config_name: "Example 6"
start_date: "2016-04-01"
areas:
  - "Area_A"
```

## 例7: ESSの蓄電池運用設定その1

計画運用制約に変更（デフォルトは境界条件制約）

```yaml
config_name: "Example 7"
start_date: "2016-04-01"
set_e_ess_plan_constrs: True
```

## 例8: ESSの蓄電池運用設定その2

境界条件制約を考慮した後、計画運用制約で上書きする。

```yaml
config_name: "Example 8"
start_date: "2016-04-01"
set_e_ess_plan_constrs: True
set_e_ess_bc_constrs: True
```

## 例9: 原子力発電機のマストラン運転制約の解除

```yaml
config_name: "Example 9"
start_date: "2016-04-01"
set_must_run_operation_of_nucl_constrs: False

```

## 例10: 発電機・ESS1台ごとの運用結果をエクセルファイルに出力する

```yaml
config_name: "Example 10"
start_date: "2016-04-01"
export_xlsx_file:
  generation: True
  ESS: True
```

## 例11: MPSファイルの出力

```yaml
config_name: "Example 11"
start_date: "2016-04-01"
export_mps_file: True
```
