# Parameters for large-scale power generation

> **Note**: The items on this page such as ΔkW / kWh / $p^{\text{id}}$ are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

## Parameters common to both modes

Constants used in both `delta-kW-no-market` and `delta-kW-bid`, such as fuel cost, output capability, startup cost, and operating constraints.

$$
\begin{array}{ll}
      C_{g}^{\text{coef}}
       & : \text{Coefficient of the output proportional term of the fuel cost function of large-scale power $g$ [kYen/MWh]}
      \\
      C_{g}^{\text{intc}}
       & : \text{Intercept term in the fuel cost function of large-scale power generation $g$ [kYen/h]}
      \\
      C_{g}^{\text{startup}}
       & : \text{Startup cost of large-scale power generation $g$ [kYen]}
      \\
      P_{g}^{\text{MAX}}
       & : \text{Maximum output of large-scale power generation $g$ [MW]}
      \\
      P_{t,g}^{\text{des}}
       & : \text{Temporary output reduction of large-scale power generation $g$ at time $t$ [MW]}
      \\
      P_{g}^{\text{MIN}}
       & : \text{Minimum output of large-scale power generation $g$ [MW]}
      \\
      R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}
       & : \text{GF\\&LFC reserve availability percentage of large-scale power generation $g$ [\\%]}
      \\
      M_{g}
       & : \text{Per-unit inertia constant of large-scale power generation $g$ [MW$\cdot$s/MVA]}
      \\
      E_{g}^{N\text{day}\text{MAX}}
       & : \text{Upper limit of energy output of large-scale power generation $g$ every $N$ days [MWh]}
      \\
      t^{EN\text{day}\text{MAX}}
       & : \text{Start time of accumulation for $N$-day upper limit of energy output of large-scale power generation $g$ [Date and Time].}
      \\
      P_{t,g}^{\text{INHE}}
       & : \text{Average output of large-scale power generation $g$ at time $t$ determined in the previous optimization [MW]}
\end{array}
$$

## Parameters used only in `delta-kW-bid` (day-ahead scheduling)

Unit procurement cost of the tertiary reserve (ΔkW, kW value).

$$
\begin{array}{ll}
      C_{g}^{\Delta\text{kW}\,\text{UP}}
       & : \text{Unit procurement cost of the tertiary up-reserve ($\Delta$kW) of large-scale power generation $g$ [kYen/MW]}
      \\
      C_{g}^{\Delta\text{kW}\,\text{DOWN}}
       & : \text{Unit procurement cost of the tertiary down-reserve ($\Delta$kW) of large-scale power generation $g$ [kYen/MW]}
\end{array}
$$

## Parameters used only in `delta-kW-bid` (intra-day scheduling)

Unit procurement cost of the tertiary reserve energy (kWh), and the average generation output and tertiary reserve (ΔkW) inherited from day-ahead scheduling.

$$
\begin{array}{ll}
      C_{g}^{\text{kWh}\,\text{UP}}
       & : \text{Unit procurement cost of the tertiary up-reserve energy (kWh) of large-scale power generation $g$ [kYen/MWh]}
      \\
      C_{g}^{\text{kWh}\,\text{DOWN}}
       & : \text{Unit procurement cost of the tertiary down-reserve energy (kWh) of large-scale power generation $g$ [kYen/MWh]}
      \\
      P_{t,g}^{\text{da}}
       & : \text{Average generation output of large-scale power generation $g$ at time $t$ determined in day-ahead scheduling [MW]}
      \\
      P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : \text{Tertiary up-reserve ($\Delta$kW) of large-scale power generation $g$ at time $t$ determined in day-ahead scheduling [MW]}
      \\
      P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : \text{Tertiary down-reserve ($\Delta$kW) of large-scale power generation $g$ at time $t$ determined in day-ahead scheduling [MW]}
\end{array}
$$

## Parameters related to nuclear and thermal generation only

$$
\begin{array}{ll}
      MinUpTime_{g}
       & : \text{Minimum up time of nuclear and thermal generation $g$ [h]}
      \\
      MinDownTime_{g}
       & : \text{Minimum down time of nuclear and thermal generation $g$ [h]}
      \\
      U_{t,g}^{\text{INHE}}
       & : \text{Operating state of nuclear and thermal generation $g$ at time $t$ determined in the previous optimization (binary, 1: operating,0: stopping)}
      \\
      SU_{t,g}^{\text{INHE}}
       & : \text{Whether nuclear or thermal generation $g$ started at time $t$ in the previous optimization (binary, 1: started, 0: not started)}
      \\
      SD_{t,g}^{\text{INHE}}
       & : \text{Whether nuclear or thermal generation $g$ stopped at time $t$ in the previous optimization (binary, 1: stopped, 0: not stopped)}
      \\
      R_{g}^{\text{ramp,MAX}}
       & : \text{Maximum ramp ratio of nuclear and thermal generation $g$ [\\%MW/min.]}
\end{array}
$$

## Parameters related to hydro generation only

$$
\begin{array}{ll}
      U_{t,g}
       & : \text{Operating state of hydro generation $g$ at time $t$ (binary, 1: operating, 0: stopping)}
\end{array}
$$
