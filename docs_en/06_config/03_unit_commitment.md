# UC Problem Setting

The problem settings for performing UC can be easily changed by editing the descriptions in the configuration file. The main condition settings are as follows:

## Formulation style

### formulation_type

- **Type: string (`"delta-kW-no-market"` or `"delta-kW-bid"`)**
- **default value: `"delta-kW-no-market"`**

Setting value that determines the formulation style.

- `"delta-kW-no-market"` (default): treats the tertiary reserve as a single reserve quantity. Exactly identical to the behavior before this flag was introduced (backward compatible).
- `"delta-kW-bid"`: the ΔkW-value version. The value of tertiary reserve in the balancing market is reflected in the objective function and constraints as ΔkW (kW value) in day-ahead scheduling and as kWh (energy value) in intra-day scheduling. The tertiary reserve secured in day-ahead scheduling is taken over into intra-day scheduling.

Specifying a value other than `"delta-kW-no-market"` / `"delta-kW-bid"` raises an error. `formulation_type` determines how tertiary reserve is evaluated, and is a separate setting from the planning-time-axis key [`optimization_timing`](04_rolling_optimization_list.md#optimization_timing) (`day-ahead` / `intra-day`). Under `delta-kW-bid`, however, the two are not unrelated: intra-day scheduling takes over the ΔkW secured in day-ahead scheduling and operates it as energy (kWh), so `delta-kW-bid` intra-day scheduling presupposes a preceding day-ahead plan.

> **Input when `delta-kW-bid` is specified**: add the ΔkW/kWh-related columns (`C_Delta_kW_UP`, `C_Delta_kW_DOWN`, `C_kWh_UP`, `C_kWh_DOWN`, etc.) to the generation and ESS CSVs. If these columns are absent, they are filled with `0.0` (or a default value), and the missing column names are output to a WARNING log. When `"delta-kW-no-market"` is specified, these columns are not read (fully compatible with the previous behavior).

## Constraints per area

### consider_required_gf_lfc_up_by_demand

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider demand-induced required GF&LFC up-reserve

### consider_required_gf_lfc_up_by_pv

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider PV-output-induced required GF&LFC up-reserve

### consider_required_gf_lfc_up_by_wf

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider wind-power-induced required GF&LFC up-reserve

### consider_required_gf_lfc_down_by_demand

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider demand-induced required GF&LFC down-reserve

### consider_required_gf_lfc_down_by_pv

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider PV-output-induced required GF&LFC down-reserve

### consider_required_gf_lfc_down_by_wf

- **Type: Boolean**
- **default value: `False`**

Variables that determine whether or not to consider wind-power-induced required GF&LFC down-reserve

### consider_required_tert_up_by_pv

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider PV-output-induced required tertiary up-reserve

### consider_required_tert_up_by_wf

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider wind-power-induced required tertiary up-reserve

### consider_required_tert_down_by_pv

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider PV-output-induced required tertiary down-reserve

### consider_required_tert_down_by_wf

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider wind-power-induced required tertiary down-reserve

### consider_require_inertia

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not the inertia constant requirement is taken into account

## Photovoltaic and wind farm generation

### provide_p_pv_gf_lfc_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider GF&LFC up-reserve supply by Photovoltaic

### provide_p_wf_gf_lfc_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider GF&LFC up-reserve supply by wind farm

### provide_p_pv_gf_lfc_down

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider GF&LFC down-reserve supply by Photovoltaic

### provide_p_wf_gf_lfc_down

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider GF&LFC down-reserve supply by wind farm

### provide_p_pv_tert_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider the provision of tertiary up-reserve by Photovoltaic

### provide_p_wf_tert_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider tertiary up-reserve supply by wind farm

### provide_p_pv_tert_down

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider tertiary down-reserve supply by Photovoltaic

### provide_p_wf_tert_down

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider tertiary down-reserve supply by wind farm

## Interconnection line

### flexible_p_tie

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider power interchange through tie lines

### flexible_p_tie_gf_lfc_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider GF&LFC up-reserve exchange through tie lines

### flexible_p_tie_gf_lfc_down

- **Type: Boolean**
- **default value: `False`**

Variables that determine whether or not to consider GF&LFC down-reserve exchange through tie lines

### flexible_p_tie_tert_up

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider the tertiary up-reserve exchange through tie lines

### flexible_p_tie_tert_down

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider the tertiary down-reserve exchange through tie line

### consider_TTC

- **Type: Boolean**
- **default value: `True`**

Variables that determine whether to consider the operational capacity constraints of tie lines

### consider_maximum_reserve_constraint_for_tie

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to consider the maximum reserve constraint for tie lines

### consider_tie_margin_in_intra-day

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not the operational margin of the tie line is considered in the day-ahead planning

## ESS (Energy storage systems)

### make_dchg_chg_ess_continuous

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether to convert the binary variables $dchg_{t,ess}$, $chg_{t,ess}$ related to the operating status of the energy storage system into continuous variables in the function "make_grb_model"

### set_e_ess_schedule_constrs

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not the energy storage system's energy storage planning operational constraints are considered in the function "make_grb_model".

### set_e_ess_balance_constrs

- **Type: Boolean**
- **default value:**
  - **If set_e_ess_schedule_constrs = `False`: `True`.**
  - **If set_e_ess_schedule_constrs = `True`: `False`.**

Variable that determines whether or not the energy storage system's storage capacity boundary condition constraint is considered in the function "make_grb_model".

## Nuclear and thermal power generators

### set_ramp_constr

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not to consider the output change rate constraint of nuclear and thermal power generators in the function "make_grb_model"

### make_u_continuous

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether to convert the binary variables $u_{t,g}$, $su_{t,g}$, $sd_{t,g}$ related to the startup and shutdown of nuclear and thermal power generators into continuous variables in the function "make_grb_model"

## Nuclear power generator

### set_must_run_operation_of_nucl_constrs

- **Type: Boolean**
- **default value: `True`**

Variable that determines whether or not the must-run operational constraints of the nuclear generator are considered in the function "make_grb_model".
