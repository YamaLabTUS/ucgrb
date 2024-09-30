# Constraints on energy storage system
Large-scale Energy Storage Systems (ESS), such as pumped storage power plants, can be considered.


- Maximum discharge and charge and minimum discharge and charge constraints can be considered.
  - $P_{t,ess}^{\text{discharge}\,\text{des}}$ and $P_{t,ess}^{\text{charge}\,\text{des}}$ are added to the maximum discharge and charging constraint to allow for reduced discharge and charging conditions (See CSV file ['descent.csv'](../../05_csvfile/02_generation.md#decent), where output drops can be set).
- It is assumed that GF&LFC and tertiary reserve can be provided to the extent that operating conditions and storage capacity allow.
- The following two type constraints can be considered for the operation of the state of charge. These two constraints can be considered at the same time. By default, only the boundary condition constraints are considered.
  - Energy balancing constraint between starting and ending times : Constraints that fix the state of charge at the time before and at the end of the period to be optimized to a reference value.
  - Energy scheduling constraint at designated times : Constraints that fix the variables to meet the time and state of charge specified in the CSV file.



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

## Maximum power discharge and charge constraints for energy storage system

$$
\begin{align}
   p_{t,ess}^{\text{discharge}}
    & \leq \left( P_{ess}^{\text{discharge}\,\text{MAX}} - P_{t,ess}^{\text{discharge}\,\text{des}} \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{charge}}
    & \leq \left( P_{ess}^{\text{charge}\,\text{MAX}} - P_{t,ess}^{\text{charge}\,\text{des}} \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$

## Minimum power discharge and charge constraints for energy storage system

$$
\begin{align}
   p_{t,ess}^{\text{discharge}}
    & \geq P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{charge}}
    & \geq P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$

## Operational status determination for energy storage system

$$
\begin{align}
   dchg_{t,ess} + chg_{t,ess}
    & \leq 1
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$

## GF&LFC reserve assured quantity constraints for energy storage system

$$
\begin{align}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess}
   \- p_{t,ess}^{\text{discharge}} \notag
   \\
        &  + p_{t,ess}^{\text{charge}}
   \- P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (3)
\\
  p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{charge}\,\text{MAX}} chg_{t,ess}
   \- p_{t,ess}^{\text{charge}} \notag
   \\
        &  + p_{t,ess}^{\text{discharge}}
   \- P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (4)
\end{align}
$$

## Reserve assured quantity constraints for energy storage system

$$
\begin{align}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,p}^{\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$

## State of charge operational constraints for energy storage system

$$
\begin{align}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}}}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$

## Maximum energy storage constraints for energy storage system

$$
\begin{align}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$

## Minimum energy storage constraints for energy storage system

$$
\begin{align}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$

## Energy balancing constraint between starting and ending times for energy storage system

$$
\begin{align}
   e_{0,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
           \ \ \left( E_{0,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{0,ess}^{\text{INHE}}
           \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall ess \in ESS
    & \qquad (1)
\\
   e_{end,ess} + e_{end,ess}^{\text{short}} - e_{end,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
    & \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
| Condition name                                                             | Default value | Setting name on the configuration file | Change in the above formula when set in False          |
| :------------------------------------------------------------------------- | :------------ | :------------------------------------- | :----------------------------------------------------- |
| Consideration of boundary condition constraints of state of charge for ESS | True          | set_e_ess_balance_constrs              | Equations (1) and (2) above are not taken into account |

## Energy scheduling constraint at designated times for energy storage system

$$
\begin{align}
   e_{t,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}                    \\
           \ \ \ \ \ \ \ \left( E_{t,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{t,ess}^{\text{INHE}}                                                   \\
           \ \ \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T^{\text{INHE}},
   \forall ess \in ESS
   & \qquad (1)
\\
   e_{t,ess} + e_{t,ess}^{\text{short}} - e_{t,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T,
   \forall ess \in ESS
   & \qquad (2)
\end{align}
$$
| Condition name                                                               | Default value | Setting name on the configuration file | Change in the above formula when set in False          |
| :--------------------------------------------------------------------------- | :------------ | :------------------------------------- | :----------------------------------------------------- |
| Consideration of planning operational constraints of state of charge for ESS | False         | set_e_ess_schedule_constrs             | Equations (1) and (2) above are not taken into account |

## Planned outage duration constraints for energy storage system

$$
\begin{align}
   dchg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2)
\\
   chg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
