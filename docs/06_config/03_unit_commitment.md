# UC問題設定

UCを行う際の問題設定は、設定ファイルの記載を編集することで、簡単に変更することができる。主な条件設定は以下の通りである。

## 地域毎の制約

### consider_required_gf_lfc_up_by_demand

- **書式: ブール値**
- **デフォルト値: `True`**

需要起因の必要GF&LFC上向き調整力を考慮するか否かを決定する変数

### consider_required_gf_lfc_up_by_pv

- **書式: ブール値**
- **デフォルト値: `True`**

太陽光起因の必要GF&LFC上向き調整力を考慮するか否かを決定する変数

### consider_required_gf_lfc_up_by_wf

- **書式: ブール値**
- **デフォルト値: `True`**

風力起因の必要GF&LFC上向き調整力を考慮するか否かを決定する変数

### consider_required_gf_lfc_down_by_demand

- **書式: ブール値**
- **デフォルト値: `False`**

需要起因の必要GF&LFC下向き調整力を考慮するか否かを決定する変数

### consider_required_gf_lfc_down_by_pv

- **書式: ブール値**
- **デフォルト値: `False`**

太陽光起因の必要GF&LFC下向き調整力を考慮するか否かを決定する変数

### consider_required_gf_lfc_down_by_wf

- **書式: ブール値**
- **デフォルト値: `False`**

風力起因の必要GF&LFC下向き調整力を考慮するか否かを決定する変数

### consider_required_tert_up_by_pv

- **書式: ブール値**
- **デフォルト値: `True`**

太陽光起因の必要三次上向き調整力を考慮するか否かを決定する変数

### consider_required_tert_up_by_wf

- **書式: ブール値**
- **デフォルト値: `True`**

風力起因の必要三次上向き調整力を考慮するか否かを決定する変数

### consider_required_tert_down_by_pv

- **書式: ブール値**
- **デフォルト値: `False`**

太陽光起因の必要三次下向き調整力を考慮するか否かを決定する変数

### consider_required_tert_down_by_wf

- **書式: ブール値**
- **デフォルト値: `False`**

風力起因の必要三次下向き調整力を考慮するか否かを決定する変数

### consider_require_inertia

- **書式: ブール値**
- **デフォルト値: `True`**

慣性定数必要量を考慮するか否かを決定する変数

## 太陽光・風力発電

### provide_p_pv_gf_lfc_up

- **書式: ブール値**
- **デフォルト値: `True`**

太陽光によるGF&LFC上向き調整力供給を考慮するか否かを決定する変数

### provide_p_wf_gf_lfc_up

- **書式: ブール値**
- **デフォルト値: `True`**

風力によるGF&LFC上向き調整力供給を考慮するか否かを決定する変数

### provide_p_pv_gf_lfc_down

- **書式: ブール値**
- **デフォルト値: `False`**

太陽光によるGF&LFC下向き調整力供給を考慮するか否かを決定する変数

### provide_p_wf_gf_lfc_down

- **書式: ブール値**
- **デフォルト値: `False`**

風力によるGF&LFC下向き調整力供給を考慮するか否かを決定する変数

### provide_p_pv_tert_up

- **書式: ブール値**
- **デフォルト値: `True`**

太陽光による三次上向き調整力提供を考慮するか否かを決定する変数

### provide_p_wf_tert_up

- **書式: ブール値**
- **デフォルト値: `True`**

風力による三次上向き調整力提供を考慮するか否かを決定する変数

### provide_p_pv_tert_down

- **書式: ブール値**
- **デフォルト値: `False`**

太陽光による三次下向き調整力提供を考慮するか否かを決定する変数

### provide_p_wf_tert_down

- **書式: ブール値**
- **デフォルト値: `False`**

風力による三次下向き調整力提供を考慮するか否かを決定する変数

## 連系線

### flexible_p_tie

- **書式: ブール値**
- **デフォルト値: `True`**

連系線による電力融通を考慮するか否かを決定する変数

### flexible_p_tie_gf_lfc_up

- **書式: ブール値**
- **デフォルト値: `True`**

連系線によるGF&LFC上向き調整力融通を考慮するか否かを決定する変数

### flexible_p_tie_gf_lfc_down

- **書式: ブール値**
- **デフォルト値: `False`**

連系線によるGF&LFC下向き調整力融通を考慮するか否かを決定する変数

### flexible_p_tie_tert_up

- **書式: ブール値**
- **デフォルト値: `True`**

連系線による3次上向き調整力融通を考慮するか否かを決定する変数

### flexible_p_tie_tert_down

- **書式: ブール値**
- **デフォルト値: `False`**

連系線による3次下向き調整力融通を考慮するか否かを決定する変数

### consider_TTC

- **書式: ブール値**
- **デフォルト値: `True`**

連系線の運用容量制約を考慮するか否かを決定する変数

### consider_maximum_reserve_constraint_for_tie

- **書式: ブール値**
- **デフォルト値: `False`**

連系線の融通調整力最大値制約を考慮するか否かを決定する変数

### consider_tie_margin_in_intra-day

- **書式: ブール値**
- **デフォルト値: `False`**

当日計画において、連系線の運用マージンを考慮するか否かを決定する変数

## ESS（エネルギー貯蔵システム）

### set_e_ess_plan_constrs

- **書式: ブール値**
- **デフォルト値: `False`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの蓄電量計画運用制約を考慮するか否かを決める変数

### set_e_ess_bc_constrs

- **書式: ブール値**
- **デフォルト値: **
  - **set_e_ess_plan_constrs = `False` のとき: `True`**
  - **set_e_ess_plan_constrs = `True` のとき: `False`**

関数「make_grb_model」の中で、エネルギー貯蔵システムの蓄電量境界条件制約を考慮するか否かを決める変数

## 原子力発電機

### set_must_run_operation_of_nucl_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力発電機のマストラン運用制約を考慮するか否かを決める変数
