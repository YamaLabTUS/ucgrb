# UC問題設定

UCを行う際の問題設定は、設定ファイルの記載を編集することで、簡単に変更することができる。主な条件設定は以下の通りである。

## 定式化スタイル

### formulation_type

- **書式: 文字列（`"delta-kW-no-market"` または `"delta-kW-bid"`）**
- **デフォルト値: `"delta-kW-no-market"`**

定式化のスタイルを決定する設定値。

- `"delta-kW-no-market"`（既定）: 三次調整力を単一の予備力量として扱う。本フラグ導入前の挙動と完全に同一（後方互換）。
- `"delta-kW-bid"`: ΔkW価値考慮版。需給調整市場における三次調整力の価値を、前日計画では ΔkW（kW価値）、当日計画では kWh（電力量価値）として目的関数・制約に反映する。前日計画で確保した三次調整力を当日計画に引き継ぐ。

`"delta-kW-no-market"` / `"delta-kW-bid"` 以外の値を指定するとエラーとなる。`formulation_type` は三次調整力の評価方法を決める設定で、計画の時間軸 [`optimization_timing`](04_rolling_optimization_list.md#optimization_timing)（`day-ahead` / `intra-day`）とは別の設定である。ただし `delta-kW-bid` では両者は無関係ではなく、当日計画は前日計画で確保した ΔkW を引き継いで電力量（kWh）として運用するため、`delta-kW-bid` の当日計画は前日計画を前提とする。

> **`delta-kW-bid` 指定時の入力**: 発電機・ESSの CSV に ΔkW/kWh 関連列（`C_Delta_kW_UP`, `C_Delta_kW_DOWN`, `C_kWh_UP`, `C_kWh_DOWN` 等）を追加する。これらの列が無い場合は `0.0`（または既定値）で補完され、欠損列名が WARNING ログに出力される。`"delta-kW-no-market"` 指定時はこれらの列を読み込まない（従来挙動と完全互換）。

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

### make_dchg_chg_ess_continuous

- **書式: ブール値**
- **デフォルト値: `False`**
-
関数「make_grb_model」の中で、エネルギー貯蔵システムの運転状況に関するバイナリ変数 $dchg_{t,ess}, chg_{t,ess}$ を連続変数に変換するか否かを決める変数

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

## 原子力・火力発電機

### set_ramp_constr

- **書式: ブール値**
- **デフォルト値: `True`**
-
関数「make_grb_model」の中で、原子力・火力発電機の出力変化速度制約を考慮するか否かを決める変数

### make_u_continuous

- **書式: ブール値**
- **デフォルト値: `False`**
-
関数「make_grb_model」の中で、原子力・火力発電機の起動停止に関するバイナリ変数 $u_{t,g}, su_{t,g}, sd_{t,g}$ を連続変数に変換するか否かを決める変数

## 原子力発電機

### set_must_run_operation_of_nucl_constrs

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、原子力発電機のマストラン運用制約を考慮するか否かを決める変数
