# 連系線データ

## 連系線

**ファイル名: tie.csv**

- 連系線の名称と接続関係を表す

| インデックス              | 値     | 概要                                                                                                                                                                                                                          |
| ------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                      | 文字列 | 名称（重複禁止）                                                                                                                                                                                                              |
| from                      | 文字列 | 送電元の地域名（連系線の向きを正とする際の送電側エリア）                                                                                                                                                                      |
| to                        | 文字列 | 送電先の地域名（連系線の向きを正とする際の受電側エリア）                                                                                                                                                                      |
| C_tie_penalty             | 数字   | 電力融通使用ペナルティ係数 [千円/MWh]                                                                                                                                                                                         |
| C_tie_penalty_GF_LFC_UP   | 数字   | GF&LFC上げ調整力融通使用ペナルティ係数 [千円/MWh]                                                                                                                                                                             |
| C_tie_penalty_GF_LFC_DOWN | 数字   | GF&LFC下げ調整力融通使用ペナルティ係数 [千円/MWh]                                                                                                                                                                             |
| C_tie_penalty_Tert_UP     | 数字   | 三次上げ調整力融通使用ペナルティ係数 [千円/MWh]                                                                                                                                                                               |
| C_tie_penalty_Tert_DOWN   | 数字   | 三次上げ調整力融通使用ペナルティ係数 [千円/MWh]                                                                                                                                                                               |
| TTC_forward               | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）運用容量 [MW] <br />**setting_method_of_TTC_and_Margin**=`fixed`のときに用いられる                                                                                        |
| TTC_counter               | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）運用容量 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`のときに用いられる                                                                                         |
| Margin_forward            | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）容量マージン [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`のときに用いられる                                                                                     |
| Margin_counter            | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）容量マージン [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`のときに用いられる                                                                                     |
| GF_LFC_UP_forward_MAX     | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通されるGF&LFC上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる |
| GF_LFC_UP_counter_MAX     | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通されるGF&LFC上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる |
| GF_LFC_DOWN_forward_MAX   | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通されるGF&LFC下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる |
| GF_LFC_DOWN_counter_MAX   | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通されるGF&LFC下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる |
| Tert_UP_forward_MAX       | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通される三次上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる   |
| Tert_UP_counter_MAX       | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通される三次上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる   |
| Tert_DOWN_forward_MAX     | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通される三次下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる   |
| Tert_DOWN_counter_MAX     | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通される三次下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`fixed`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる   |

### 例

[data_set/data-example/tie/tie.csv](../../data_set/data-example/tie/tie.csv)

[data_set/data-mini/tie.csv](../../data_set/data-mini/tie.csv)

| name     | from   | to     | C_tie_penalty | C_tie_penalty_GF_LFC_UP | C_tie_penalty_GF_LFC_DOWN | C_tie_penalty_Tert_UP | C_tie_penalty_Tert_DOWN | TTC_forward | TTC_counter | Margin_forward | Margin_counter | GF_LFC_UP_forward_MAX | GF_LFC_UP_counter_MAX | GF_LFC_DOWN_forward_MAX | GF_LFC_DOWN_counter_MAX | Tert_UP_forward_MAX | Tert_UP_counter_MAX | Tert_DOWN_forward_MAX | Tert_DOWN_counter_MAX |
| :------- | :----- | :----- | :------------ | :---------------------- | :------------------------ | :-------------------- | :---------------------- | :---------- | :---------- | :------------- | :------------- | :-------------------- | :-------------------- | :---------------------- | :---------------------- | :------------------ | :------------------ | :-------------------- | :-------------------- |
| Tie-Line | Area_B | Area_A | 0.002         | 0.002                   | 0.002                     | 0.002                 | 0.002                   | 400         | 400         | 50             | 50             | 100                   | 100                   | 100                     | 100                     | 100                 | 100                 | 100                   | 100                   |
| ...      | ...    | ...    | ...           | ...                     | ...                       | ...                   | ...                     | ...         | ...         | ...            | ...            | ...                   | ...                   | ...                     | ...                     | ...                 | ...                 | ...                   | ...                   |

## 連系線運用 - tie_operation -

**ファイル名: tie_operation.csv**

- 各連系線における、各月、各時間帯の最大送電量を示す。
- **setting_method_of_TTC_and_Margin**=`season`のときに用いられる

| インデックス            | 値     | 概要                                                                                                                                                                                                                                                                               |
| ----------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tie                     | 文字列 | 対象連系線の名称                                                                                                                                                                                                                                                                   |
| month_section           | 文字列 | 季節の区分を示す。 |
| of_the_clock_section    | 文字列 | 時間帯を平日昼・平日夜・休日昼・休日夜の4つに区分する。<br />「weekday_day」: 平日昼、「weekday_night」: 平日夜、「holiday_day」: 休日昼、「holiday_night」: 休日夜。                                                                                                              |
| TTC_forward             | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）運用容量 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`のときに用いられる                                                                                                                                             |
| TTC_counter             | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）運用容量 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`のときに用いられる                                                                                                                                             |
| Margin_forward          | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）容量マージン [MW]<br />**setting_method_of_TTC_and_Margin**=`season`のときに用いられる                                                                                                                                         |
| Margin_counter          | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）容量マージン [MW]<br />**setting_method_of_TTC_and_Margin**=`season`のときに用いられる                                                                                                                                         |
| GF_LFC_UP_forward_MAX   | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通されるGF&LFC上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                     |
| GF_LFC_UP_counter_MAX   | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通されるGF&LFC上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                     |
| GF_LFC_DOWN_forward_MAX | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通されるGF&LFC下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                     |
| GF_LFC_DOWN_counter_MAX | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通されるGF&LFC下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                     |
| Tert_UP_forward_MAX     | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通される三次上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                       |
| Tert_UP_counter_MAX     | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通される三次上げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                       |
| Tert_DOWN_forward_MAX   | 数字   | 順方向（送電側エリア"from"から受電側エリア”to”への）に融通される三次下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                       |
| Tert_DOWN_counter_MAX   | 数字   | 逆方向（受電側エリア”to”から送電側エリア"from"への）に融通される三次下げ調整力最大値 [MW]<br />**setting_method_of_TTC_and_Margin**=`season`、且つ、**consider_maximum_reserve_constraint_for_tie**=`true`のときに用いられる                                                       |

### 例

[data_set/data-example/tie/season/operation/weekday_day/tie_operation.csv](../../data_set/data-example/tie/season/operation/weekday_day/tie_operation.csv)

[data_set/data-example/tie/season/operation/weekday_night/tie_operation.csv](../../data_set/data-example/tie/season/operation/weekday_night/tie_operation.csv)

[data_set/data-example/tie/season/operation/holiday_day/tie_operation.csv](../../data_set/data-example/tie/season/operation/holiday_day/tie_operation.csv)

[data_set/data-example/tie/season/operation/holiday_night/tie_operation.csv](../../data_set/data-example/tie/season/operation/holiday_night/tie_operation.csv)

| tie      | month_section | of_the_clock_section | TTC_forward | TTC_counter | Margin_forward | Margin_counter | GF_LFC_UP_forward_MAX | GF_LFC_UP_counter_MAX | GF_LFC_DOWN_forward_MAX | GF_LFC_DOWN_counter_MAX | Tert_UP_forward_MAX | Tert_UP_counter_MAX | Tert_DOWN_forward_MAX | Tert_DOWN_counter_MAX |
| :------- | :------------ | :------------------- | :---------- | :---------- | :------------- | :------------- | :-------------------- | :-------------------- | :---------------------- | :---------------------- | :------------------ | :------------------ | :-------------------- | :-------------------- |
| Tie-Line | Apr           | weekday_day          | 450         | 450         | 87.3           | 171.3          | 100                   | 100                   | 100                     | 100                     | 100                 | 100                 | 100                   | 100                   |
| Tie-Line | May           | weekday_day          | 450         | 450         | 96.3           | 174.3          | 100                   | 100                   | 100                     | 100                     | 100                 | 100                 | 100                   | 100                   |
| Tie-Line | Jun           | weekday_day          | 450         | 450         | 93.3           | 174.3          | 100                   | 100                   | 100                     | 100                     | 100                 | 100                 | 100                   | 100                   |
| ...      | ...           | ...                  | ...         | ...         | ...            | ...            | ...                   | ...                   | ...                     | ...                     | ...                 | ...                 | ...                   | ...                   |
