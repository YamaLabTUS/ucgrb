# Changes in formulation due to time granularity modification

This formulation assumes that the time granularity during optimization execution is 1 hour (60 minutes).
In this program, the optimization can be performed with any time granularity by changing the setting value [`time_series_granularity`](../../06_config/02_input_data_and_solver.md#time_series_granularity).
In such cases, various data and formulation contents are modified as follows.

Hereafter, the ratio between the set time granularity and 60 minutes is denoted as $TSGRatio$. For example, when the set time granularity is 30 minutes, $TSGRatio=0.5$, and when the set time granularity is 2 hours, $TSGRatio=2$.

See the following pages for definitions of each subscript, set, constant, and decision variable other than $TSGRatio$.
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


## Time series data interpolation

The granularity of the input data time series is also automatically converted within this program according to the time granularity setting. The conversion method depends on the **relationship between the input data granularity and the set granularity**.

- When the granularity of the input data time series is **finer** than the set granularity (e.g., 15-minute input with a 60-minute setting), the data is **aggregated by averaging**.
- When the granularity of the input data time series is **coarser** than the set granularity (e.g., 60-minute input with a 15-minute setting), intermediate values are generated through linear or rectangular **interpolation**.

> For a fixed input granularity, the **finer** the set granularity, the more **interpolation** is applied; the **coarser** it is, the more **averaging (aggregation)** is applied.

Specifically, the time series set in [`time_series_to_be_linearly_interpolated`](../../06_config/02_input_data_and_solver.md#time_series_to_be_linearly_interpolated) are linearly interpolated, while the other time series are rectangularly interpolated.


## Modification of minimum up time and minimum down time

The minimum up time and minimum down time described in [Parameters for large-scale power generation](../04_parameter/02_generation.md) are expressed in hours and therefore need to be modified according to the time granularity. Specifically, after dividing by $TSGRatio$, the result is rounded to the nearest integer at the first decimal place. If the rounding results in 0, it is replaced with 1. This is a measure to satisfy the conditional expressions of the [Minimum required operation time constraint for nuclear and thermal power generators](../02_constraint/02_generation.md) and the [Minimum required shutdown time constraint](../02_constraint/02_generation.md).

## Changes in formulation content

### [Objective function](../01_objective_function.md)
All elements except the startup cost are multiplied by $TSGRatio$.

$$
\begin{aligned}
         \min \ F = &  \sum_{t \in T} \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) TSGRatio \right.
                  \notag \\
                  & \left.  + \sum_{ess \in \textit{ESS}} Penalty_{ess,t} TSGRatio +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} TSGRatio \right]
    & \qquad (6\text{-}4\text{-}1)
                  \\
         Cost_{g,t} = &
         C_{g}^{\text{coef}}\ p_{t,g} TSGRatio + C_{g}^{\text{intc}}\ u_{t,g} TSGRatio
         \+ C_{g}^{\text{startup}}\ su_{t,g}
         & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}2)
\end{aligned}
$$


### [Upper limit constraint on power generation per N days for large generators](../02_constraint/02_generation.md)

$$
\begin{aligned}
   \sum_{i = t}^{t + \frac{24N}{TSGRatio} - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + \frac{24N}{TSGRatio} \times m \; (m = 0,1,2\dots), \forall g \in G
    & \qquad (6\text{-}4\text{-}3)
\end{aligned}
$$

### [Rate of output change constraint for nuclear and thermal power generators](../02_constraint/02_generation.md)

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}TSGRatio}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}4)
\\
   p_{t,g} - p_{t,g}^{\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}TSGRatio}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}5)
\end{aligned}
$$

### [Stored energy operation constraint for energy storage system](../02_constraint/04_ess.md)

$$
\begin{aligned}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}} TSGRatio}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}} TSGRatio
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}6)
\end{aligned}
$$

### [Maximum stored energy constraint for energy storage system](../02_constraint/04_ess.md)
$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right) TSGRatio
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}7)
\end{aligned}
$$

### [Minimum stored energy constraint for energy storage system](../02_constraint/04_ess.md)
$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}} TSGRatio
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}8)
\end{aligned}
$$
