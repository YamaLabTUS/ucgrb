# 目的関数

最適化の目的関数は最適化対象期間の全地域の総コスト最小化である。考慮可能なコストは以下の通りである。
- 大規模発電機の可変費、固定費、起動費 $Cost_{g,t}$
- 各地域の供給不足処理費 $Cost_{a,t}^{\text{short}}$
- 各地域の供給余剰処理費 $Cost_{a,t}^{\text{surplus}}$
- 各地域の三次調整力不足処理費 $Cost_{a,t}^{\text{Tert,short}}$
- 各地域の再生可能エネルギー出力抑制処理費 $Cost_{a,t,\text{RE}}^{\text{suppr}}$
  - 現在の日本では、出力抑制に対する対価を支払うルールは存在しない。
- エネルギー貯蔵装置（ESS）の蓄電量計画逸脱ペナルティ $Penalty_{ess,t}$
- 連系線の使用ペナルティ $Penalty_{tie,t}$
  - ループ型の連系線によるエネルギー循環の発生を避けるためのペナルティー項。実際に使用料金を使用者が払うことはない。

各添字、集合、定数、決定変数の定義は以下のページを参照。
- [添字と集合](03_set_and_index.md)
- 定数
  1. [地域に関する定数](04_parameter/01_area.md)
  2. [大規模発電機に関する定数](04_parameter/02_generator.md)
  3. [再生可能エネルギーに関する定数](04_parameter/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する定数](04_parameter/04_ess.md)
  5. [連系線に関する定数](04_parameter/05_tie.md)
  6. [計画種に依存する定数](04_parameter/06_depend_on_scheduling_kind.md)
- 決定変数
  1. [地域に関する決定変数](05_variable/01_area.md)
  2. [大規模発電機に関する決定変数](05_variable/02_geneation.md)
  3. [再生可能エネルギーに関する決定変数](05_variable/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する決定変数](05_variable/04_ess.md)
  5. [連系線に関する決定変数](05_variable/05_tie.md)

$$
\begin{align}
         \min \ F = \sum_{t \in T} & \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) \right.
                  \\
                  & \left.  + \sum_{ess \in \textit{ESS}} Penalty_{ess,t}  +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} \right]
\end{align}
$$

--------------

$$
\begin{align}
    Cost_{g,t} = &
    C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g}
    + C_{g}^{\text{startup}}\ su_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
    Cost_{a,t}^{\text{short}} = &
    C_{a}^{\text{short}}\ p_{t,a}^{\text{short}}
    & \forall t \in T, \forall a \in A
    & \qquad (2)
\\
    Cost_{a,t}^{\text{surplus}} = &
    C_{a}^{\text{surplus}}\ p_{t,a}^{\text{surplus}}
    & \forall t \in T, \forall a \in A
    & \qquad (3)
\\
    Cost_{a,t}^{\text{Tert,short}} = &
    C_{a}^{\text{tert,short}} \left( p_{t,a}^{\text{Tert}\,\text{UP, short}} +
    p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \right)
    & \forall t \in T, \forall a \in A
    & \qquad (4)
\\
    Cost_{a,t,\text{RE}}^{\text{suppr}} = &
    C_{a,\text{PV}}^{\text{suppr}} p_{t,a,\text{PV}}^{\text{suppr}} +
    C_{a,\text{WF}}^{\text{suppr}} p_{t,a,\text{WF}}^{\text{suppr}}
    & \forall t \in T, \forall a \in A
    & \qquad (5)
\end{align}
$$

--------------

$$
\begin{align}
    Penalty_{ess,t} = &
    C_{ess}^{\text{short}}\ e_{t,ess}^{\text{short}} + C_{ess}^{\text{surplus}}\ e_{t,ess}^{\text{surplus}}
    & \forall t \in T, \forall ess \in \textit{ESS}
    & \qquad (6)
    \\
    Penalty_{tie,t} = &
    C_{tie}^{\text{penalty}} \left( p_{t,tie}^{\text{forward}} + p_{t,tie}^{\text{counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
    + p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
    + p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
    + p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
    + p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right)
    & \forall t \in T, \forall tie \in \textit{TIE}
    & \qquad (7)
\end{align}
$$
