# Decision variables for large-scale power generation

> **Note**: The items on this page such as ΔkW / kWh / p^id are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

Unless otherwise stated, all decision variables x are non-negative real numbers. $x \in R_{+}$ (non-negative real numbers)

## Decision variables common to both modes

$$
\begin{array}{ll}
      p_{t,g}
       & : \text{Average output of large-scale power generation $g$ at time $t$ [MW]}
      \\
      p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
       & : \text{GF\\&LFC up reserve ability of large-scale power generation $g$ at time $t$ [MW]}
      \\
      p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
       & : \text{GF\\&LFC down reserve ability of large-scale power generation $g$ at time $t$ [MW]}
\end{array}
$$

## Decision variables used only in `delta-kW-no-market`

$$
\begin{array}{ll}
      p_{t,g}^{\text{Tert}\,\text{UP}}
       & : \text{Tertiary up reserve ability of large-scale power generation $g$ at time $t$ [MW]}
      \\
      p_{t,g}^{\text{Tert}\,\text{DOWN}}
       & : \text{Tertiary down reserve ability of large-scale power generation $g$ at time $t$ [MW]}
\end{array}
$$

## Decision variables used only in `delta-kW-bid` (day-ahead scheduling)

$$
\begin{array}{ll}
      p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : \text{Tertiary up reserve ability of large-scale power generation $g$ at time $t$ ($\Delta\text{kW}$) [MW]}
      \\
      p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : \text{Tertiary down reserve ability of large-scale power generation $g$ at time $t$ ($\Delta\text{kW}$) [MW]}
\end{array}
$$

## Decision variables used only in `delta-kW-bid` (intra-day scheduling)

$$
\begin{array}{ll}
      p_{t,g}^{\text{id},\text{UP}}
       & : \text{Tertiary up-reserve energy (kWh) provided by large-scale power generation $g$ at time $t$ [MWh]}
      \\
      p_{t,g}^{\text{id},\text{DOWN}}
       & : \text{Tertiary down-reserve energy (kWh) provided by large-scale power generation $g$ at time $t$ [MWh]}
      \\
      u_{t,g}^{\text{id is UP}} \in \\{0,1\\}
       & : \text{Whether or not large-scale power generation $g$ provides tertiary up-reserve energy at time $t$ (binary, 1: up adjustment, 0: down adjustment)}
\end{array}
$$

## Decision variables for nuclear and thermal generation only

$$
\begin{array}{ll}
      u_{t,g} \in \\{0,1\\}
       & : \text{Operating state of nuclear and thermal power generation $g$ at time $t$ (binary, 1: running, 0: stopped)}
      \\
      su_{t,g} \in \\{0,1\\}
       & : \text{Whether nuclear and thermal power generation $g$ has been started or not at time $t$ (binary, 1: started, 0: not started)}
      \\
      sd_{t,g} \in \\{0,1\\}
       & : \text{Whether nuclear and thermal power generation $g$ has stopped or not at time $t$ (binary, 1: stopped, 0: not stopped)}
\end{array}
$$
