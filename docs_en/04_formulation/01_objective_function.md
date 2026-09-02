# Objective function

> **Conditional branching by [`formulation_type`](../06_config/03_unit_commitment.md#formulation_type)**
> The items on this page related to ΔkW (day-ahead scheduling) / kWh (intra-day scheduling) are effective only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). In `delta-kW-no-market` (default), the tertiary reserve is treated as a single reserve quantity, and these items are disabled.

The objective function of the optimization is the minimization of the total social procurement cost over all areas for the period under optimization. The cost components that can be considered are as follows.

- Variable cost, no-load cost, start-up cost, and reserve procurement cost for large-scale power generation $Cost_{g,t}$
  - The reserve procurement cost is obtained by multiplying, in day-ahead scheduling the reserve capacity ($\Delta\text{kW}$), or in intra-day scheduling the actually operated reserve energy ($\text{kWh}$), by the respective unit price
- Supply shortage cost in each area $Cost_{a,t}^{\text{short}}$
- Supply surplus cost in each area $Cost_{a,t}^{\text{surplus}}$
- Tertiary reserve shortage cost in each area $Cost_{a,t}^{\text{Tert,short}}$
- Renewable energy output suppression cost in each area $Cost_{a,t,\text{RE}}^{\text{suppr}}$
  - Currently in Japan, there are no rules for paying compensation for output suppression. If you want to evaluate this situation, $Cost_{a,t,\text{RE}}^{\text{suppr}}$ should be 0.
- Reserve procurement cost of the energy storage system (ESS) $Cost_{ess,t}$
- Stored-energy plan deviation penalty of the energy storage system (ESS) $Penalty_{ess,t}$
- Penalty for using tie lines $Penalty_{tie,t}$
  - Penalty term to avoid energy cycling caused by looped tie lines. The user does not actually pay the usage fee.

See the following pages for definitions of each index, set, parameter, and decision variable.

- [Sets and indices](03_set_and_index.md)
- Parameters
  1. [Parameters for area](04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](04_parameter/02_generation.md)
  3. [Parameters for renewable energy](04_parameter/03_re.md)
  4. [Parameters for energy storage system](04_parameter/04_ess.md)
  5. [Parameters for tie line](04_parameter/05_tie.md)
  6. [Parameters that depend on scheduling kind](04_parameter/06_depend_on_scheduling_kind.md)
- Decision variables
  1. [Variables for area](05_variable/01_area.md)
  2. [Variables for large-scale power generation](05_variable/02_generation.md)
  3. [Variables for renewable energy](05_variable/03_re.md)
  4. [Variables for energy storage system](05_variable/04_ess.md)
  5. [Variables for tie line](05_variable/05_tie.md)

## Overall objective function (common to both modes)

The total cost is expressed as the summation of the cost terms of each area and each facility. Among these cost terms, the cost of large-scale power generation $Cost_{g,t}$ and the cost of the ESS $Cost_{ess,t}$ change their definitions depending on `formulation_type` (described below).

$$
\begin{aligned}
         \min \ F = \sum_{t \in T} & \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) \right.
                  \notag \\
                  & \left.  + \sum_{ess \in \textit{ESS}} \left( Cost_{ess,t}+ Penalty_{ess,t} \right) +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} \right]
    & \qquad (1\text{-}1)
\end{aligned}
$$

---

## Cost of large-scale power generation $Cost_{g,t}$

### In the case of `formulation_type: "delta-kW-no-market"`

(Default) The sum of the variable cost, no-load cost, and start-up cost. The tertiary reserve procurement cost is not included.

$$
Cost_{g,t} = C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g}
\qquad \forall t \in T,\ \forall g \in G_{N\\&T} \qquad (1\text{-}2)
$$

### In the case of `formulation_type: "delta-kW-bid"`

In addition to the above, the tertiary reserve procurement cost is also included into the objective function. Day-ahead scheduling is evaluated with the reserve capacity ΔkW (kW value, unit price $C^{\Delta\text{kW}}$), and intra-day scheduling with the actually operated energy kWh (unit price $C^{\text{kWh}}$). In intra-day scheduling, since $p^{\text{id}}$ is already included in $p$, the variable cost is charged against the day-ahead value $P^{\text{da}}$ to avoid double counting.

$$
Cost_{g,t} =
\begin{cases}
C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g} + C_{g}^{\Delta\text{kW}\,\text{UP}}\ p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} + C_{g}^{\Delta\text{kW}\,\text{DOWN}}\ p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} & (\text{day-ahead scheduling}) \\
C_{g}^{\text{coef}}\ P_{t,g}^{\text{da}} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g} + C_{g}^{\text{kWh}\,\text{UP}}\ p_{t,g}^{\text{id}\,\text{UP}} + C_{g}^{\text{kWh}\,\text{DOWN}}\ p_{t,g}^{\text{id}\,\text{DOWN}} & (\text{intra-day scheduling})
\end{cases}
\qquad \forall t \in T,\ \forall g \in G_{N\\&T} \qquad (1\text{-}2')
$$

## Costs for each area (common to both modes)

The costs for supply shortage, supply surplus, tertiary reserve shortage, and renewable energy output suppression. These are identical for `delta-kW-no-market` and `delta-kW-bid`.

**Supply shortage cost**

$$
Cost_{a,t}^{\text{short}} = C_{a}^{\text{short}}\ p_{t,a}^{\text{short}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}3)
$$

**Supply surplus cost**

$$
Cost_{a,t}^{\text{surplus}} = C_{a}^{\text{surplus}}\ p_{t,a}^{\text{surplus}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}4)
$$

**Tertiary reserve shortage cost**

$$
Cost_{a,t}^{\text{Tert,short}} = C_{a}^{\text{tert,short}} \left( p_{t,a}^{\text{Tert}\,\text{UP, short}} + p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \right)
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}5)
$$

**Renewable energy output suppression cost**

$$
Cost_{a,t,\text{RE}}^{\text{suppr}} = C_{a,\text{PV}}^{\text{suppr}}\ p_{t,a,\text{PV}}^{\text{suppr}} + C_{a,\text{WF}}^{\text{suppr}}\ p_{t,a,\text{WF}}^{\text{suppr}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}6)
$$

## Cost of the ESS $Cost_{ess,t}$

### In the case of `formulation_type: "delta-kW-no-market"`

(Default) The tertiary reserve procurement cost of the ESS is not included ($Cost_{ess,t} = 0$).

### In the case of `formulation_type: "delta-kW-bid"`

As with the generators, the tertiary reserve procurement cost is included, evaluated with ΔkW as the unit in day-ahead scheduling and kWh in intra-day scheduling.

$$
Cost_{ess,t} =
\begin{cases}
C_{ess}^{\Delta\text{kW}\,\text{UP}}\ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} + C_{ess}^{\Delta\text{kW}\,\text{DOWN}}\ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} & (\text{day-ahead scheduling}) \\
C_{ess}^{\text{kWh}\,\text{UP}}\ p_{t,ess}^{\text{id}\,\text{UP}} + C_{ess}^{\text{kWh}\,\text{DOWN}}\ p_{t,ess}^{\text{id}\,\text{DOWN}} & (\text{intra-day scheduling})
\end{cases}
\qquad \forall t \in T,\ \forall ess \in \textit{ESS} \qquad (1\text{-}7)
$$

---

## Penalty terms (common to both modes)

The stored-energy plan deviation penalty of the ESS and the tie-line usage penalty. These are identical for `delta-kW-no-market` and `delta-kW-bid`.

$$
\begin{aligned}
    Penalty_{ess,t} = &
    C_{ess}^{\text{short}}\ e_{t,ess}^{\text{short}} + C_{ess}^{\text{surplus}}\ e_{t,ess}^{\text{surplus}}
    & \forall t \in T, \forall ess \in \textit{ESS}
    & \qquad (1\text{-}8)
    \\
    Penalty_{tie,t} = &
    C_{tie}^{\text{penalty}} \left( p_{t,tie}^{\text{forward}} + p_{t,tie}^{\text{counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
    \+ p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
    \+ p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
    \+ p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
    \+ p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right)
    & \forall t \in T, \forall tie \in \textit{TIE}
    & \qquad (1\text{-}9)
\end{aligned}
$$
