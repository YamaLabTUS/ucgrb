# ローリング最適化リスト設定

最適化リストの設定方法は2つある。

## 設定方法1 -直接記述-

### rolling_opt_list

- **必須項目**
- **書式: リスト形式**

実施する最適化の各回の設定をリスト形式で記載する。

リスト内に記載する要素は以下の通りである。

#### name

- **必須項目**

- **書式: 文字列**

実施する最適化の名称。

#### start_time

- **必須項目**
- **書式: `"YYYY-MM-DD hh:mm:ss"`**

最適化対象期間開始時刻。

#### end_time

- **必須項目**
- **書式: `"YYYY-MM-DD hh:mm:ss"`**

最適化対象期間終了時刻。

#### pre_period_hours

- **必須項目**
- **書式: 数字**

最適化対象期間前に決定変数が用意される期間。単位は時間。

#### pv_value

- **必須項目**
- **書式: 辞書式**
  - **インデックス:  `"YYYY-MM-DD hh:mm:ss"`**
  - **値: `"ACT"` or `"FCST"`**

インデックス以降の時間帯のPV出力値を、実出力値（`"ACT"`）とするか予測値(`"FCST"`)とするか選択する。

#### wf_value

- **必須項目**
- **書式: 辞書式**
  - **インデックス:  `"YYYY-MM-DD hh:mm:ss"`**
  - **値:  `"ACT"` or `"FCST"`**

インデックス以降の時間帯のWF出力値を、実出力値（`"ACT"`）とするか予測値(`"FCST"`)とするか選択する。

#### E_MAX_start_time

- **書式: `"YYYY-MM-DD hh:mm:ss"`**

大規模発電機のN日毎の発電量上限制約を考慮し始める時刻。

本項目を指定しない場合、最適化対象期間前の引き継ぎ期間も含めて、一日の最初の時刻（時間粒度が1時間のときは、1時）とする。

例: 最適化対象期間: 4月30日13時～5月2日0時、最適化対象期間前の引き継ぎ期間:24時間
→　発電量上限制約の考慮開始時刻 : 4月30日1時

#### pickup_start_time_in_result_file

- **書式: `"YYYY-MM-DD hh:mm:ss"`**
- **デフォルト値: start_timeと同値**

結果を収納するxlsxファイルで、全最適化期間のうち、一部の期間を選択して結果を表示する際の、選択開始時間

#### pickup_end_time_in_result_file

- **書式: `"YYYY-MM-DD hh:mm:ss"`**
- **デフォルト値: end_timeと同値**

結果を収納するxlsxファイルで、全最適化期間のうち、一部の期間を選択して結果を表示する際の、選択終了時間

#### fix_tie_margin_to_zero

- **書式: ブール値**
- **デフォルト値: `False`**

連系線の運用マージンを0に固定するか否かを選択する。

#### fix_required_tertiary_reserve_to_zero

- **書式: ブール値**
- **デフォルト値: `False`**

必要三次調整力を0に固定するか否かを選択する。

**記述例: 受渡日2016年5月1日の前日計画、当日計画を連続で実施**

```yaml
rolling_opt_list:
  - name: "2016-05-01_day-ahead_scheduling"
    start_time: "2016-04-30 13:00:00"
    end_time: "2016-05-02 00:00:00"
    pre_period_hours: 24
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
    pv_value:
      "2016-05-01 01:00:00": "ACT"
    wf_value:
      "2016-05-01 01:00:00": "ACT"
    fix_tie_margin_to_zero: True
    fix_required_tertiary_reserve_to_zero: True
```

## 設定方法2 -自動生成-

対象期間（受渡日）の運用が確定するようにrolling_opt_listを生成する。

### **設定方法2-1 -日付で指定-**

### start_date

- **必須項目**
- **書式: `"YYYY-MM-DD"`**

最適化対象期間の最初の日。

### end_date

- **書式: `"YYYY-MM-DD"`**

- **デフォルト値: "start_date"と同一日**

最適化対象期間の最後の日。

### **設定方法2-2 -年月で指定-**

### start_month

- **必須項目**
- **書式: `"YYYY-MM"`**

最適化対象期間の最初の月。対象月の最初の日（1日）から期間開始となる。

### end_month

- **書式: `"YYYY-MM-DD"`**

- **デフォルト値: "start_month"と同一月**

最適化対象期間の最後の月。対象月の最終日に期間終了となる。

**※"start_date"、"end_date"と”start_month”、"end_month”を併記してしまった場合、”start_month”、"end_month”で書かれている期間が最適化される（非推奨）。**

### rolling_opt_list_rule

- **書式: 文字列**
- **デフォルト値:  `"default"`**

rolling_opt_listの生成ルール。現時点では’default’のみ設定可能。

**default**

最適化期間が前日13時から翌日0時までの前日計画（day-ahead scheduling）と当日1時から翌日12時までの当日計画（intra-day scheduling）を交互に行う。最終日の後半12時間の運用を確定するために、最終日翌日の前日計画まで実施する。

**記述例: rolling_opt_listの生成ルールとして"Special"を選択したい**

```yaml
rolling_opt_list_rule: "Special"
```
注: 現バージョンで"Special"という条件は存在しないので、この例は正しく動作しない。
将来、default以外のルールが実装された場合に利用する設定である。
