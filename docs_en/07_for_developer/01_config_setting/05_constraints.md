# Constraint expression options

### set_power_balance_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the power balance constraint is taken into account in the function "make_grb_model".

### set_gf_lfc_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the GF&LFC reserve constraints are considered in the function "make_grb_model".

### set_tert_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the tertiary reserve constraint is considered in the function "make_grb_model".

### set_inertia_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the necessary inertia constant constraints are considered in the function "make_grb_model".

### set_p_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the maximum power constraint for large generators is considered in the function "make_grb_model".

### set_p_min_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the minimum power constraint for large generators is considered in the function "make_grb_model".

### set_p_gf_lfc_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the GF&LFC maximum reserve constraint for large generators is considered in the function "make_grb_model".


### set_e_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the generation limit constraint every *N* days for large generators is considered in the function "make_grb_model".

### set_start_up_and_shout_down_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the start-stop decision for nuclear and thermal generators is taken into account in the function "make_grb_model".

### set_min_up_time_constrs

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not the minimum up time constraints for nuclear and thermal generators are considered in the function "make_grb_model".

### set_min_down_time_constrs

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not the minimum down time constraints for nuclear and thermal generators are considered in the function "make_grb_model".

### set_planned_outage_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the planned outage duration constraints for nuclear and thermal generators are considered in the function "make_grb_model".

### set_must_run_operation_of_nucl_constrs

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to consider must-run operational constraints for nuclear and thermal generators in the function "make_grb_model".

### set_suppr_and_res_pv_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to consider PV suppression and reserve constraints in the function "make_grb_model".

### set_suppr_and_res_wf_constrs

- **Type: Boolean value**
- **default value: `True`**

Variables that determine whether or not to consider wind power suppression and reserve constraints in the function "make_grb_model".

### set_p_ess_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the maximum generation and charging capacity constraints of the energy storage system are considered in the function "make_grb_model".

### set_p_ess_min_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the minimum generation and charging capacity constraints of the energy storage system are considered in the function "make_grb_model".

### set_dchg_and_chg_ess_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the operational status determination of the energy storage system is taken into account in the function "make_grb_model".

### set_p_ess_gf_lfc_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the GF&LFC maximum reserve constraint of the energy storage system is considered in the function "make_grb_model".

### set_p_ess_res_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to consider the maximum reserve constraint of the energy storage system in the function "make_grb_model".

### set_e_ess_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the energy storage system's energy storage operational constraints are taken into account in the function "make_grb_model".

### set_e_ess_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the maximum storage capacity constraint of the energy storage system is taken into account in the function "make_grb_model".

### set_e_ess_min_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the minimum storage capacity constraint of the energy storage system is considered in the function "make_grb_model".

### set_e_ess_schedule_constrs

- **Type: Boolean value**
- **default value: `False`**

Variable that determines whether or not the energy storage system's energy storage planning operational constraints are considered in the function "make_grb_model".

### set_e_ess_balance_constrs

- **Type: Boolean value**
- **default value:**
  - **set_e_ess_schedule_constrs = If `False`: `True`**
  - **set_e_ess_schedule_constrs = If `True`: `False`**

Variable that determines whether or not the energy storage system's storage capacity boundary condition constraint is considered in the function "make_grb_model".

### set_planned_outage_for_ess_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the planned outage duration constraints of the energy storage system are taken into account in the function "make_grb_model".

### set_p_tie_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to take into account the tie line's interchange power constraints in the function "make_grb_model".

### set_d_tie_gf_lfc_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to consider the GF&LFC reserve direction constraint of the tie line in the function "make_grb_model".

### set_d_tie_tert_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to consider the tertiary reserve direction constraint of the tie line in the function "make_grb_model".

### set_p_tie_res_max_constrs

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the maximum interchange reserve constraint of the tie line is considered in the function "make_grb_model".
