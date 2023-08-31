# 大規模発電機に関する制約

水力、原子力、火力等の大規模発電機を考慮することができる。

- 最大出力、最小出力、N日毎の発電量上限制約を考慮することができる。
  - 最大出力制約には出力低下状態を考慮できるように $P_{t,g}^{\text{des}$が追記されている（出力低下を設定することができるCSVファイル[「descent.csv」](../../05_csvfile/02_generation.md#出力低下)を参照）。
- 原子力・火力の起動停止計画に関する制約として、必要最小運転時間制約と必要最小停止時間制約を考慮することができる。
- 原子力・火力の年間補修計画を反映することができ、補修期間中の発電機の停止を制約として加えることができる。
- 原子力のマストラン運用、つまり補修期間以外は常に起動中とする制約を考慮することができる。


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


## 大規模発電機の最大出力制約

$$
\begin{align}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & = \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & = \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2)
\end{align}
$$

## 大規模発電機の最小出力制約

$$
\begin{align}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & = P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & = P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2)
\end{align}
$$

## 大規模発電機の GF&LFC 調整力確保可能量制約

$$
\begin{align}
   p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (1)
\\
   p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2)
\end{align}
$$

## 大規模発電機のN日毎の発電量上限制約

$$
\begin{align}
   \sum_{i = t}^{t + 24N - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + 24N \times m \; (m = 0,1,2\dots), \forall g \in G
\end{align}
$$

## 原子力・火力発電機の起動停止判定

$$
\begin{align}
   su_{t,g} - sd_{t,g}
    & = u_{t,g} - u_{t-1,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (1)
\\
   su_{t,g} + sd_{t,g}
    & \leq 1
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2)
\end{align}
$$

|変数                  |状態1|状態2|状態3|状態4|備考    |
|---------------------|:--:|:--:|:--:|:--:|:-----:|
|$u_{t,g}$            |1   |1   |0   |0   |       |
|$u_{t-1,g}$          |1   |0   |1   |0   |       |
|$u_{t,g} - u_{t-1,g}$|0   |1   |-1  |0   |式(1)右辺|
|$su_{t,g} - sd_{t,g}$|0   |1   |-1  |0   |式(1)左辺|
|$su_{t,g}$           |0   |1   |0   |0   |式(2)より $sd_{t,g}$ と同時に1となることはない|
|$sd_{t,g}$           |0   |0   |1   |0   |式(2)より $su_{t,g}$ と同時に1となることはない|

## 原子力・火力発電機の必要最小運転時間制約

$$
\begin{align}
   \sum_{i=t+1-ReqRunTime_{g}}^{t} su_{i,g}
    & \leq u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
\end{align}
$$

## 原子力・火力発電機の必要最小停止時間制約

$$
\begin{align}
   \sum_{i=t+1-ReqStopTime_{g}}^{t} sd_{i,g}
    & \leq 1 - u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
\end{align}
$$

## 原子力・火力発電機の計画停止期間制約

$$
\begin{align}
   u_{t,g}
    & = 0
    & \forall t \in T_{g}^{\text{Planned Outage}} , \forall g \in G_{N\\&T}
\end{align}
$$

## 原子力のマストラン運用制約

$$
\begin{align}
   u_{t,g}
    & =1
    & \forall t \in \left( T^{\text{INHE,A}} \cup T \right) \setminus T_{g}^{\text{Planned Outage}}, \forall g \in G_{NUCL}
\end{align}
$$

| 機能名                                 | デフォルト | 設定ファイル上での設定名               | Falseとしたときの上記式からの変更内容 |
| :------------------------------------- | :--------- | :------------------------------------- | :------------------------------------ |
| 原子力発電機のマストラン運転制約の考慮 | True       | set_must_run_operation_of_nucl_constrs | 上記式を考慮しない                    |
