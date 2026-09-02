# Method for calculating CO<sub>2</sub> emissions of large-scale power generation

See the following pages for the definitions of each subscript, set, parameter, and decision variable.
- [Sets and indices](../03_set_and_index.md)
- Parameters
  1. [Parameters for area](../04_parameter/01_area.md)
  2. [Parameters for large generators](../04_parameter/02_generation.md)
  3. [Parameters for renewable energy](../04_parameter/03_re.md)
  4. [Parameters for energy storage systems (ESS)](../04_parameter/04_ess.md)
  5. [Parameters for tie lines](../04_parameter/05_tie.md)
  6. [Parameters dependent on the scheduling kind](../04_parameter/06_depend_on_scheduling_kind.md)
- Decision variables
  1. [Variables for area](../05_variable/01_area.md)
  2. [Variables for large generators](../05_variable/02_generation.md)
  3. [Variables for renewable energy](../05_variable/03_re.md)
  4. [Variables for energy storage systems (ESS)](../05_variable/04_ess.md)
  5. [Variables for tie lines](../05_variable/05_tie.md)


$$
\begin{aligned}
   F_{t,g,\text{CO} _ {2}}
    & = \begin{cases}
           0 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  \ \ \ \ \ \ \ \left(g \\_ type_{g} \in \\{\text{HYDRO},\text{NUCL}\\}\right) \\
           C_{g,\text{CO} _ 2}^{\text{coef}}\ p_{t,g} + C_{g,\text{CO} _ 2}^{\text{intc}}\ u_{t,g} + C_{g,\text{CO} _ 2}^{\text{startup}}\ su_{t,g}
           \\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \left(g \\_ type_{g} \in \\{\text{OIL},\text{GAS},\text{COAL}\\}\right)
        \end{cases}
    & \forall t \in T, \forall g \in G
    & \qquad (6\text{-}3\text{-}1)
\end{aligned}
$$

$$
\begin{aligned}
   C_{g,\text{CO} _ {2}}^{\text{coef}}
    & = \frac{EMIS_{g}^{\text{MAX}} - EMIS_{g}^{\text{MIN}}}{P_{g}^{\text{MAX}} - P_{g}^{\text{MIN}}}
    & \forall g \in G
    & \qquad (6\text{-}3\text{-}2)
\\
   C_{g,\text{CO} _ 2}^{\text{intc}}
    & = EMIS_{g}^{\text{MIN}} - C_{g,\text{CO} _ 2}^{\text{coef}} P_{g}^{\text{MIN}}
    & \forall g \in G
    & \qquad (6\text{-}3\text{-}3)
\\
   C_{g,\text{CO} _ 2}^{\text{startup}}
    & = \frac{C_{g}^{\text{startup}}EF_{g \\_ type_{g}}^{\text{startup}}}{FuelPrice_{g \\_ type_{g}}^{\text{startup}}}
    & \forall g \in G
    & \qquad (6\text{-}3\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
   EMIS_{g}^{\text{MAX}}
    & = EF_{g \\_ type_{g}} FCPUMC_{g \\_ type_{g}} HR_{g}^{\text{MAX}} P_{g}^{MAX,GENE \\_ END}
    & \forall g \in G
    & \qquad (6\text{-}3\text{-}5)
   \\
   EMIS_{g}^{\text{MIN}}
    & = EF_{g \\_ type_{g}} FCPUMC_{g \\_ type_{g}} HR_{g}^{\text{MIN}} P_{g}^{MIN,GENE \\_ END}
    & \forall g \in G
    & \qquad (6\text{-}3\text{-}6)
\end{aligned}
$$

$$
\begin{array}{ll}
      F_{t,g,\text{CO} _ 2}
       & : \text{$\text{CO} _ 2$ emissions of large-scale power generation $g$ at time $t$ [t$\text{CO} _ 2$]}
      \\
      C_{g,\text{CO} _ 2}^{\text{coef}}
       & : \text{$\text{CO} _ 2$ emissions per unit output of large-scale power generation $g$ [t$\text{CO} _ 2$/MWh]}
      \\
      C_{g,\text{CO} _ 2}^{\text{intc}}
       & : \text{$\text{CO} _ 2$ emissions per unit time of large-scale power generation $g$ [t$\text{CO} _ 2$]}
      \\
      C_{g,\text{CO} _ {2}}^{\text{startup}}
       & : \text{$\text{CO} _ 2$ emissions per start-up of large-scale power generation $g$ [t$\text{CO} _ 2$]}
      \\
      EMIS_{g}^{\text{MAX}}
       & : \text{$\text{CO} _ 2$ emissions of large-scale power generation $g$ at maximum output [t$\text{CO} _ 2$]}
      \\
      EMIS_{g}^{\text{MIN}}
       & : \text{$\text{CO} _ 2$ emissions of large-scale power generation $g$ at minimum output [t$\text{CO} _ 2$]}
      \\
      EF_{g \\_ type_{g}}
       & : \text{Emission factor of large-scale power generation type $g \\_ type$ [t$\text{CO} _ 2$/t or kl]}
      \\
      FCPUMC_{g \\_ type_{g}}
       & : \text{Fuel consumption per unit calorific value of large-scale power generation type $g \\_ type$ [t or kl/Mcal]}
      \\
      HR_{g}^{\text{MAX}}
       & : \text{Heat rate (heat consumption rate) at maximum output of large-scale power generation $g$ [Mcal/MWh]}
      \\
      HR_{g}^{\text{MIN}}
       & : \text{Heat rate (heat consumption rate) at minimum output of large-scale power generation $g$ [Mcal/MWh]}
      \\
      EF_{g \\_ type_{g}}^{\text{startup}}
       & : \text{Emission factor at start-up of large-scale power generation type $g \\_ type$ [t$\text{CO} _ 2$/t or kl]}
      \\
      FuelPrice_{g \\_ type_{g}}^{\text{startup}}
       & : \text{Fuel cost coefficient at start-up of large-scale power generation type $g \\_ type$ [kYen/t or kl]}
\end{array}
$$

※ When the large generator type $`g\\_type`$ is hydro or nuclear, the CO<sub>2</sub> emissions $F_{t,g,\text{CO} _ 2}$ are fixed at 0.
