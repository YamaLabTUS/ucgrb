# 目的関数のオプション設定

### set_C_coef_on_objective_function

- #### **書式: ブール値**

- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に燃料費関数の発電機出力比例分の項を加えるか否かを決める変数

### set_C_intc_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に燃料費関数の定数項を加えるか否かを決める変数

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

関数「make_grb_model」の中で、目的関数に供給不足ペナルティの項を加えるか否かを決める変数

### set_C_surplus_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に供給余剰ペナルティの項を加えるか否かを決める変数

### set_C_PV_suppr_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に太陽光発電出力抑制ペナルティの項を加えるか否かを決める変数

### set_C_WF_suppr_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に風力発電出力抑制ペナルティの項を加えるか否かを決める変数

### set_C_Tert_short_on_objective_function

- **書式: ブール値**
- **デフォルト値: `True`**

関数「make_grb_model」の中で、目的関数に三次調整力不足ペナルティの項を加えるか否かを決める変数

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
