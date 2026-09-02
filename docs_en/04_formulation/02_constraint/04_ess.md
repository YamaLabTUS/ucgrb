# Constraints on energy storage system

> **Conditional branching by [`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type)**
> The items on this page related to ΔkW (day-ahead scheduling) / kWh (intra-day scheduling) are effective only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). In `delta-kW-no-market` (default), the tertiary reserve is treated as a single reserve quantity, and these items are disabled.

Large-scale energy storage systems (ESS), such as pumped storage power plants, can be considered.

- Maximum discharge and charge capacity, and minimum discharge and charge capacity constraints can be considered.
  - $P_{t,ess}^{\text{discharge}\,\text{des}}$ and $P_{t,ess}^{\text{charge}\,\text{des}}$ are added to the maximum discharge and charge capacity constraints so that each capacity-reduction state can be taken into account (see the CSV file ["descent.csv"](../../05_csvfile/02_generation.md#output-reduction), where output reduction can be set).
- It is assumed that GF&LFC reserve and tertiary reserve can be provided to the extent that the operating state and stored energy allow.
- The following two constraints can be considered for the operation of the stored energy. These two constraints can also be considered simultaneously. By default, only the boundary condition constraint is considered.
  - Energy balancing constraint between starting and ending times: a constraint that fixes the stored energy at the time before the optimization period and at the end time to reference values.
  - Energy scheduling constraint at designated times: a constraint that fixes the decision variables so as to satisfy the time and stored energy specified in the CSV file.

See the following pages for definitions of each index, set, parameter, and decision variable.

- [Sets and indices](../03_set_and_index.md)
- Parameters
  1. [Parameters for area](../04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](../04_parameter/02_generation.md)
  3. [Parameters for renewable energy](../04_parameter/03_re.md)
  4. [Parameters for energy storage system](../04_parameter/04_ess.md)
  5. [Parameters for tie line](../04_parameter/05_tie.md)
  6. [Parameters that depend on scheduling kind](../04_parameter/06_depend_on_scheduling_kind.md)
- Variables
  1. [Variables for area](../05_variable/01_area.md)
  2. [Variables for large-scale power generation](../05_variable/02_generation.md)
  3. [Variables for renewable energy](../05_variable/03_re.md)
  4. [Variables for energy storage system](../05_variable/04_ess.md)
  5. [Variables for tie line](../05_variable/05_tie.md)

## Average power output and charging power in intra-day scheduling (`delta-kW-bid` only)

As values inherited from day-ahead scheduling, the following preconditions apply:

$$
\begin{aligned}
    P_{t,ess}^{\text{da},\text{discharge}}&=p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}1)
\\
    P_{t,ess}^{\text{da},\text{charge}}&=p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}2)
\end{aligned}
$$

On this basis, the average power output and charging power in intra-day scheduling are given as follows.

$$
\begin{aligned}
    p_{t,ess}^{\text{discharge}} &\geq P_{t,ess}^{\text{da},\text{discharge}} - P_{t,ess}^{\text{da},\text{charge}} + p_{t,ess}^{\text{id},\text{UP}} - p_{t,ess}^{\text{id},\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}3)
    \\
    p_{t,ess}^{\text{discharge}} &\leq P_{t,ess}^{\text{da},\text{discharge}} - P_{t,ess}^{\text{da},\text{charge}} + p_{t,ess}^{\text{id},\text{UP}} - p_{t,ess}^{\text{id},\text{DOWN}} + \max \left( P_{ess}^{\text{discharge}\,\text{MAX}},  P_{ess}^{\text{charge}\,\text{MAX}}  \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
    p_{t,ess}^{\text{charge}} &\geq P_{t,ess}^{\text{da},\text{charge}} - P_{t,ess}^{\text{da},\text{discharge}} + p_{t,ess}^{\text{id},\text{DOWN}} - p_{t,ess}^{\text{id},\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}5)
    \\
    p_{t,ess}^{\text{charge}} &\leq P_{t,ess}^{\text{da},\text{charge}} - P_{t,ess}^{\text{da},\text{discharge}} + p_{t,ess}^{\text{id},\text{DOWN}} - p_{t,ess}^{\text{id},\text{UP}} + \max \left( P_{ess}^{\text{discharge}\,\text{MAX}},  P_{ess}^{\text{charge}\,\text{MAX}}  \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}6)
\end{aligned}
$$

$$
\begin{aligned}
    p_{t,ess}^{\text{id},\text{UP}} &\leq u_{t,ess}^{\text{id is UP}} \left( P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}} \right)
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}7)
    \\
    p_{t,ess}^{\text{id},\text{DOWN}} &\leq \left( 1 - u_{t,ess}^{\text{id is UP}} \right) \left( P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}} \right)
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}8)
\end{aligned}
$$

Here, $u_{t,ess}^{\text{id is UP}}$ is a binary variable representing the reserve direction (1: up, 0: down). Equations (2-4-0-7) and (2-4-0-8) are a **direction-selection constraint** that prohibits providing up and down simultaneously; the term $P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}}$ on the right-hand side is not the actual upper limit of the reserve power, but is used as a sufficiently large constant (big-M) for direction selection. In the up direction, $u_{t,ess}^{\text{id is UP}} = 1$ and the down-reserve amount $p_{t,ess}^{\text{id},\text{DOWN}}$ is fixed to 0 (the down direction is the reverse). The actual upper limit of the reserve power is imposed separately by the tertiary reserve $P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}}$ secured in the day-ahead scheduling.

## 1. Maximum discharge and charge capacity constraints for energy storage system

$$
\begin{aligned}
   p_{t,ess}^{\text{discharge}}
    & \leq \left( P_{ess}^{\text{discharge}\,\text{MAX}} - P_{t,ess}^{\text{discharge}\,\text{des}} \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}1\text{-}1)
\\
   p_{t,ess}^{\text{charge}}
    & \leq \left( P_{ess}^{\text{charge}\,\text{MAX}} - P_{t,ess}^{\text{charge}\,\text{des}} \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}1\text{-}2)
\end{aligned}
$$

## 2. Minimum discharge and charge capacity constraints for energy storage system

$$
\begin{aligned}
   p_{t,ess}^{\text{discharge}}
    & \geq P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}2\text{-}1)
\\
   p_{t,ess}^{\text{charge}}
    & \geq P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}2\text{-}2)
\end{aligned}
$$

## 3. Operational status determination for energy storage system

$$
\begin{aligned}
   dchg_{t,ess} + chg_{t,ess}
    & \leq 1
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}3\text{-}1)
\end{aligned}
$$

| Feature name                                                  | Default | Setting name on configuration file | Change from the above equations when True                                            |
| :------------------------------------------------------------ | :------ | :--------------------------------- | :----------------------------------------------------------------------------------- |
| Making the ESS operational-status binary variables continuous | False   | make_dchg_chg_ess_continuous       | The binary variables $dchg_{t,ess}, chg_{t,ess}$ are treated as continuous variables |

## 4. GF&LFC reserve assured quantity constraints for energy storage system

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}2)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq & \; P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess}
   \- p_{t,ess}^{\text{discharge}} \notag
   \\
        &  + p_{t,ess}^{\text{charge}}
   \- P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}3)
\\
  p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{charge}\,\text{MAX}} chg_{t,ess}
   \- p_{t,ess}^{\text{charge}} \notag
   \\
        &  + p_{t,ess}^{\text{discharge}}
   \- P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}4)
\end{aligned}
$$

## 5. Reserve assured quantity constraints for energy storage system

### In the case of `formulation_type: "delta-kW-no-market"`

(Default) The tertiary reserve is treated as a single reserve quantity $p_{t,ess}^{\text{Tert}\,\text{UP/DOWN}}$.

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}2)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

In day-ahead scheduling, the tertiary reserve is treated as ΔkW ($p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$), and in intra-day scheduling, it is treated as the actual operating power ($p_{t,ess}^{\text{id}\,\text{UP/DOWN}}$).

#### Day-ahead scheduling

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}3)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}4)
\end{aligned}
$$

#### Intra-day scheduling

As values inherited from day-ahead scheduling, the following preconditions apply:

$$
\begin{aligned}
    P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}&=p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}5)
\\
    P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}&=p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}6)
\end{aligned}
$$

On this basis, the constraint is expressed as follows. In intra-day scheduling, since $p_{t,ess}^{\text{id},\text{UP}}$ and $p_{t,ess}^{\text{id},\text{DOWN}}$ are already included in $p_{t,ess}^{\text{discharge}}$ and $p_{t,ess}^{\text{charge}}$ (see equations (2-4-0-3) and (2-4-0-4)), $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ and $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ are treated as 0 to avoid double counting.

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}7)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}8)
\\
    p_{t,ess}^{\text{id},\text{UP}} \leq P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}9)
\\
    p_{t,ess}^{\text{id},\text{DOWN}} \leq P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}10)
\end{aligned}
$$

## 6. Stored energy operational constraints for energy storage system

$$
\begin{aligned}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}}}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}6\text{-}1)
\end{aligned}
$$

## 7. Maximum stored energy constraints for energy storage system

### In the case of `formulation_type: "delta-kW-no-market"`

(Default) The tertiary reserve is treated as a single reserve quantity $p_{t,ess}^{\text{Tert}\,\text{DOWN}}$.

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}1)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

In day-ahead scheduling, the tertiary reserve is treated as ΔkW ($p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$).

#### Day-ahead scheduling

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}2)
\end{aligned}
$$

#### Intra-day scheduling

In intra-day scheduling, since $p_{t,ess}^{\text{id},\text{DOWN}}$ is already included in $p_{t,ess}^{\text{charge}}$ (see equation (2-4-0-4)), $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ is treated as 0 to avoid double counting.

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}3)
\end{aligned}
$$

## 8. Minimum stored energy constraints for energy storage system

### In the case of `formulation_type: "delta-kW-no-market"`

(Default) The tertiary reserve is treated as a single reserve quantity $p_{t,ess}^{\text{Tert}\,\text{UP}}$.

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}1)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

In day-ahead scheduling, the tertiary reserve is treated as ΔkW ($p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$).

#### Day-ahead scheduling

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}2)
\end{aligned}
$$

#### Intra-day scheduling

In intra-day scheduling, since $p_{t,ess}^{\text{id},\text{UP}}$ is already included in $p_{t,ess}^{\text{discharge}}$ (see equation (2-4-0-3)), $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ is treated as 0 to avoid double counting.

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}3)
\end{aligned}
$$

## 9. Energy balancing constraint between starting and ending times for energy storage system

$$
\begin{aligned}
   e_{0,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
           \ \ \left( E_{0,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{0,ess}^{\text{INHE}}
           \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}9\text{-}1)
\\
   e_{end,ess} + e_{end,ess}^{\text{short}} - e_{end,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
    & \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}9\text{-}2)
\end{aligned}
$$

| Feature name                                                         | Default | Setting name on configuration file | Change from the above equations when False                 |
| :------------------------------------------------------------------- | :------ | :--------------------------------- | :--------------------------------------------------------- |
| Consideration of the ESS stored-energy boundary condition constraint | True    | set_e_ess_balance_constrs          | Equations (2-4-9-1) and (2-4-9-2) above are not considered |

## 10. Energy scheduling constraint at designated times for energy storage system

$$
\begin{aligned}
   e_{t,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}                    \\
           \ \ \ \ \ \ \ \left( E_{t,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{t,ess}^{\text{INHE}}                                                   \\
           \ \ \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T^{\text{INHE}},
   \forall ess \in ESS
   & \qquad (2\text{-}4\text{-}10\text{-}1)
\\
   e_{t,ess} + e_{t,ess}^{\text{short}} - e_{t,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T,
   \forall ess \in ESS
   & \qquad (2\text{-}4\text{-}10\text{-}2)
\end{aligned}
$$

| Feature name                                                | Default | Setting name on configuration file | Change from the above equations when False                   |
| :---------------------------------------------------------- | :------ | :--------------------------------- | :----------------------------------------------------------- |
| Consideration of the ESS stored-energy scheduling constraint | False   | set_e_ess_schedule_constrs         | Equations (2-4-10-1) and (2-4-10-2) above are not considered |

## 11. Planned outage duration constraints for energy storage system

$$
\begin{aligned}
   dchg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}11\text{-}1)
\\
   chg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}11\text{-}2)
\end{aligned}
$$
