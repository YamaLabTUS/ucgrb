# 決定変数のオプション設定

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
