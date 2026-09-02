# 辞書型データ作成のオプション設定

### make_area_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、地域のリスト"area"と各値のパラメータ値"area_para"を生成するか否かを決める変数

### make_generation_type_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、発電機の種類のリスト"generation_type"と各種のパラメータ値"generation_type_para"を生成するか否かを決める変数

### make_generation_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、発電機のリスト"generation"と各発電機のパラメータ値"generation_para"を生成するか否かを決める変数

### make_ess_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、エネルギー貯蔵システムのリスト"ess"と各所のパラメータ値"ess_para"を生成するか否かを決める変数

### make_tie_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、連系線のリスト"tie"と各線のパラメータ値"tie_para"を生成するか否かを決める変数

### make_whole_timeline_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、全ての最適化対象の時系列'whole_timeline'と日毎に時系列を分けて保存する'daily_whole_timeline'を生成するか否かを決める変数

### make_demand_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、電力需要の時系列リスト"demand"と各時間帯、各地域のパラメータ値"demand_para"を生成するか否かを決める変数

### make_pv_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、太陽光発電の時系列リスト"pv"と各時間帯、各地域のパラメータ値"pv_para"を生成するか否かを決める変数

### make_wf_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、風力発電の時系列リスト"wf"と各時間帯、各地域のパラメータ値"wf_para"を生成するか否かを決める変数

### make_tie_operation_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、連系線運用のリスト"tie_operation"と各運用のパラメータ値"tie_operation_para"を生成するか否かを決める変数

### make_maintenance_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、補修期間のデータから、計画停止時系列を作成し、uc_dataの”planned_outage”に格納するか否かを決定する変数

### make_planned_outage_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、計画停止のタイムラインを作成し、"planned_outage"に格納するか否かを決定する変数

### make_descent_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、出力低下に関するタイムラインを作成し、"P_des"に格納するか否かを決定する変数

### make_e_ess_plan_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、エネルギー貯蔵システムの蓄電量計画運用制約に関する辞書型データを生成するか否かを決める変数


### make_others_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、その他の発電設備の出力時系列リストを生成するか否かを決める変数

### make_timeline_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、各回の最適化対象の時系列'timeline'を生成するか否かを決める変数

### update_pv_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、各回の最適化で必要な太陽光発電のデータ（出力値、最大予測値、最小予測値）を生成するか否かを決める変数

### update_wf_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、各回の最適化で必要な風力発電のデータ（出力値、最大予測値、最小予測値）を生成するか否かを決める変数

### make_max_energy_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、N日毎の発電量上限制約に関する辞書型データを生成するか否かを決める変数

### make_constants_depend_on_scheduling_kind_dicts

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、計画の種類に依存して決定される定数を生成するか否かを決める変数

### calculate_C_coef

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、燃料費係数と所内率から、出力比例係数を生成するか否かを決める変数

### calculate_P_MAX

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、発電端最大出力と所内率から、送電端最大出力を生成するか否かを決める変数

### calculate_P_MIN

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、発電端最小出力と所内率から、送電端最小出力を生成するか否かを決める変数

### calculate_C_coef_CO2

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、単位出力あたりのCO2排出量を生成するか否かを決める変数

### calculate_C_intc_CO2

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、単位時間あたりのCO2排出量を生成するか否かを決める変数

### calculate_C_startup_CO2

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、1 回起動あたりのCO2排出量を生成するか否かを決める変数

### calculate_Min_Up_Time

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、最小起動時間を最適化時間粒度に合わせて修正するか否かを決める変数

### calculate_Min_Down_Time

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCDicts」の中で、最小停止時間を最適化時間粒度に合わせて修正するか否かを決める変数
