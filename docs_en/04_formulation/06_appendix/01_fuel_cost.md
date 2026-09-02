# Calculation method for the output proportionality coefficient of the fuel cost function and the unit price of reserve energy for nuclear and thermal generation

> **Note**: The items on this page such as ΔkW / kWh / p^id are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

See the following pages for definitions of each subscript, set, constant, and decision variable.

- [Sets and indices](../03_set_and_index.md)
- Parameters
  1. [Parameters for area](../04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](../04_parameter/02_generation.md)
  3. [Parameters for renewable energy](../04_parameter/03_re.md)
  4. [Parameters for energy storage system](../04_parameter/04_ess.md)
  5. [Parameters for tie line](../04_parameter/05_tie.md)
  6. [Parameters that depends on scheduling kind](../04_parameter/06_depend_on_scheduling_kind.md)
- Decision variables
  1. [Variables for area](../05_variable/01_area.md)
  2. [Variables for large-scale power generation](../05_variable/02_generation.md)
  3. [Variables for renewable energy](../05_variable/03_re.md)
  4. [Variables for energy storage system](../05_variable/04_ess.md)
  5. [Variables for tie line](../05_variable/05_tie.md)

## Output proportionality coefficient of the fuel cost function

$$
\begin{aligned}
   C_{g}^{\text{coef}}
    & = \frac{C_{g}^{\text{fuel}}}{\left( 1 - \frac{ICR_{g}}{100}\right)}
    & \forall g \in G_{N\\&T}
    & \qquad (6\text{-}1\text{-}1)
\end{aligned}
$$

## Unit price of reserve energy

$$
\begin{aligned}
   C_{g}^{\text{kWh}\,\text{UP}}
    & = \frac{C_{g}^{\text{fuel}\,\text{kWh}\,\text{UP}}}{\left( 1 - \frac{ICR_{g}}{100}\right)}
    & \forall g \in G_{N\\&T}
    \\
   C_{g}^{\text{kWh}\,\text{DOWN}}
    & = \frac{C_{g}^{\text{fuel}\,\text{kWh}\,\text{DOWN}}}{\left( 1 - \frac{ICR_{g}}{100}\right)}
    & \forall g \in G_{N\\&T}
\end{aligned}
$$

$$
\begin{array}{ll}
      C_{g}^{{\text{fuel}}}
       & : \text{Fuel cost proportionality coefficient for nuclear and thermal generation $g$ [kYen/MWh]}
      \\
      C_{g}^{\text{fuel}\,\text{kWh}\,\text{UP}}
       & : \text{Unit price of upward reserve energy (kWh) for nuclear and thermal generation $g$ (before accounting for the internal consumption rate) [kYen/MWh]}
      \\
      C_{g}^{\text{fuel}\,\text{kWh}\,\text{DOWN}}
       & : \text{Unit price of downward reserve energy (kWh) for nuclear and thermal generation $g$ (before accounting for the internal consumption rate) [kYen/MWh]}
      \\
      ICR_{g}
       & : \text{Internal consumption rate of nuclear and thermal generation $g$ [\%]}
\end{array}
$$
