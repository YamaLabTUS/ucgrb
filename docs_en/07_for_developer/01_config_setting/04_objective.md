# Objective function options

### set_C_coef_on_objective_function

- #### **Type: Boolean value**

- **default value: `True`**

Variable determines whether or not to add the generator output proportional term of the fuel cost function to the objective function within the function "make_grb_model".

### set_C_intc_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable determines whether or not to add a constant term of the fuel cost function to the objective function within the function "make_grb_model".

### set_C_startup_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to add a startup cost term to the objective function in the function "make_grb_model".

### set_C_short_ess_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the energy storage system under-planning penalty term is added to the objective function in the function "make_grb_model".

### set_C_ess_surplus_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the energy storage system's energy storage planning surplus penalty term is added to the objective function in the function "make_grb_model".

### set_C_ess_short_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to add a supply shortage cost term to the objective function in the function "make_grb_model".

### set_C_surplus_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variables in the function "make_grb_model" that determine whether or not to add a supply surplus cost term to the objective function.

### set_C_PV_suppr_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variables in the function "make_grb_model" that determine whether or not to add a PV output suppression cost term to the objective function.

### set_C_WF_suppr_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variables in the function "make_grb_model" that determine whether or not to add a wind power output suppression cost term to the objective function.

### set_C_Tert_short_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not to add a tertiary reserve shortage cost term to the objective function within the function "make_grb_model".

### set_C_tie_penalty_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", a variable that determines whether or not to add a term for the interchange usage penalty of the tie line to the objective function.

### set_C_tie_penalty_GF_LFC_UP_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", a variable that determines whether or not to add a term for the GF&LFC up-reserve interchange usage penalty of the tie line to the objective function.

### set_C_tie_penalty_GF_LFC_DOWN_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

In the function "make_grb_model", a variable that determines whether or not to add a term for the GF&LFC down-reserve interchange usage penalty of the tie line to the objective function.

### set_C_tie_penalty_Tert_UP_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variables in the function "make_grb_model" that determine whether or not to add a term for the tertiary up-reserve interchange usage penalty of the tie line to the objective function.

### set_C_tie_penalty_Tert_DOWN_on_objective_function

- **Type: Boolean value**
- **default value: `True`**

Variables in the function "make_grb_model" that determine whether or not to add a term for the tertiary down-reserve interchange usage penalty of the tie line to the objective function.
