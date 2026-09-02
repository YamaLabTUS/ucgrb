# 制約式のオプション設定

### set_power_balance_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、需給バランス制約を考慮するか否かを決める変数

### set_gf_lfc_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、GF&LFC調整力制約を考慮するか否かを決める変数

### set_tert_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、三次調整力制約を考慮するか否かを決める変数

### set_inertia_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、必要慣性定数制約を考慮するか否かを決める変数

### set_p_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、大規模発電機の最大出力制約を考慮するか否かを決める変数

### set_p_min_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、大規模発電機の最小出力制約を考慮するか否かを決める変数

### set_p_gf_lfc_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、大規模発電機のGF&LFC調整力確保可能量制約を考慮するか否かを決める変数


### set_e_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、大規模発電機の *N* 日毎の発電量上限制約を考慮するか否かを決める変数

### set_start_up_and_shout_down_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力・火力発電機の起動停止判定を考慮するか否かを決める変数

### set_min_up_time_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力・火力発電機の必要最小運転時間制約を考慮するか否かを決める変数

### set_min_down_time_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力・火力発電機の必要最小停止時間制約を考慮するか否かを決める変数

### set_planned_outage_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力・火力発電機の計画停止期間制約を考慮するか否かを決める変数

### set_must_run_operation_of_nucl_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力・火力発電機のマストラン運用制約を考慮するか否かを決める変数

### set_suppr_and_res_pv_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、太陽光発電の抑制量・調整力制約を考慮するか否かを決める変数

### set_suppr_and_res_wf_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、風力発電の抑制量・調整力制約を考慮するか否かを決める変数

### set_p_ess_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの最大発電能力・充電能力制約を考慮するか否かを決める変数

### set_p_ess_min_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの最小発電能力・充電能力制約を考慮するか否かを決める変数

### set_dchg_and_chg_ess_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの運転状況判定を考慮するか否かを決める変数

### set_p_ess_gf_lfc_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムのGF&LFC調整力確保可能量制約を考慮するか否かを決める変数

### set_p_ess_res_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの調整力確保可能量制約を考慮するか否かを決める変数

### set_e_ess_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの蓄電量運用制約を考慮するか否かを決める変数

### set_e_ess_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの最大蓄電量制約を考慮するか否かを決める変数

### set_e_ess_min_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの最小蓄電量制約を考慮するか否かを決める変数

### set_e_ess_schedule_constrs

- **書式: ブール値**
- **デフォルト値: `False`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの蓄電量計画運用制約: 特定時間の蓄電量指定制約を考慮するか否かを決める変数

### set_e_ess_balance_constrs

- **書式: ブール値**
- **デフォルト値:**
  - **set_e_ess_schedule_constrs = `False` のとき: `True`**
  - **set_e_ess_schedule_constrs = `True` のとき: `False`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの蓄電量境界条件制約: 開始時間・終了時間の蓄電量一致条件制約を考慮するか否かを決める変数

### set_planned_outage_for_ess_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの計画停止期間制約を考慮するか否かを決める変数

### set_p_tie_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、連系線の融通電力量制約を考慮するか否かを決める変数

### set_d_tie_gf_lfc_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、連系線の融通GF&LFC調整力方向制約を考慮するか否かを決める変数

### set_d_tie_tert_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、連系線の融通三次調整力方向制約を考慮するか否かを決める変数

### set_p_tie_res_max_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、連系線の最大融通調整力制約を考慮するか否かを決める変数
