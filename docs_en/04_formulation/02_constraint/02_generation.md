# Constraints on large-scale power generation

> **Conditional branching by [`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type)**
> The items on this page related to ΔkW (day-ahead scheduling) / kWh (intra-day scheduling) are effective only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). In `delta-kW-no-market` (default), the tertiary reserve is treated as a single reserve quantity, and these items are disabled.

large-scale power generations such as hydro, nuclear, thermal, etc. can be considered.

- Maximum output, minimum output, and maximum generated energy for each N days can be considered.
  - $P_{t,g}^{\text{des}}$ is added to the maximum output constraint to allow for reduced output conditions (See CSV file ['descent.csv'](../../05_csvfile/02_generation.md#output-reduction), where output drops can be set).
- The required minimum up time constraints and the required minimum down time constraints can be considered as constraints on the start-up and shutdown scheduling of nuclear and thermal generation.
- The annual maintenance schedule for nuclear and thermal power can be considered. This means generator outages during the maintenance period can be added as a constraint.
- The constraints of nuclear must-run operation, i.e., always in startup except during maintenance periods, can be considered.

See the following pages for definitions of each set, index, constant, and variable.

- [Sets and indices](../03_set_and_index.md)
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

## Average power output in intra-day scheduling (`delta-kW-bid` only)

As values inherited from day-ahead scheduling, the following preconditions apply:

$$
\begin{aligned}
    P_{t,g}^{\text{da}}&=p_{t,g}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}1)
\end{aligned}
$$

On this basis, the average power output in intra-day scheduling is given as follows.

$$
\begin{aligned}
    p_{t,g} &= P_{t,g}^{\text{da}} + p_{t,g}^{\text{id},\text{UP}} - p_{t,g}^{\text{id},\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}2)
    \\
    p_{t,g}^{\text{id},\text{UP}} &\leq u_{t,g}^{\text{id is UP}} P_{g}^{\text{MAX}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}3)
    \\
    p_{t,g}^{\text{id},\text{DOWN}} &\leq \left( 1 - u_{t,g}^{\text{id is UP}} \right) P_{g}^{\text{MAX}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}4)
\end{aligned}
$$

where $u_{t,g}^{\text{id is UP}}$ is a binary variable representing the reserve direction (1: up, 0: down). Equations (2-2-0-3) and (2-2-0-4) are **direction-selection constraints** that prohibit providing up and down reserve simultaneously, and the $P_{g}^{\text{MAX}}$ on the right-hand side is not the actual upper limit of the reserve energy but is used as a sufficiently large constant (big-M) for direction selection. In the up direction, $u_{t,g}^{\text{id is UP}} = 1$ and the down adjustment $p_{t,g}^{\text{id},\text{DOWN}}$ is fixed to 0 (and vice versa for the down direction). The actual upper limit of the reserve energy is imposed separately by the intra-day equation of the maximum output constraint, through the tertiary reserve $P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}}$ secured in day-ahead scheduling.

## 1. Maximum power output constraints for large-scale power generation

### In the case of `formulation_type: "delta-kW-no-market"`

(default) The tertiary reserve is treated as a single reserve quantity $p_{t,g}^{\text{Tert}\,\text{UP}}$.

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}1)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}2)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

The tertiary reserve is treated as ΔkW ( $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ ) in day-ahead scheduling, and as the actually operated energy kWh ( $p_{t,g}^{\text{id},\text{UP}}$ ) in intra-day scheduling.

#### Day-ahead scheduling

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}3)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}4)
\end{aligned}
$$

#### Intra-day scheduling

As values inherited from day-ahead scheduling, the following preconditions apply:

$$
\begin{aligned}
    P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}&=p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}1\text{-}5)
\end{aligned}
$$

On this basis, the constraint is expressed as follows. In intra-day scheduling, since $p_{t,g}^{\text{id},\text{UP}}$ is already included in $p_{t,g}$ (see equation (2-2-0-2)), $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ is treated as 0 to avoid double counting.

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}6)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}7)
\\
    p_{t,g}^{\text{id},\text{UP}} \leq P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}1\text{-}8)
\end{aligned}
$$

## 2. Minimum power output constraints for large-scale power generation

### In the case of `formulation_type: "delta-kW-no-market"`

(default) The tertiary reserve is treated as a single reserve quantity $p_{t,g}^{\text{Tert}\,\text{DOWN}}$.

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}1)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}2)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

The tertiary reserve is treated as ΔkW ( $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ ) in day-ahead scheduling, and as the actually operated energy kWh ( $p_{t,g}^{\text{id},\text{DOWN}}$ ) in intra-day scheduling.

#### Day-ahead scheduling

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}3)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}4)
\end{aligned}
$$

#### Intra-day scheduling

As values inherited from day-ahead scheduling, the following preconditions apply:

$$
\begin{aligned}
    P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}&=p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}2\text{-}5)
\end{aligned}
$$

On this basis, the constraint is expressed as follows. In intra-day scheduling, since $p_{t,g}^{\text{id},\text{DOWN}}$ is already included in $p_{t,g}$ (see equation (2-2-0-2)), $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ is treated as 0 to avoid double counting.

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}6)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}7)
\\
    p_{t,g}^{\text{id},\text{DOWN}} \leq P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}2\text{-}8)
\end{aligned}
$$

## 3. GF&LFC reserve assured quantity constraints for large-scale power generation

$$
\begin{aligned}
   p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}3\text{-}1)
\\
   p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}3\text{-}2)
\end{aligned}
$$

## 4. N daily maximum energy of generation constraints for large-scale power generation

$$
\begin{aligned}
   \sum_{i = t}^{t + 24N - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + 24N \times m \; (m = 0,1,2\dots), \forall g \in G
    & \qquad (2\text{-}2\text{-}4\text{-}1)
\end{aligned}
$$

## 5. Start-up and shutdown decisions for nuclear and thermal power generation

$$
\begin{aligned}
   su_{t,g} - sd_{t,g}
    & = u_{t,g} - u_{t-1,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}5\text{-}1)
\\
   su_{t,g} + sd_{t,g}
    & \leq 1
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}5\text{-}2)
\end{aligned}
$$

| Variable              | Condition 1 | Condition 2 | Condition 3 | Condition 4 |                            Remarks                             |
| --------------------- | :---------: | :---------: | :---------: | :---------: | :-----------------------------------------------------------: |
| $u_{t,g}$             |      1      |      1      |      0      |      0      |                                                               |
| $u_{t-1,g}$           |      1      |      0      |      1      |      0      |                                                               |
| $u_{t,g} - u_{t-1,g}$ |      0      |      1      |     -1      |      0      |             Right side of equation (2-2-5-1)                  |
| $su_{t,g} - sd_{t,g}$ |      0      |      1      |     -1      |      0      |             Left side of equation (2-2-5-1)                   |
| $su_{t,g}$            |      0      |      1      |      0      |      0      | From equation (2-2-5-2), it cannot be 1 at the same time as $sd_{t,g}$ |
| $sd_{t,g}$            |      0      |      0      |      1      |      0      | From equation (2-2-5-2), it cannot be 1 at the same time as $su_{t,g}$ |

| Feature name                                                                        | Default | Setting name on configuration file | Change from the above equations when `True`                       |
| :---------------------------------------------------------------------------------- | :------ | :--------------------------------- | :---------------------------------------------------------------- |
| Continuous relaxation of the start-up and shutdown binary variables for nuclear and thermal generation | False   | make_u_continuous                  | The binary variables $u_{t,g}, su_{t,g}, sd_{t,g}$ are treated as continuous variables |

## 6. Required minimum up time constraints for nuclear and thermal generation

$$
\begin{aligned}
   \sum_{i=t+1-MinUpTime_{g}}^{t} su_{i,g}
    & \leq u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}6\text{-}1)
\end{aligned}
$$

## 7. Required minimum down time constraints for nuclear and thermal generation

$$
\begin{aligned}
   \sum_{i=t+1-MinDownTime_{g}}^{t} sd_{i,g}
    & \leq 1 - u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}7\text{-}1)
\end{aligned}
$$

## 8. Ramp rate constraints for nuclear and thermal generation

### In the case of `formulation_type: "delta-kW-no-market"`

(default) The tertiary reserve is treated as a single reserve quantity $p_{t,g}^{\text{Tert}\,\text{UP}}$ / $p_{t,g}^{\text{Tert}\,\text{DOWN}}$.

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}1)
\\
   p_{t,g} - p_{t,g}^{\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}2)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

The tertiary reserve is treated as ΔkW in day-ahead scheduling, and as the actually operated energy kWh in intra-day scheduling.

#### Day-ahead scheduling

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}3)
\\
   p_{t,g} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}4)
\end{aligned}
$$

#### Intra-day scheduling

In intra-day scheduling, since $p_{t,g}^{\text{id},\text{UP}}$ and $p_{t,g}^{\text{id},\text{DOWN}}$ are already included in $p_{t,g}$ (see equation (2-2-0-2)), $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ and $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ are treated as 0 to avoid double counting.

$$
\begin{aligned}
   p_{t,g} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}5)
\\
   p_{t,g} + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}6)
\end{aligned}
$$

| Feature name                                                       | Default | Setting name on configuration file | Change from the above equations when `False` |
| :----------------------------------------------------------------- | :------ | :--------------------------------- | :------------------------------------------- |
| Consideration of ramp rate constraints for nuclear and thermal generation | True    | set_ramp_constr                    | The above equations are not considered       |

## 9. Planned outage duration constraints for nuclear and thermal generation

$$
\begin{aligned}
   u_{t,g}
    & = 0
    & \forall t \in T_{g}^{\text{Planned Outage}} , \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}9\text{-}1)
\end{aligned}
$$

## 10. Nuclear must-run operational constraints

$$
\begin{aligned}
   u_{t,g}
    & =1
    & \forall t \in \left( T^{\text{INHE,A}} \cup T \right) \setminus T_{g}^{\text{Planned Outage}}, \forall g \in G_{NUCL}
    & \qquad (2\text{-}2\text{-}10\text{-}1)
\end{aligned}
$$

| Feature name                                            | Default | Setting name on configuration file     | Change from the above equations when `False` |
| :------------------------------------------------------ | :------ | :------------------------------------- | :------------------------------------------- |
| Consideration of nuclear must-run operation constraints | True    | set_must_run_operation_of_nucl_constrs | The above equations are not considered       |
