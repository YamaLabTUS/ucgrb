# Calculation methods for maximum and minimum output of nuclear and thermal generation

See the following pages for definitions of each subscript, set, constant, and decision variable.
- [Sets and indices](../03_set_and_index.md)
- constant
  1. [Parameters for area](../04_parameter/01_area.md)
  2. [Parameters for large-scale power generation](../04_parameter/02_generation.md)
  3. [Parameters for renewable energy](../04_parameter/03_re.md)
  4. [Parameters for energy storage system](../04_parameter/04_ess.md)
  5. [Parameters for tie line](../04_parameter/05_tie.md)
  6. [Parameters that depends on scheduling kind](../04_parameter/06_depend_on_scheduling_kind.md)
- decision variable
  1. [Variables for area](../05_variable/01_area.md)
  2. [Variables for large generators](../05_variable/02_generation.md)
  3. [Variables for renewable energy](../05_variable/03_re.md)
  4. [Variables for energy storage systems (ESS)](../05_variable/04_ess.md)
  5. [Variables for interconnection lines](../05_variable/05_tie.md)


$$
\begin{aligned}
   P_{g}^{\text{MAX}}
    & = \left( 1 - \frac{ICR_{g}}{100} \right) P_{g}^{\text{MAX,GENE} \\_ \text{END}}
    & \forall g \in G_{N\\&T}
    & \qquad (6\text{-}2\text{-}1)
\\
   P_{g}^{\text{MIN}}
    & = \left( 1 - \frac{ICR_{g}}{100} \right) P_{g}^{\text{MIN,GENE} \\_ \text{END}}
    & \forall g \in G_{N\\&T}
    & \qquad (6\text{-}2\text{-}2)
\end{aligned}
$$

$$
   \begin{array}{ll}
      P_{g}^{\text{MAX,GENE} \\_ \text{END}}
       & : \text{Maximum output at generating end of nuclear and thermal generation $g$ [MW]}
      \\
      P_{g}^{\text{MIN,GENE} \\_ \text{END}}
       & : \text{Minimum output power at generating end of nuclear and thermal generation $g$ [MW]}
   \end{array}
$$
