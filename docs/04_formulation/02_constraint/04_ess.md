# エネルギー貯蔵システム（ESS）に関する制約
揚水発電所等をイメージした大規模のエネルギー貯蔵システム（Energy Storage System: ESS）を考慮することができる。

- 最大発電能力・充電能力、最小発電能力・充電能力制約を考慮することができる。
  - 最大発電能力・充電能力制約には各能力低下状態を考慮できるように $P_{t,ess}^{\text{discharge}\,\text{des}}$ , $P_{t,ess}^{\text{charge}\,\text{des}}$ が追記されている（出力低下を設定することができるCSVファイル[「descent.csv」](../../05_csvfile/02_generation.md#出力低下)を参照）。
- 運転状態や蓄電量の許す限りにGF&LFC調整力や三次調整力を提供することができると想定している。
- 蓄電量の運用に関しては以下の2つの制約を考慮することができる。デフォルトでは境界条件制約のみ考慮する。
  - 境界条件制約: 最適化対象期間前時刻と終了時刻の蓄電量を基準値に固定する制約
  - 計画運用制約: CSVファイルで指定された時刻、蓄電量を満たすように決定変数を固定する制約

各添字、集合、定数、決定変数の定義は以下のページを参照。
- [添字と集合](../03_set_and_index.md)
- 定数
  1. [地域に関する定数](../04_parameter/01_area.md)
  2. [大規模発電機に関する定数](../04_parameter/02_generator.md)
  3. [再生可能エネルギーに関する定数](../04_parameter/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する定数](../04_parameter/04_ess.md)
  5. [連系線に関する定数](../04_parameter/05_tie.md)
  6. [計画種に依存する定数](../04_parameter/06_depend_on_scheduling_kind.md)
- 決定変数
  1. [地域に関する決定変数](../05_variable/01_area.md)
  2. [大規模発電機に関する決定変数](../05_variable/02_geneation.md)
  3. [再生可能エネルギーに関する決定変数](../05_variable/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する決定変数](../05_variable/04_ess.md)
  5. [連系線に関する決定変数](../05_variable/05_tie.md)


## エネルギー貯蔵システムの最大発電能力・充電能力制約

$$
\begin{align}
   p_{t,ess}^{\text{discharge}}
    & \leq \left( P_{ess}^{\text{discharge}\,\text{MAX}} - P_{t,ess}^{\text{discharge}\,\text{des}} \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{charge}}
    & \leq \left( P_{ess}^{\text{charge}\,\text{MAX}} - P_{t,ess}^{\text{charge}\,\text{des}} \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
## エネルギー貯蔵システムの最小発電能力・充電能力制約
$$
\begin{align}
   p_{t,ess}^{\text{discharge}}
    & \geq P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{charge}}
    & \geq P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
## エネルギー貯蔵システムの運転状況判定
$$
\begin{align}
   dchg_{t,ess} + chg_{t,ess}
    & \leq 1
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$

## エネルギー貯蔵システムのGF&LFC調整力確保可能量制約
$$
\begin{align}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq & \; P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess}
   \- p_{t,ess}^{\text{discharge}} \notag
   \\
        &  + p_{t,ess}^{\text{charge}}
   \- P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (3)
\\
  p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{charge}\,\text{MAX}} chg_{t,ess}
   \- p_{t,ess}^{\text{charge}} \notag
   \\
        &  + p_{t,ess}^{\text{discharge}}
   \- P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (4)
\end{align}
$$
## エネルギー貯蔵システムの調整力確保可能量制約
$$
\begin{align}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,p}^{\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
## エネルギー貯蔵システムの蓄電量運用制約
$$
\begin{align}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}}}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$
## エネルギー貯蔵システムの最大蓄電量制約
$$
\begin{align}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$
## エネルギー貯蔵システムの最小蓄電量制約
$$
\begin{align}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
\end{align}
$$
## エネルギー貯蔵システムの蓄電量境界条件制約
$$
\begin{align}
   e_{0,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
           \ \ \left( E_{0,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{0,ess}^{\text{INHE}}
           \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall ess \in ESS
    & \qquad (1)
\\
   e_{end,ess} + e_{end,ess}^{\text{short}} - e_{end,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
    & \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
| 機能名                        | デフォルト | 設定ファイル上での設定名 | Falseとしたときの上記式からの変更内容 |
| :---------------------------- | :--------- | :----------------------- | :------------------------------------ |
| ESSの蓄電量境界条件制約の考慮 | True       | set_e_ess_bc_constrs     | 上記式(1),(2)を考慮しない             |

## エネルギー貯蔵システムの蓄電量計画運用制約

$$
\begin{align}
   e_{t,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}                    \\
           \ \ \ \ \ \ \ \left( E_{t,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{t,ess}^{\text{INHE}}                                                   \\
           \ \ \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T^{\text{INHE}},
   \forall ess \in ESS
   & \qquad (1)
\\
   e_{t,ess} + e_{t,ess}^{\text{short}} - e_{t,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T,
   \forall ess \in ESS
   & \qquad (2)
\end{align}
$$
| 機能名                        | デフォルト | 設定ファイル上での設定名 | Falseとしたときの上記式からの変更内容 |
| :---------------------------- | :--------- | :----------------------- | :------------------------------------ |
| ESSの蓄電量計画運用制約の考慮 | False      | set_e_ess_plan_constrs   | 上記式(1),(2)を考慮しない             |

## エネルギー貯蔵システムの計画停止期間制約

$$
\begin{align}
   dchg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2)
\\
   chg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2)
\end{align}
$$
