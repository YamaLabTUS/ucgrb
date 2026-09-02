# Decision variables for tie line

Unless otherwise stated, all variables x are non-negative real numbers. $x \in R_{+}$ (non-negative real numbers)

$$
   \begin{array}{ll}
      p_{t,tie}^{\text{forward}}
       & : \text{Average power interchanged to forward direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{counter}}
       & :\text{Average power interchanged to counter direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
       & : \text{GF\\&LFC up-reserve interchanged to forward direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}}
       & : \text{GF\\&LFC up-reserve interchanged to counter direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
       & : \text{GF\\&LFC down-reserve interchanged to forward direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}}
       & :\text{GF\\&LFC down-reserve interchanged to counter direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
       & : \text{Tertiary up-reserve interchanged to forward direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{Tert}\,\text{UP, counter}}
       & : \text{Tertiary up-reserve interchanged to counter direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
       & : \text{Tertiary down-reserve interchanged to forward direction in tie line $tie$ at time $t$ [MW]}
      \\
      p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}}
       & : \text{Tertiary down-reserve interchanged to counter direction in tie line $tie$ at time $t$ [MW]}
      \\
      d_{t,tie} \in \\{0,1\\}
       & : \text{Power flow direction of tie line $tie$ at time $t$ (binary, 1: forward, 0: counter)}
      \\
      d_{t,tie}^{\text{GF\\&LFC}\,\text{UP}} \in \\{0,1\\}
       & : \text{Power flow direction of GF\\&LFC up-reserve of tie line $tie$ at time $t$ (binary, 1: forward, 0: counter)}
      \\
      d_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN}} \in \\{0,1\\}
       & : \text{Power flow direction of GF\\&LFC down-reserve of tie line $tie$ at time $t$ (binary, 1: forward, 0: counter)}
      \\
      d_{t,tie}^{\text{Tert}\,\text{UP}} \in \\{0,1\\}
       & : \text{Power flow direction of tertiary up-reserve of tie line $tie$ at time $t$ (binary, 1: forward, 0: counter)}
      \\
      d_{t,tie}^{\text{Tert}\,\text{DOWN}} \in \\{0,1\\}
       & : \text{Power flow direction of tertiary down-reserve of tie line $tie$ at time $t$ (binary, 1: forward, 0: counter)}
   \end{array}
$$
