# 目的関数

> **[`formulation_type`](../06_config/03_unit_commitment.md#formulation_type) による条件分岐**
> 本ページの ΔkW（前日計画）／kWh（当日計画）に関する項目は、ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ有効。`delta-kW-no-market`（既定）では三次調整力を単一の予備力量として扱い、これらの項目は無効。

最適化の目的関数は最適化対象期間の全地域の総社会調達コスト最小化である。考慮可能なコストは以下の通りである。

- 大規模発電機の可変費、無負荷費、起動費、 調整力調達費 $Cost_{g,t}$
  - 調整力調達費は前日計画の場合は調整力（ $\Delta\text{kW}$ ）、当日計画では実際に運用された調整電力量（ $\text{kWh}$ ）に各価格単価を乗ずることで得られる
- 各地域の供給不足処理費 $Cost_{a,t}^{\text{short}}$
- 各地域の供給余剰処理費 $Cost_{a,t}^{\text{surplus}}$
- 各地域の三次調整力不足処理費 $Cost_{a,t}^{\text{Tert,short}}$
- 各地域の再生可能エネルギー出力抑制処理費 $Cost_{a,t,\text{RE}}^{\text{suppr}}$
  - 現在の日本では、出力抑制に対する対価を支払うルールは存在しない。そのような設定をする場合には、 $Cost_{a,t,\text{RE}}^{\text{suppr}}=0$ とすればよい。
- エネルギー貯蔵装置（ESS）の調整力調達費 $Cost_{ess,t}$
- エネルギー貯蔵装置（ESS）の蓄電量計画逸脱ペナルティ $Penalty_{ess,t}$
- 連系線の使用ペナルティ $Penalty_{tie,t}$
  - ループ型の連系線によるエネルギー循環の発生を避けるためのペナルティー項。実際に使用料金を使用者が払うことはない。

各添字、集合、定数、決定変数の定義は以下のページを参照。

- [添字と集合](03_set_and_index.md)
- 定数
  1. [地域に関する定数](04_parameter/01_area.md)
  2. [大規模発電機に関する定数](04_parameter/02_generation.md)
  3. [再生可能エネルギーに関する定数](04_parameter/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する定数](04_parameter/04_ess.md)
  5. [連系線に関する定数](04_parameter/05_tie.md)
  6. [計画種に依存する定数](04_parameter/06_depend_on_scheduling_kind.md)
- 決定変数
  1. [地域に関する決定変数](05_variable/01_area.md)
  2. [大規模発電機に関する決定変数](05_variable/02_generation.md)
  3. [再生可能エネルギーに関する決定変数](05_variable/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する決定変数](05_variable/04_ess.md)
  5. [連系線に関する決定変数](05_variable/05_tie.md)

## 全体の目的関数（両モード共通）

総コストは各地域・各設備の費用項の総和として表される。費用項のうち、大規模発電機の費用 $Cost_{g,t}$ と ESS の費用 $Cost_{ess,t}$ は `formulation_type` により定義が変わる（後述）。

$$
\begin{aligned}
         \min \ F = \sum_{t \in T} & \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) \right.
                  \notag \\
                  & \left.  + \sum_{ess \in \textit{ESS}} \left( Cost_{ess,t}+ Penalty_{ess,t} \right) +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} \right]
    & \qquad (1\text{-}1)
\end{aligned}
$$

---

## 大規模発電機の費用 $Cost_{g,t}$

### `formulation_type: "delta-kW-no-market"` の場合

（既定）可変費・無負荷費・起動費の和。三次調整力の調達費は計上しない。

$$
Cost_{g,t} = C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g}
\qquad \forall t \in T,\ \forall g \in G_{N\\&T} \qquad (1\text{-}2)
$$

### `formulation_type: "delta-kW-bid"` の場合

上記に加え、三次調整力の調達費を計上する。前日計画は調整力 ΔkW（kW価値、単価 $C^{\Delta\text{kW}}$ ）、当日計画は実運用された電力量 kWh（単価 $C^{\text{kWh}}$ ）で評価する。当日計画では $p^{\text{id}}$ が既に $p$ に含まれるため、可変費は前日計画値 $P^{\text{da}}$ に対して計上し二重カウントを避ける。

$$
Cost_{g,t} =
\begin{cases}
C_{g}^{\text{coef}}\ p_{t,g} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g} + C_{g}^{\Delta\text{kW}\,\text{UP}}\ p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} + C_{g}^{\Delta\text{kW}\,\text{DOWN}}\ p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} & (\text{前日計画}) \\
C_{g}^{\text{coef}}\ P_{t,g}^{\text{da}} + C_{g}^{\text{intc}}\ u_{t,g} + C_{g}^{\text{startup}}\ su_{t,g} + C_{g}^{\text{kWh}\,\text{UP}}\ p_{t,g}^{\text{id}\,\text{UP}} + C_{g}^{\text{kWh}\,\text{DOWN}}\ p_{t,g}^{\text{id}\,\text{DOWN}} & (\text{当日計画})
\end{cases}
\qquad \forall t \in T,\ \forall g \in G_{N\\&T} \qquad (1\text{-}2')
$$

## 各地域の処理費（両モード共通）

供給不足・供給余剰・三次調整力不足・再エネ出力抑制の各処理費。`delta-kW-no-market` / `delta-kW-bid` で同一。

**供給不足処理費**

$$
Cost_{a,t}^{\text{short}} = C_{a}^{\text{short}}\ p_{t,a}^{\text{short}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}3)
$$

**供給余剰処理費**

$$
Cost_{a,t}^{\text{surplus}} = C_{a}^{\text{surplus}}\ p_{t,a}^{\text{surplus}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}4)
$$

**三次調整力不足処理費**

$$
Cost_{a,t}^{\text{Tert,short}} = C_{a}^{\text{tert,short}} \left( p_{t,a}^{\text{Tert}\,\text{UP, short}} + p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \right)
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}5)
$$

**再エネ出力抑制処理費**

$$
Cost_{a,t,\text{RE}}^{\text{suppr}} = C_{a,\text{PV}}^{\text{suppr}}\ p_{t,a,\text{PV}}^{\text{suppr}} + C_{a,\text{WF}}^{\text{suppr}}\ p_{t,a,\text{WF}}^{\text{suppr}}
\qquad \forall t \in T,\ \forall a \in A \qquad (1\text{-}6)
$$

## ESS の費用 $Cost_{ess,t}$

### `formulation_type: "delta-kW-no-market"` の場合

（既定）ESS の三次調整力調達費は計上しない（ $Cost_{ess,t} = 0$ ）。

### `formulation_type: "delta-kW-bid"` の場合

発電機と同様に、前日計画は ΔkW、当日計画は kWh を単価として三次調整力の調達費を計上する。

$$
Cost_{ess,t} =
\begin{cases}
C_{ess}^{\Delta\text{kW}\,\text{UP}}\ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} + C_{ess}^{\Delta\text{kW}\,\text{DOWN}}\ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} & (\text{前日計画}) \\
C_{ess}^{\text{kWh}\,\text{UP}}\ p_{t,ess}^{\text{id}\,\text{UP}} + C_{ess}^{\text{kWh}\,\text{DOWN}}\ p_{t,ess}^{\text{id}\,\text{DOWN}} & (\text{当日計画})
\end{cases}
\qquad \forall t \in T,\ \forall ess \in \textit{ESS} \qquad (1\text{-}7)
$$

---

## ペナルティ項（両モード共通）

ESS の蓄電量計画逸脱ペナルティ、連系線の使用ペナルティ。`delta-kW-no-market` / `delta-kW-bid` で同一。

$$
\begin{aligned}
    Penalty_{ess,t} = &
    C_{ess}^{\text{short}}\ e_{t,ess}^{\text{short}} + C_{ess}^{\text{surplus}}\ e_{t,ess}^{\text{surplus}}
    & \forall t \in T, \forall ess \in \textit{ESS}
    & \qquad (1\text{-}8)
    \\
    Penalty_{tie,t} = &
    C_{tie}^{\text{penalty}} \left( p_{t,tie}^{\text{forward}} + p_{t,tie}^{\text{counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
    \+ p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{GF\\&LFC}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
    \+ p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{UP, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
    \+ p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right)
    \\
    & + C_{tie}^{\text{Tert}\,\text{DOWN, penalty}}
    \left( p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
    \+ p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right)
    & \forall t \in T, \forall tie \in \textit{TIE}
    & \qquad (1\text{-}9)
\end{aligned}
$$
