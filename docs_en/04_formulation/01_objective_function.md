# Objective function

The objective function of the optimization is total cost minimization for all areas for the period under optimization. The cost  is consists of the components as follows.
- Linearized fuel cost and start-up cost for large-scale power generations $Cost_{g,t}$
- Power supply shortage cost in each area $Cost_{a,t}^{\text{short}}$
- Power supply surplus penalty in each area $Cost_{a,t}^{\text{surplus}}$
- Tertiary reserve shortage cost in each area $Cost_{a,t}^{\text{Tert,short}}$
- Renewable energy output curtailment penalty cost for each area $Cost_{a,t,\text{RE}}^{\text{suppr}}$
  - Currently in Japan, there are no rules for paying for output suppression.
- Energy storage system (ESS) energy storage plan deviation penalty $Penalty_{ess,t}$
- Penalty for using tie lines $Penalty_{tie,t}$
  - Penalty term to avoid energy cycling caused by looped tie lines. The user does not actually pay the usage fee.

See the following pages for definitions of each set, index, constant, and variable.
- [Sets and indies](03_set_and_index.md)
- Parameters
  1. [Parameters for area](04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](04_parameter/02_generation.md)
  3. [Parameters for renewable energy](04_parameter/03_re.md)
  4. [Parameters for energy storage system](04_parameter/04_ess.md)
  5. [Parameters for tie line](04_parameter/05_tie.md)
  6. [Parameters that depends on scheduling kind](04_parameter/06_depend_on_scheduling_kind.md)
- Variables
  1. [Variables for area](05_variable/01_area.md)
  2. [Variables for large-scale power generation](05_variable/02_generation.md)
  3. [Variables for renewable energy](05_variable/03_re.md)
  4. [Variables for energy storage system](05_variable/04_ess.md)
  5. [Variables for tie line](05_variable/05_tie.md)

$$
\begin{align}
         \min \ F = \sum_{t \in T} & \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) \right.
                  \\
                  & \left.  + \sum_{ess \in \textit{ESS}} Penalty_{ess,t}  +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} \right]
\end{align}
$$

--------------

$$
\begin{align}
    Cost_{g,t} = &
    C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g}
    + C_{g}^{\text{startup}}\ su_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
    Cost_{a,t}^{\text{short}} = &
    C_{a}^{\text{short}}\ p_{t,a}^{\text{short}}
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\\
    Cost_{a,t}^{\text{surplus}} = &
    C_{a}^{\text{surplus}}\ p_{t,a}^{\text{surplus}}
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\\
    Cost_{a,t}^{\text{Tert,short}} = &
    C_{a}^{\text{tert,short}} \left( p_{t,a}^{\text{Tert}\,\text{UP, short}} +
    p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \right)
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\\
    Cost_{a,t,\text{RE}}^{\text{suppr}} = &
    C_{a,\text{PV}}^{\text{suppr}} p_{t,a,\text{PV}}^{\text{suppr}} +
    C_{a,\text{WF}}^{\text{suppr}} p_{t,a,\text{WF}}^{\text{suppr}}
    & \forall t \in T, \forall a \in A
    & \qquad (5)
\end{align}
$$

--------------

$$
\begin{align}
    Penalty_{ess,t} = &
    C_{ess}^{\text{short}}\ e_{t,ess}^{\text{short}} + C_{ess}^{\text{surplus}}\ e_{t,ess}^{\text{surplus}}
    & \forall t \in T, \forall ess \in \textit{ESS}
    & \qquad (6)
    \\
    Penalty_{tie,t} = &
    C_{tie}^{\text{penalty}} \left( p_{t,tie}^{\text{forward}} + p_{t,tie}^{\text{counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
    + p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
    + p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
    + p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
    + p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right)
    & \forall t \in T, \forall tie \in \textit{TIE}
    & \qquad (7)
\end{align}
$$
