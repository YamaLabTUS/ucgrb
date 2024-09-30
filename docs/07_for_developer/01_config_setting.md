# 開発者向け設定値
本ツールを構成する3つのクラス（UCData, UCDicts, UCVars）と２つの関数（make_grb_model, output_result）を組み合わせ、新しい最適化シミュレーションモデルを構築するために、辞書型データ、決定変数、目的関数、制約式、決定変数の引継ぎに関するオプションを用意している。
下記の設定値をデフォルトから変更した場合、エラーなく動作する事が保証されていないことに注意が必要である。

## 辞書型データ作成のオプション設定

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

クラス「UCDicts」の中で、発電機のリスト"generation"と各所のパラメータ値"generation_para"を生成するか否かを決める変数

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

クラス「UCDicts」の中で、燃料費係数と所内率から、可変費係数を生成するか否かを決める変数

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

## 決定変数のオプション設定

### set_p

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における大規模発電機 *g* の出力平均値を、決定変数”p"として設定するか否かを決める変数

### set_p_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における大規模発電機 *g* が確保するGF\&LFC調整力を、決定変数”p_gf_lfc_up"と”p_gf_lfc_down"して設定するか否かを決める変数

### set_p_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における大規模発電機 *g* が確保する三次調整力を、決定変数”p_tert_up"と”p_tert_down"として設定するか否かを決める変数

### set_u

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における原子力・火力発電機 *g* の運転状態を、決定変数"u"として設定するか否かを決める変数

### set_su

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における原子力・火力発電機 *g* が起動したか否かを示す決定変数を、"su"として設定するか否かを決める変数

### set_sd

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における原子力・火力発電機 *g* が停止したか否かを示す決定変数を、"sd"として設定するか否かを決める変数

### set_p_pv_suppr

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の太陽光発電出力抑制量平均値を、決定変数”p_pv_suppr"として設定するか否かを決める変数

### set_p_pv_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の太陽光発電が確保するGF&LFC調整力を、決定変数”p_pv_gf_lfc_up"、"p_pv_gf_lfc_down"として設定するか否かを決める変数

### set_p_pv_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の太陽光発電が確保する三次調整力を、決定変数”p_pv_tert_up"、"p_pv_tert_down"として設定するか否かを決める変数

### set_p_wf_suppr

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の風力発電出力抑制量平均値を、決定変数”p_wf_suppr"として設定するか否かを決める変数

### set_p_wf_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の風力発電が確保するGF&LFC調整力を、決定変数”p_wf_gf_lfc_up"、"p_wf_gf_lfc_down"として設定するか否かを決める変数

### set_p_wf_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の風力発電が確保する三次調整力を、決定変数”p_wf_tert_up"、"p_wf_tert_down"として設定するか否かを決める変数

### set_p_ess

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* の発電出力平均値・揚水動力平均値を、決定変数”p_ess_d"と”p_ess_c"として設定するか否かを決める変数

### set_p_ess_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* が確保するGF&LFC調整力を、決定変数”p_ess_gf_lfc_up"と”p_ess_gf_lfc_down"として設定するか否かを決める変数

### set_p_ess_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* が確保する三次調整力を、決定変数”p_ess_tert_up"と”p_ess_tert_down"として設定するか否かを決める変数

### set_e_ess

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* の蓄電量を、決定変数”e_ess"として設定するか否かを決める変数

### set_e_ess_short

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* の蓄電量計画不足分を、決定変数”e_ess_short"として設定するか否かを決める変数

### set_e_ess_surplus

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* の蓄電量計画余剰分を、決定変数”e_ess_surplus"として設定するか否かを決める変数

### set_dchg_and_chg_ess

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* におけるエネルギー貯蔵システム *ess* の運転状態を、決定変数”dchg_ess"と"chg_ess"として設定するか否かを決める変数

### set_p_tie

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* で融通される電力平均値を、決定変数”p_tie_f"、”p_tie_c”として設定するか否かを決める変数

### set_p_tie_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* で融通されるGF&LFC調整力を、決定変数”p_tie_gf_lfc_up_f"、”p_tie_gf_lfc_up_c”、"p_tie_gf_lfc_down_f"、"p_tie_gf_lfc_down_c"として設定するか否かを決める変数

### set_p_tie_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* で融通される三次調整力を、決定変数”p_tie_tert_up_f"、”p_tie_tert_up_c”、"p_tie_tert_down_f"、"p_tie_tert_down_c"として設定するか否かを決める変数

### set_d

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* の潮流方向を、決定変数”d"として設定するか否かを決める変数

### set_d_gf_lfc

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* のGF&LFC調整力の潮流方向を、決定変数”d_gf_lfc_up"、”d_gf_lfc_down”として設定するか否かを決める変数

### set_d_tert

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における連系線 *tie* の三次調整力の潮流方向を、決定変数”d_tert_up"、”d_tert_down”として設定するか否かを決める変数

### set_p_short

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の供給不足を、決定変数”p_short"として設定するか否かを決める変数

### set_p_surplus

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の供給余剰を、決定変数”p_surplus"として設定するか否かを決める変数

### set_p_tert_short

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、時刻 *t* における地域 *a* の三次調整力不足量を、決定変数”p_tert_up_short"、”p_tert_down_short”として設定するか否かを決める変数

## 目的関数のオプション設定

### set_C_coef_on_objective_function

- #### **書式: ブール値**

- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に可変費の項を加えるか否かを決める変数

### set_C_intc_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に固定費の項を加えるか否かを決める変数

### set_C_startup_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に起動費の項を加えるか否かを決める変数

### set_C_short_ess_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数にエネルギー貯蔵システムの蓄電量計画不足分ペナルティ項を加えるか否かを決める変数

### set_C_ess_surplus_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数にエネルギー貯蔵システムの蓄電量計画余剰分ペナルティ項を加えるか否かを決める変数

### set_C_ess_short_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に供給不足処理費の項を加えるか否かを決める変数

### set_C_surplus_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に供給余剰処理費の項を加えるか否かを決める変数

### set_C_PV_suppr_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に太陽光発電出力抑制処理費の項を加えるか否かを決める変数

### set_C_WF_suppr_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に風力発電出力抑制処理費の項を加えるか否かを決める変数

### set_C_Tert_short_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に三次調整力不足処理費の項を加えるか否かを決める変数

### set_C_tie_penalty_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に連系線の電力融通使用ペナルティの項を加えるか否かを決める変数

### set_C_tie_penalty_GF_LFC_UP_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に連系線のGF&LFC 上げ調整力融通使用ペナルティの項を加えるか否かを決める変数

### set_C_tie_penalty_GF_LFC_DOWN_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に連系線のGF&LFC 下げ調整力融通使用ペナルティの項を加えるか否かを決める変数

### set_C_tie_penalty_Tert_UP_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に連系線の三次上げ調整力融通使用ペナルティの項を加えるか否かを決める変数

### set_C_tie_penalty_Tert_DOWN_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に連系線の三次下げ調整力融通使用ペナルティの項を加えるか否かを決める変数

## 制約式のオプション設定

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

### set_Min_Up_Time_constrs

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
- **デフォルト値: **
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

## 決定変数引き継ぎのオプション設定

### set_p_to_inherited_vars

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCVars」の中で、大規模発電機の出力"p"を次回の最適化の引き継ぎ対象とするか否かを決める変数

### set_u_su_sd_to_inherited_vars

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCVars」の中で、原子力・火力発電機の運転状況を示す変数"u"、"su"、"sd"を次回の最適化の引き継ぎ対象とするか否かを決める変数

### set_e_ess_to_inherited_vars

- **書式: ブール値**
- **デフォルト値: `True`**

クラス「UCVars」の中で、エネルギー貯蔵装置の蓄電量"e_ess"を次回の最適化の引き継ぎ対象とするか否かを決める変数
