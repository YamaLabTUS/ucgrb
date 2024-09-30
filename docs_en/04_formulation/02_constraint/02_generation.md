# Constraints on large-scale power generation

large-scale power generations such as hydro, nuclear, thermal, etc. can be considered.

- Maximum output, minimum output, and maximum generated energy for each N days can be considered.
  - $P_{t,g}^{\text{des}}$ is added to the maximum output constraint to allow for reduced output conditions (See CSV file ['descent.csv'](../../05_csvfile/02_generation.md#decent), where output drops can be set).
- The required minimum up (run) time constraints and the required minimum down (stop) time constraints can be considered as constraints on nuclear and thermal power start-up and shutdown plans.
- The annual maintenance schedule for nuclear and thermal power can be considered. This means generator outages during the maintenance period can be added as a constraint.
- The constraints of nuclear must-run operation, i.e., always in startup except during maintenance periods, can be considered.

See the following pages for definitions of each set, index, constant, and variable.
- [Sets and indies](../03_set_and_index.md)
- Parameters
  1. [Parameters for area](../04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](../04_parameter/02_generation.md)
  3. [Parameters for renewable energy](../04_parameter/03_re.md)
  4. [Parameters for energy storage system](../04_parameter/04_ess.md)
  5. [Parameters for tie line](../04_parameter/05_tie.md)
  6. [Parameters that depends on scheduling kind](../04_parameter/06_depend_on_scheduling_kind.md)
- Variables
  1. [Variables for area](../05_variable/01_area.md)
  2. [Variables for large-scale power generation](../05_variable/02_generation.md)
  3. [Variables for renewable energy](../05_variable/03_re.md)
  4. [Variables for energy storage system](../05_variable/04_ess.md)
  5. [Variables for tie line](../05_variable/05_tie.md)



## Maximum power output constraints for large-scale power generation

$$
\begin{align}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & = \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & = \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2)
\end{align}
$$

## Minimum power output constraints for large-scale power generation

$$
\begin{align}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & = P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & = P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2)
\end{align}
$$

## GF&LFC reserve constraints for large-scale power generation

$$
\begin{align}
   p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (1)
\\
   p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2)
\end{align}
$$

## N daily maximum energy of generation constraints for large-scale power generation

$$
\begin{align}
   \sum_{i = t}^{t + 24N - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + 24N \times m \; (m = 0,1,2\dots), \forall g \in G
\end{align}
$$

## Start-up and shutdown decisions for nuclear and thermal power generation

$$
\begin{align}
   su_{t,g} - sd_{t,g}
    & = u_{t,g} - u_{t-1,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   su_{t,g} + sd_{t,g}
    & \leq 1
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2)
\end{align}
$$

| Variable              | Condition1 | Condition2 | Condition3 | Condition4 |                               Remarks                                |
| --------------------- | :--------: | :--------: | :--------: | :--------: | :------------------------------------------------------------------: |
| $u_{t,g}$             |     1      |     1      |     0      |     0      |                                                                      |
| $u_{t-1,g}$           |     1      |     0      |     1      |     0      |                                                                      |
| $u_{t,g} - u_{t-1,g}$ |     0      |     1      |     -1     |     0      |                      Right side of equation (1)                      |
| $su_{t,g} - sd_{t,g}$ |     0      |     1      |     -1     |     0      |                      Left side of equation (1)                       |
| $su_{t,g}$            |     0      |     1      |     0      |     0      | From equation (2), they may not be 1 at the same time as $sd_{t,g}$. |
| $sd_{t,g}$            |     0      |     0      |     1      |     0      | From equation (2), they may not be 1 at the same time as $su_{t,g}$. |

## Required minimum up time constraints for nuclear and thermal generation

$$
\begin{align}
   \sum_{i=t+1-MinUpTime_{g}}^{t} su_{i,g}
    & \leq u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
\end{align}
$$

## Required minimum down time constraints for nuclear and thermal generation

$$
\begin{align}
   \sum_{i=t+1-MinDownTime_{g}}^{t} sd_{i,g}
    & \leq 1 - u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
\end{align}
$$

## Planned outage duration constraints for nuclear and thermal generation

$$
\begin{align}
   u_{t,g}
    & = 0
    & \forall t \in T_{g}^{\text{Planned Outage}} , \forall g \in G_{N\\&T}
\end{align}
$$

## Nuclear must-run operational constraints

$$
\begin{align}
   u_{t,g}
    & =1
    & \forall t \in \left( T^{\text{INHE,A}} \cup T \right) \setminus T_{g}^{\text{Planned Outage}}, \forall g \in G_{NUCL}
\end{align}
$$

| Condition name                                                    | Default value | Setting name on the configuration file | Change in when nuclear must-run operational constraints set in to False |
| :---------------------------------------------------------------- | :------------ | :------------------------------------- | :---------------------------------------------------------------------- |
| Consideration of nuclear generator mast run operating constraints | True          | set_must_run_operation_of_nucl_constrs | Not considering the above formula                                       |
