# Constraints on area

The following constraints may be considered for each area
- supply and demand balance constraints
- GF&LFC reserve constraints
- tertiary reserve constraint
  - There are two types of reserve: the first is reserve-up which compensates for the difference between the forecasted output of RE power and the minimum forecasted output, and the second is reserve-down which compensates for the difference between the forecasted output of RE power and the maximum forecasted output.
- Constraints of requirement of inertia

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

## Power balance constraints

$$
\begin{align}
   \sum_{g \in G_{a}}
   p_{t,g}\+ P_{t,a,\text{Others}}
  \+ \sum_{ess \in ESS_{a}} \left(
   p_{t,ess}^{\text{discharge}} - p_{t,ess}^{\text{charge}} \right) \notag
   \\
  \+ P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}}
  \+ P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}}
   \left( p_{t,tie}^{\text{forward}} - p_{t,tie}^{\text{counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}}
   \left( p_{t,tie}^{\text{counter}} - p_{t,tie}^{\text{forward}} \right) \notag
   \\
  \+ p_{t,a}^{\text{short}} - p_{t,a}^{\text{surplus}}
    & = D_{t,a}
    & \forall t \in T, \forall a \in A
\end{align}
$$



## GF&LFC reserve constraints

$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq D_{t,a}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (1)
\end{align}
$$

$$
\begin{align}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\end{align}
$$

$$
\begin{align}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\end{align}
$$

$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq D_{t,a}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\end{align}
$$


$$
\begin{align}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (5)
\end{align}
$$

$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (6)
\end{align}
$$

## Required GF&LFC reserve constraints

$$
\begin{align}
   D_{t,a}^{\text{GF\\&LFC}\,\text{UP, req}}
    & =  D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (1)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\end{align}
$$

$$
\begin{align}
   D_{t,a}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (5)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (6)
\end{align}
$$

By editing the configuration file, you can easily change whether or not each formula is taken into account. The settings are as follows:

| Condition name                                             | Default value | Setting name on the configuration file  | Change in required GF & LFC reserve when set to False |
| :--------------------------------------------------------- | :------------ | :-------------------------------------- | :---------------------------------------------------- |
| Demand-induced required GF & LFC up-reserve availability   | True          | consider_required_gf_lfc_up_by_demand   | Set the right-hand side of equation (1) to 0          |
| PV-induced required GF & LFC up-reserve availability       | True          | consider_required_gf_lfc_up_by_pv       | Set the right-hand side of equation (2) to 0          |
| WF-induced required GF & LFC up-reserve availability       | True          | consider_required_gf_lfc_up_by_wf       | Set the right-hand side of equation (3) to 0          |
| Demand-induced required GF & LFC down-reserve availability | False         | consider_required_gf_lfc_down_by_demand | Set the right-hand side of equation (4) to 0          |
| PV-induced required GF & LFC down-reserve availability     | False         | consider_required_gf_lfc_down_by_pv     | Set the right-hand side of equation (5) to 0          |
| WF-induced required GF & LFC down-reserve availability     | False         | consider_required_gf_lfc_down_by_wf     | Set the right-hand side of equation (6) to 0          |

## Tertiary reserve constraints



$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (1)
\end{align}
$$

$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}}
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}  \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\end{align}
$$

Add a constraint equation (3) as the total value of the raising reserve must be greater than or equal to zero,　because　$p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}$ 、 $p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}$ the possibility of taking negative values,

$$
\begin{align}
 \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq 0
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\end{align}
$$

$$
\begin{align}
  \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\end{align}
$$

$$
\begin{align}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (5)
\end{align}
$$

## Required tertiary reserve constraints

$$
\begin{align}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} - P_{t,a,\text{PV}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (1)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} - P_{t,a,\text{WF}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\end{align}
$$

$$
\begin{align}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{upper}} - P_{t,a,\text{PV}}^{\text{output}}\+ p_{t,a,\text{PV}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{upper}} - P_{t,a,\text{WF}}^{\text{output}}\+ p_{t,a,\text{WF}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\end{align}
$$

By editing the configuration file, you can easily change whether or not each formula is taken into account. The settings are as follows:

| Condition name                                         | Default value | Setting name on the configuration file | Change in required tertiary reserve when set to False |
| :----------------------------------------------------- | :------------ | :------------------------------------- | :---------------------------------------------------- |
| PV-induced required tertiary up-reserve availability   | True          | consider_required_tert_up_by_pv        | Set the right-hand side of equation (1) to 0          |
| WF-induced required tertiary up-reserve availability   | True          | consider_required_tert_up_by_wf        | Set the right-hand side of equation (2) to 0          |
| PV-induced required tertiary down-reserve availability | False         | consider_required_tert_down_by_pv      | Set the right-hand side of equation (3) to 0          |
| WF-induced required tertiary down-reserve availability | False         | consider_required_tert_down_by_wf      | Set the right-hand side of equation (4) to 0          |



## Required inertia constant constraint

$$
\begin{align}
   \sum_{g \in G_{N\\&T,a}} P_{g}^{\text{MAX}} u_{t,g} M_{g}
  \+ \sum_{g \in G_{HYDRO,a}} P_{g}^{\text{MAX}} M_{g} \notag
   \\
  \+ \sum_{ess \in ESS_{a}} P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess} M_{p}
    & \geq D_{t,a} M_{t,a}^{\text{req}}
    & \forall t \in T, \forall a \in A
\end{align}
$$

By editing the configuration file, you can easily change whether or not each formula is taken into account. The settings are as follows:

| Condition name                         | Default value | Setting name on the configuration file | Change in required inertia constant constraint when set to False |
| :------------------------------------- | :------------ | :------------------------------------- | :--------------------------------------------------------------- |
| required inertia constant availability | True          | consider_require_inertia               | Set the right-hand side of the above equation to 0               |
