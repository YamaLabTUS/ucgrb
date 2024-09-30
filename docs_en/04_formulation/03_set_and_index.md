# Sets and indies

$$
\begin{array}{ll}
      t \in T=\{ 1, 2, ... , end-1, end \}
       & : \text{Optimization target period}
      \\
      t \in T_{g}^{\text{Planned Outage}} \\;\\;\\;\\; \forall g \in G_{N\\&T}
       & : \text{Planned outage period for nuclear and thermal generation $g$ }
      \\
      t \in T_{ess}^{\text{PLAN}}
       & : \text{Time specified for energy storage system $ess$ to plan energy storage operation}
       \\
       & \\; \\; \text{(used when considering energy scheduling constraint at designated times)}
      \\
      t \in T_{ess}^{\text{Planned Outage}}
       & : \text{Planned outage period for energy storage system $ess$}
      \\
      t \in T^{\text{INHE,A}}
       & : \text{Variable inheritance period from previous optimization}
       \\
       & \\; \\; \text{ for output of large-scale power generations and storage capacity of ESS}
      \\
      t \in T^{\text{INHE,A}}
       & : \text{Variable inheritance period from previous optimization}
       \\
       & \\; \\; \text{ for binary variables related to the operating conditions of nuclear and thermal power generation}
      \\
      a \in A
       & : \text{Areas}
      \\
      g \in G=\{ G_{N\\&T} \cup G_{HYDRO} \}
       & : \text{Large-scale power generations}
      \\
      g \in G_{N\\&T}
       & : \text{Nuclear and thermal generations}
      \\
      g \in G_{NUCL}
       & : \text{Nuclear generations}
      \\
      g \in G_{HYDRO}
       & : \text{Hydro generations}
      \\
      g \in G_{a}
       & : \text{Large-scale power generations in area $a$}
      \\
      g \in G_{N\\&T,a}
       & : \text{Nuclear and thermal generations in area $a$}
      \\
      g \in G_{HYDRO,a}
       & : \text{Hydro generations in area $a$}
      \\
      ess \in ESS
       & : \text{Energy storage systems}
      \\
      ess \in ESS_{a}
       & : \text{Energy storage systems in area $a$}
      \\
      tie \in TIE
       & : \text{Tie lines}
      \\
      tie \in TIE_{\text{to}=a}
       & : \text{Tie lines that are connected in forward direction to area $a$ }
      \\
      tie \in TIE_{\text{from}=a}
       & : \text{Tie lines that are connected in counter direction to area $a$ }
\end{array}
$$
