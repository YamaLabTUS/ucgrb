# Constraints on area

> **Conditional branching by [`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type)**
> The items on this page related to ΔkW (day-ahead scheduling) / kWh (intra-day scheduling) are effective only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). In `delta-kW-no-market` (default), the tertiary reserve is treated as a single reserve quantity, and these items are disabled.

The following constraints can be considered for each area.

- power balance constraints
- GF&LFC reserve constraints
- tertiary reserve constraints
  - There are two types of reserve: reserve-up, which compensates for the difference between the forecasted output of RE power and its minimum forecasted value, and reserve-down, which compensates for the difference between the forecasted output of RE power and its maximum forecasted value.
- required inertia constant constraint

See the following pages for definitions of each set, index, parameter, and decision variable.

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

## 1. Power balance constraints

$$
\begin{aligned}
   \sum_{g \in G_{a}}
   p_{t,g}+ P_{t,a,\text{Others}}
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
    & \qquad (2\text{-}1\text{-}1\text{-}1)
\end{aligned}
$$

## 2. GF&LFC reserve constraints

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}1)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}2)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}5)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}2\text{-}6)
\end{aligned}
$$

## 3. Required GF&LFC reserve constraints

$$
\begin{aligned}
   D_{t,a}^{\text{GF\\&LFC}\,\text{UP, req}}
    & =  D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}1)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}2)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
   D_{t,a}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}4)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}5)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}6)
\end{aligned}
$$

By editing the configuration file, you can easily change whether or not each formula is taken into account. The settings are as follows:

| Condition name                                             | Default value | Setting name on the configuration file  | Change in required GF&LFC reserve when set to False |
| :--------------------------------------------------------- | :------------ | :-------------------------------------- | :---------------------------------------------------- |
| Demand-induced required GF&LFC up-reserve availability   | True          | consider_required_gf_lfc_up_by_demand   | Set the right-hand side of equation (2-1-3-1) to 0    |
| PV-induced required GF&LFC up-reserve availability       | True          | consider_required_gf_lfc_up_by_pv       | Set the right-hand side of equation (2-1-3-2) to 0    |
| WF-induced required GF&LFC up-reserve availability       | True          | consider_required_gf_lfc_up_by_wf       | Set the right-hand side of equation (2-1-3-3) to 0    |
| Demand-induced required GF&LFC down-reserve availability | False         | consider_required_gf_lfc_down_by_demand | Set the right-hand side of equation (2-1-3-4) to 0    |
| PV-induced required GF&LFC down-reserve availability     | False         | consider_required_gf_lfc_down_by_pv     | Set the right-hand side of equation (2-1-3-5) to 0    |
| WF-induced required GF&LFC down-reserve availability     | False         | consider_required_gf_lfc_down_by_wf     | Set the right-hand side of equation (2-1-3-6) to 0    |

## 4. Tertiary reserve constraints

The reserve quantity handled by the tertiary reserve securing constraint differs depending on `formulation_type`. In `delta-kW-no-market`, the tertiary reserve is secured as a single quantity $p_{t,g}^{\text{Tert}\,\text{UP/DOWN}}$. In `delta-kW-bid`, it is secured in day-ahead scheduling as the ΔkW-value tertiary reserve $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$ (in `delta-kW-bid`, this constraint is considered only in day-ahead scheduling; it is not considered in intra-day scheduling).

### In the case of `formulation_type: "delta-kW-no-market"`

(default) The tertiary reserve is secured as a single quantity $p_{t,g}^{\text{Tert}\,\text{UP/DOWN}}$.

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}4\text{-}1)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}4\text{-}2)
\end{aligned}
$$

Since $p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}$ and $p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}$ may take negative values, a constraint requiring the total up-reserve to be greater than or equal to zero is added as equation (2-1-4-3).

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}4\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}4\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
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
    & \qquad (2\text{-}1\text{-}4\text{-}5)
\end{aligned}
$$

### In the case of `formulation_type: "delta-kW-bid"`

In day-ahead scheduling, the tertiary reserve is secured as the ΔkW-value $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$. In `delta-kW-bid`, this constraint is considered **only in day-ahead scheduling**; it is not considered in intra-day scheduling (in intra-day scheduling it is handled as the kWh-value reserve energy).

#### Day-ahead scheduling

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
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
    & \qquad (2\text{-}1\text{-}4\text{-}6)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
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
    & \qquad (2\text{-}1\text{-}4\text{-}7)
\end{aligned}
$$

Since $p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}$ and $p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}$ may take negative values, a constraint requiring the total up-reserve to be greater than or equal to zero is added as equation (2-1-4-8).

$$
\begin{aligned}
 \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
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
    & \qquad (2\text{-}1\text{-}4\text{-}8)
\end{aligned}
$$

$$
\begin{aligned}
  \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
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
    & \qquad (2\text{-}1\text{-}4\text{-}9)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
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
    & \qquad (2\text{-}1\text{-}4\text{-}10)
\end{aligned}
$$

## 5. Required tertiary reserve constraints

$$
\begin{aligned}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} - P_{t,a,\text{PV}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}1)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} - P_{t,a,\text{WF}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}2)
\end{aligned}
$$

$$
\begin{aligned}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{upper}} - P_{t,a,\text{PV}}^{\text{output}}+ p_{t,a,\text{PV}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}3)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{upper}} - P_{t,a,\text{WF}}^{\text{output}}+ p_{t,a,\text{WF}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}4)
\end{aligned}
$$

By editing the configuration file, you can easily change whether or not each formula is taken into account. The settings are as follows:

| Condition name                                         | Default value | Setting name on the configuration file | Change in required tertiary reserve when set to False |
| :----------------------------------------------------- | :------------ | :------------------------------------- | :---------------------------------------------------- |
| PV-induced required tertiary up-reserve availability   | True          | consider_required_tert_up_by_pv        | Set the right-hand side of equation (2-1-5-1) to 0    |
| WF-induced required tertiary up-reserve availability   | True          | consider_required_tert_up_by_wf        | Set the right-hand side of equation (2-1-5-2) to 0    |
| PV-induced required tertiary down-reserve availability | False         | consider_required_tert_down_by_pv      | Set the right-hand side of equation (2-1-5-3) to 0    |
| WF-induced required tertiary down-reserve availability | False         | consider_required_tert_down_by_wf      | Set the right-hand side of equation (2-1-5-4) to 0    |

## 6. Required inertia constant constraint

$$
\begin{aligned}
   \sum_{g \in G_{N\\&T,a}} P_{g}^{\text{MAX}} u_{t,g} M_{g}
  \+ \sum_{g \in G_{HYDRO,a}} P_{g}^{\text{MAX}} M_{g} \notag
   \\
  \+ \sum_{ess \in ESS_{a}} P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess} M_{p}
    & \geq D_{t,a} M_{t,a}^{\text{req}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}6\text{-}1)
\end{aligned}
$$

By editing the configuration file, you can easily change whether or not the above formula is taken into account. The setting is as follows:

| Condition name                         | Default value | Setting name on the configuration file | Change in required inertia constant constraint when set to False |
| :------------------------------------- | :------------ | :------------------------------------- | :--------------------------------------------------------------- |
| required inertia constant availability | True          | consider_require_inertia               | Set the right-hand side of the above equation to 0               |
