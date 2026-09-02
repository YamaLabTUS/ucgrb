# Decision variable options

### set_p

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the average output of the large generator *g* at time *t* is set as the decision variable "p" in the function "make_grb_model".

### set_p_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", the variable that determines whether or not to set the GF&LFC reserve that the large generator *g* will secure at time *t* with the variables "p_gf_lfc_up" and "p_gf_lfc_down".

### set_p_tert

- **Type: Boolean value**
- **default value: `True`**

A variable that determines whether or not the tertiary reserve ensured by the large generator *g* at time *t* is set as the variables "p_tert_up" and "p_tert_down" in the function "make_grb_model".

### set_u

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the operating state of nuclear or thermal generator *g* at time *t* is set as the decision variable "u" in the function "make_grb_model".

### set_su

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the decision variable indicating whether or not nuclear or thermal generator *g* has started at time *t* is set to "su" in the function "make_grb_model".

### set_sd

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the decision variable indicating whether or not nuclear or thermal generator *g* has stopped at time *t* is set to "sd" in the function "make_grb_model".

### set_p_pv_suppr

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the average PV output suppression for area *a* at time *t* is set as the decision variable "p_pv_suppr" in the function "make_grb_model".

### set_p_pv_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not the GF&LFC reserve secured by PV in area *a* at time *t* is set as the variables "p_pv_gf_lfc_up" and "p_pv_gf_lfc_down" in the function "make_grb_model".

### set_p_pv_tert

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether the tertiary reserve secured by PV in area *a* at time *t* is set as the decision variable "p_pv_tert_up" or "p_pv_tert_down" in the function "make_grb_model".

### set_p_wf_suppr

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the average wind power output suppression for area *a* at time *t* is set as the decision variable "p_wf_suppr" in the function "make_grb_model".

### set_p_wf_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the GF&LFC reserve secured by wind generation in area *a* at time *t* is set as the variables "p_wf_gf_lfc_up" and "p_wf_gf_lfc_down" in the function "make_grb_model".

### set_p_wf_tert

- **Type: Boolean value**
- **default value: `True`**

A variable that determines whether or not the tertiary reserve secured by wind power in area *a* at time *t* is set as the variables "p_wf_tert_up" and "p_wf_tert_down" in the function "make_grb_model".

### set_p_ess

- **Type: Boolean value**
- **default value: `True`**

A variable that determines whether or not the average power output and pumping power of the energy storage system *ess* at time *t* are set as the variables "p_ess_d" and "p_ess_c" in the function "make_grb_model".

### set_p_ess_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", the variables "p_ess_gf_lfc_up" and "p_ess_gf_lfc_down" determine whether the GF&LFC reserve reserved by the energy storage system *ess* at time *t* should be set as the variables.

### set_p_ess_tert

- **Type: Boolean value**
- **default value: `True`**

Whether or not to set the tertiary reserve ensured by the energy storage system *ess* at time *t* as the variables "p_ess_tert_up" and "p_ess_tert_down" in the function "make_grb_model".

### set_e_ess

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the amount of energy stored in the energy storage system *ess* at time *t* is set as the decision variable "e_ess" in the function "make_grb_model".

### set_e_ess_short

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the energy storage system *ess* is set to the planned energy storage shortfall at time *t* as the decision variable "e_ess_short" in the function "make_grb_model".

### set_e_ess_surplus

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the planned energy storage surplus of the energy storage system *ess* at time *t* is set as the decision variable "e_ess_surplus" in the function "make_grb_model".

### set_dchg_and_chg_ess

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether the operating state of the energy storage system *ess* at time *t* is set as the variables "dchg_ess" and "chg_ess" in the function "make_grb_model".

### set_p_tie

- **Type: Boolean value**
- **default value: `True`**

A variable that determines whether or not to set the average value of the power interchanged by the tie line *tie* at time *t* as the variables "p_tie_f" and "p_tie_c" in the function "make_grb_model".

### set_p_tie_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", variables that determine whether the GF&LFC reserve is set as "p_tie_gf_lfc_up_f", "p_tie_gf_lfc_up_c", "p_tie_gf_lfc_down_f", or "p_tie_gf_lfc_down_c".

### set_p_tie_tert

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", variables that determine whether or not to set the tertiary reserve as the variables "p_tie_tert_up_f", "p_tie_tert_up_c", "p_tie_tert_down_f", and "p_tie_tert_down_c".

### set_d

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the power flow direction of the tie line *tie* at time *t* is set as the decision variable "d" in the function "make_grb_model".

### set_d_gf_lfc

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", a variable that determines whether the power flow direction of the GF&LFC reserve of the tie line *tie* at time *t* is set as the variables "d_gf_lfc_up" and "d_gf_lfc_down".

### set_d_tert

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", the variable that determines whether the power flow direction of the tertiary reserve of the tie line *tie* at time *t* is set as the variables "d_tert_up" and "d_tert_down" or not.

### set_p_short

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to set the supply shortage of area *a* at time *t* as the decision variable "p_short" in the function "make_grb_model".

### set_p_surplus

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the supply surplus of area *a* at time *t* is set as the decision variable "p_surplus" in the function "make_grb_model".

### set_p_tert_short

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", a variable that determines whether or not to set the tertiary reserve shortfall of area *a* at time *t* as the variables "p_tert_up_short" and "p_tert_down_short".
