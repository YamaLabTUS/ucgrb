# Parameters for energy storage system

> **Note**: The items on this page such as ΔkW / kWh / $p^{id}$ are used only in the ΔkW-value version (`formulation_type: "delta-kW-bid"`). They are not referenced in `delta-kW-no-market` (default).

## Parameters common to both modes

Parameters used in both `delta-kW-no-market` and `delta-kW-bid`, such as stored-energy penalties, discharge/charge capacity, efficiency, and energy storage capacity.

$$
\begin{array}{ll}
      C_{ess}^{\text{short}}
       & : \text{Coefficient of penalty term for energy shortage against planned stored energy of energy storage system $ess$ [kYen/MWh]}
      \\
      C_{ess}^{\text{surplus}}
       & : \text{Coefficient of penalty term for energy surplus against planned stored energy of energy storage system $ess$ [kYen/MWh]}
      \\
      P_{ess}^{\text{discharge}\,\text{MAX}}
       & : \text{Maximum output of energy storage system $ess$ [MW]}
      \\
      P_{ess}^{\text{charge}\,\text{MAX}}
       & : \text{Maximum charging capacity of energy storage system $ess$ [MW]}
      \\
      P_{t,ess}^{\text{discharge}\,\text{des}}
       & : \text{Temporary output reduction of energy storage system $ess$ at time $t$ [MW]}
      \\
      P_{t,ess}^{\text{charge}\,\text{des}}
       & : \text{Temporary charging capacity reduction of energy storage system $ess$ at time $t$ [MW]}
      \\
      P_{ess}^{\text{discharge}\,\text{MIN}}
       & : \text{Minimum output of energy storage system $ess$ [MW]}
      \\
      P_{ess}^{\text{charge}\,\text{MIN}}
       & : \text{Minimum charging capacity of energy storage system $ess$ [MW]}
      \\
      R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}
       & : \text{Reserve availability percentage of energy storage system $ess$ [\\%]}
      \\
      \eta_{ess}
       & : \text{Overall generating efficiency of energy storage system $ess$ [\\%]}
      \\
      \gamma_{ess}
       & : \text{Overall charging efficiency of energy storage system $ess$ [\\%]}
      \\
      E_{ess}^{\text{CAP}}
       & : \text{Energy storage capacity of energy storage system $ess$ [MWh]}
      \\
      ER_{ess}^{\text{MAX}}
       & : \text{Maximum energy storage rate of energy storage capacity of energy storage system $ess$ [\\%]}
      \\
      ER_{ess}^{\text{MIN}}
       & : \text{Minimum energy storage rate of energy storage capacity of energy storage system $ess$ [\\%]}
      \\
      ER_{ess}^{\text{base}}
       & : \text{Boundary condition of stored energy rate of energy storage system $ess$ [\\%]}
      \\
      ER_{t,ess}^{\text{plan}}
       & : \text{Planned stored energy rate of energy storage system $ess$ at time $t$ [\\%]}
      \\
      M_{ess}
       & : \text{Per-unit inertia constant of energy storage system $ess$ [MW$\cdot$s/MVA]}
      \\
      E_{t,ess}^{\text{INHE}}
       & : \text{Stored energy of energy storage system $ess$ at time $t$ determined in the previous optimization [MWh]}
\end{array}
$$

## Parameters used only in `delta-kW-bid` (day-ahead scheduling)

Unit procurement cost of tertiary reserve (ΔkW, kW value).

$$
\begin{array}{ll}
      C_{ess}^{\Delta\text{kW}\,\text{UP}}
       & : \text{Unit procurement cost of up tertiary reserve ($\Delta$kW) of energy storage system $ess$ [kYen/MW]}
      \\
      C_{ess}^{\Delta\text{kW}\,\text{DOWN}}
       & : \text{Unit procurement cost of down tertiary reserve ($\Delta$kW) of energy storage system $ess$ [kYen/MW]}
\end{array}
$$

## Parameters used only in `delta-kW-bid` (intra-day scheduling)

Unit procurement cost of tertiary reserve energy (kWh), and the average discharge/charge power and tertiary reserve (ΔkW) inherited from day-ahead scheduling.

$$
\begin{array}{ll}
      C_{ess}^{\text{kWh}\,\text{UP}}
       & : \text{Unit procurement cost of up tertiary reserve energy (kWh) of energy storage system $ess$ [kYen/MWh]}
      \\
      C_{ess}^{\text{kWh}\,\text{DOWN}}
       & : \text{Unit procurement cost of down tertiary reserve energy (kWh) of energy storage system $ess$ [kYen/MWh]}
      \\
      P_{t,ess}^{\text{da},\text{discharge}}
       & : \text{Average output of energy storage system $ess$ at time $t$ determined in day-ahead scheduling [MW]}
      \\
      P_{t,ess}^{\text{da},\text{charge}}
       & : \text{Average charging power of energy storage system $ess$ at time $t$ determined in day-ahead scheduling [MW]}
      \\
      P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : \text{Up tertiary reserve ($\Delta$kW) of energy storage system $ess$ at time $t$ determined in day-ahead scheduling [MW]}
      \\
      P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : \text{Down tertiary reserve ($\Delta$kW) of energy storage system $ess$ at time $t$ determined in day-ahead scheduling [MW]}
\end{array}
$$
