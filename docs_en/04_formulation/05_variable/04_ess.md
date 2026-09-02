# Decision variables for energy storage systems (ESS)

> **Note**: The items on this page such as ΔkW / kWh / p^id are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

Unless otherwise stated, all decision variables x are non-negative real numbers. $x \in R_{+}$ (non-negative real numbers)

## Decision variables common to both modes

$$
\begin{array}{ll}
      p_{t,ess}^{\text{discharge}}
       & : \text{Average power output of energy storage systems $ess$ at time $t$ [MW]}
      \\
      p_{t,ess}^{\text{charge}}
       & : \text{Average charging output of energy storage systems $ess$ at time $t$ [MW]}
      \\
      p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
       & : \text{GF\&LFC up-reserve power supplied by energy storage systems $ess$ at time $t$ [MW]}
      \\
      p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
       & : \text{GF\&LFC down-reserve power supplied by energy storage systems $ess$ at time $t$ [MW]}
      \\
      e_{t,ess}
       & : \text{Stored energy of energy storage systems $ess$ at time $t$ [MWh]}
      \\
      e_{t,ess}^{\text{short}}
       & : \text{Shortage in planned stored energy of energy storage systems $ess$ at time $t$ [MWh]}
      \\
      e_{t,ess}^{\text{surplus}}
       & : \text{Surplus in planned stored energy of energy storage systems $ess$ at time $t$ [MWh]}
      \\
      dchg_{t,ess} \in \\{0,1\\}
       & : \text{Power generation status of energy storage systems $ess$ at time $t$ (binary, 1: running, 0: stopped)}
      \\
      chg_{t,ess} \in \\{0,1\\}
       & : \text{Power charging status of energy storage systems $ess$ at time $t$ (binary, 1: running, 0: stopped)}
\end{array}
$$

## Decision variables used only in `delta-kW-no-market`

$$
\begin{array}{ll}
      p_{t,ess}^{\text{Tert}\,\text{UP}}
       & : \text{Tertiary up-reserve power supplied by energy storage systems $ess$ at time $t$ [MW]}
      \\
      p_{t,ess}^{\text{Tert}\,\text{DOWN}}
       & : \text{Tertiary down-reserve power supplied by energy storage systems $ess$ at time $t$ [MW]}
\end{array}
$$

## Decision variables used only in `delta-kW-bid` (day-ahead scheduling)

$$
\begin{array}{ll}
      p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : \text{Tertiary up-reserve power ($\Delta\text{kW}$) secured by energy storage systems $ess$ at time $t$ [MW]}
      \\
      p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : \text{Tertiary down-reserve power ($\Delta\text{kW}$) secured by energy storage systems $ess$ at time $t$ [MW]}
\end{array}
$$

## Decision variables used only in `delta-kW-bid` (intra-day scheduling)

$$
\begin{array}{ll}
      p_{t,ess}^{\text{id},\text{UP}}
       & : \text{Tertiary up-reserve energy (kWh) provided by energy storage systems $ess$ at time $t$ [MWh]}
      \\
      p_{t,ess}^{\text{id},\text{DOWN}}
       & : \text{Tertiary down-reserve energy (kWh) provided by energy storage systems $ess$ at time $t$ [MWh]}
      \\
      u_{t,ess}^{\text{id is UP}} \in \\{0,1\\}
       & : \text{Whether energy storage systems $ess$ provide tertiary up-reserve energy at time $t$ (binary, 1: up-reserve, 0: down-reserve)}
\end{array}
$$
