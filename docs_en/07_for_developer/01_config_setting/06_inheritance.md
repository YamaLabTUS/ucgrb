# Decision variable inheritance options

### set_p_to_inherited_vars

- **Type: Boolean value**
- **default value: `True`**

A variable that determines whether or not the output "p" of a large generator in the class "UCVars" is to be taken over for the next optimization.

### set_u_su_sd_to_inherited_vars

- **Type: Boolean value**
- **default value: `True`**

Variables in the class "UCVars" that determine whether the variables "u", "su", and "sd", which indicate the operating status of nuclear and thermal power generators, are to be taken over for the next optimization.

### set_e_ess_to_inherited_vars

- **Type: Boolean value**
- **default value: `True`**

Variable that determines whether or not the energy storage capacity "e_ess" of the energy storage device is taken over for the next optimization in the class "UCVars".
