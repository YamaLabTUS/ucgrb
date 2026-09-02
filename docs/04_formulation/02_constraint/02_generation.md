# 大規模発電機に関する制約

> **[`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type) による条件分岐**
> 本ページの ΔkW（前日計画）／kWh（当日計画）に関する項目は、ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ有効。`delta-kW-no-market`（既定）では三次調整力を単一の予備力量として扱い、これらの項目は無効。

水力、原子力、火力等の大規模発電機を考慮することができる。

- 最大出力、最小出力、N 日毎の発電量上限制約を考慮することができる。
  - 最大出力制約には出力低下状態を考慮できるように $P_{t,g}^{\text{des}}$ が追記されている（出力低下を設定することができる CSV ファイル[「descent.csv」](../../05_csvfile/02_generation.md#出力低下)を参照）。
- 原子力・火力の起動停止計画に関する制約として、必要最小運転時間制約と必要最小停止時間制約を考慮することができる。
- 原子力・火力の年間補修計画を反映することができ、補修期間中の発電機の停止を制約として加えることができる。
- 原子力のマストラン運用、つまり補修期間以外は常に起動中とする制約を考慮することができる。

各添字、集合、定数、決定変数の定義は以下のページを参照。

- [添字と集合](../03_set_and_index.md)
- 定数
  1. [地域に関する定数](../04_parameter/01_area.md)
  2. [大規模発電機に関する定数](../04_parameter/02_generation.md)
  3. [再生可能エネルギーに関する定数](../04_parameter/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する定数](../04_parameter/04_ess.md)
  5. [連系線に関する定数](../04_parameter/05_tie.md)
  6. [計画種に依存する定数](../04_parameter/06_depend_on_scheduling_kind.md)
- 決定変数
  1. [地域に関する決定変数](../05_variable/01_area.md)
  2. [大規模発電機に関する決定変数](../05_variable/02_generation.md)
  3. [再生可能エネルギーに関する決定変数](../05_variable/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する決定変数](../05_variable/04_ess.md)
  5. [連系線に関する決定変数](../05_variable/05_tie.md)

## 当日計画における発電量平均値（`delta-kW-bid` のみ）

前日計画からの引き継ぎとして、以下の前提条件がある

$$
\begin{aligned}
    P_{t,g}^{\text{da}}&=p_{t,g}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}1)
\end{aligned}
$$

その上で、当日計画の発電量平均値は以下の値となる。

$$
\begin{aligned}
    p_{t,g} &= P_{t,g}^{\text{da}} + p_{t,g}^{\text{id},\text{UP}} - p_{t,g}^{\text{id},\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}2)
    \\
    p_{t,g}^{\text{id},\text{UP}} &\leq u_{t,g}^{\text{id is UP}} P_{g}^{\text{MAX}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}3)
    \\
    p_{t,g}^{\text{id},\text{DOWN}} &\leq \left( 1 - u_{t,g}^{\text{id is UP}} \right) P_{g}^{\text{MAX}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}0\text{-}4)
\end{aligned}
$$

ここで $u_{t,g}^{\text{id is UP}}$ は調整方向を表すバイナリ変数（1: 上げ、0: 下げ）である。式 (2-2-0-3)・(2-2-0-4) は上げと下げの同時提供を禁止する **方向選択制約** であり、右辺の $P_{g}^{\text{MAX}}$ は調整電力量の実際の上限ではなく、方向選択のための十分大きな定数（big-M）として用いている。上げ方向のとき $u_{t,g}^{\text{id is UP}} = 1$ となり下げ調整量 $p_{t,g}^{\text{id},\text{DOWN}}$ は 0 に固定される（下げ方向はその逆）。調整電力量の実際の上限は、前日計画で確保した三次調整力 $P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}}$ により、最大出力制約の当日計画の式で別途課される。

## 1. 大規模発電機の最大出力制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,g}^{\text{Tert}\,\text{UP}}$ として扱う。

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}1)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}2)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

三次調整力を前日計画では ΔkW（ $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ ）、当日計画では実運用された電力量 kWh（ $p_{t,g}^{\text{id},\text{UP}}$ ）として扱う。

#### 前日計画

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}3)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}4)
\end{aligned}
$$

#### 当日計画

前日計画からの引き継ぎとして、以下の前提条件がある

$$
\begin{aligned}
    P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}&=p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}1\text{-}5)
\end{aligned}
$$

その上で、本制約式は以下の通りとなる。当日計画では、 $p_{t,g}^{\text{id},\text{UP}}$ が既に $p_{t,g}$ に含まれているため（式(2-2-0-2)参照）、二重カウントを避けるために $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ を 0 として扱う。

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}1\text{-}6)
\\
   p_{t,g} + p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq \left( P_{g}^{\text{MAX}} - P_{t,g}^{\text{des}} \right) U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}1\text{-}7)
\\
    p_{t,g}^{\text{id},\text{UP}} \leq P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}1\text{-}8)
\end{aligned}
$$

## 2. 大規模発電機の最小出力制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,g}^{\text{Tert}\,\text{DOWN}}$ として扱う。

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}1)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}2)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

三次調整力を前日計画では ΔkW（ $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ ）、当日計画では実運用された電力量 kWh（ $p_{t,g}^{\text{id},\text{DOWN}}$ ）として扱う。

#### 前日計画

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}3)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}4)
\end{aligned}
$$

#### 当日計画

前日計画からの引き継ぎとして、以下の前提条件がある

$$
\begin{aligned}
    P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}&=p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}2\text{-}5)
\end{aligned}
$$

その上で、本制約式は以下の通りとなる。当日計画では、 $p_{t,g}^{\text{id},\text{DOWN}}$ が既に $p_{t,g}$ に含まれているため（式(2-2-0-2)参照）、二重カウントを避けるために $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ を 0 として扱う。

$$
\begin{aligned}
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}2\text{-}6)
\\
   p_{t,g} - p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \geq P_{g}^{\text{MIN}} U_{t,g}
    & \forall t \in T, \forall g \in G_{HYDRO}
    & \qquad (2\text{-}2\text{-}2\text{-}7)
\\
    p_{t,g}^{\text{id},\text{DOWN}} \leq P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}2\text{-}8)
\end{aligned}
$$

## 3. 大規模発電機の GF&LFC 調整力確保可能量制約

$$
\begin{aligned}
   p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}3\text{-}1)
\\
   p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{g}^{\text{MAX}} \frac{R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
    & \forall t \in T, \forall g \in G
    & \qquad (2\text{-}2\text{-}3\text{-}2)
\end{aligned}
$$

## 4. 大規模発電機の N 日毎の発電量上限制約

$$
\begin{aligned}
   \sum_{i = t}^{t + 24N - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + 24N \times m \; (m = 0,1,2\dots), \forall g \in G
    & \qquad (2\text{-}2\text{-}4\text{-}1)
\end{aligned}
$$

## 5. 原子力・火力発電機の起動停止判定

$$
\begin{aligned}
   su_{t,g} - sd_{t,g}
    & = u_{t,g} - u_{t-1,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}5\text{-}1)
\\
   su_{t,g} + sd_{t,g}
    & \leq 1
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}5\text{-}2)
\end{aligned}
$$

| 変数                  | 状態 1 | 状態 2 | 状態 3 | 状態 4 |                           備考                            |
| --------------------- | :----: | :----: | :----: | :----: | :-------------------------------------------------------: |
| $u_{t,g}$             |   1    |   1    |   0    |   0    |                                                           |
| $u_{t-1,g}$           |   1    |   0    |   1    |   0    |                                                           |
| $u_{t,g} - u_{t-1,g}$ |   0    |   1    |   -1   |   0    |                    式(2-2-5-1)右辺                        |
| $su_{t,g} - sd_{t,g}$ |   0    |   1    |   -1   |   0    |                    式(2-2-5-1)左辺                        |
| $su_{t,g}$            |   0    |   1    |   0    |   0    | 式(2-2-5-2)より $sd_{t,g}$ と同時に 1 となることはない    |
| $sd_{t,g}$            |   0    |   0    |   1    |   0    | 式(2-2-5-2)より $su_{t,g}$ と同時に 1 となることはない    |

| 機能名                                                   | デフォルト | 設定ファイル上での設定名 | True としたときの上記式からの変更内容                     |
| :------------------------------------------------------- | :--------- | :----------------------- | :-------------------------------------------------------- |
| 原子力・火力発電機の起動停止に関するバイナリ変数の連続化 | False      | make_u_continuous        | バイナリ変数 $u_{t,g}, su_{t,g}, sd_{t,g}$ を連続変数にする |

## 6. 原子力・火力発電機の必要最小運転時間制約

$$
\begin{aligned}
   \sum_{i=t+1-MinUpTime_{g}}^{t} su_{i,g}
    & \leq u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}6\text{-}1)
\end{aligned}
$$

## 7. 原子力・火力発電機の必要最小停止時間制約

$$
\begin{aligned}
   \sum_{i=t+1-MinDownTime_{g}}^{t} sd_{i,g}
    & \leq 1 - u_{t,g}
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}7\text{-}1)
\end{aligned}
$$

## 8. 原子力・火力発電機の出力変化速度制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,g}^{\text{Tert}\,\text{UP}}$ / $p_{t,g}^{\text{Tert}\,\text{DOWN}}$ として扱う。

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}1)
\\
   p_{t,g} - p_{t,g}^{\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}2)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

三次調整力を前日計画では ΔkW、当日計画では実運用された電力量 kWh として扱う。

#### 前日計画

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}3)
\\
   p_{t,g} - p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}4)
\end{aligned}
$$

#### 当日計画

当日計画では、 $p_{t,g}^{\text{id},\text{UP}}$ と $p_{t,g}^{\text{id},\text{DOWN}}$ が既に $p_{t,g}$ に含まれているため（式(2-2-0-2)参照）、二重カウントを避けるために $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ と $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ を 0 として扱う。

$$
\begin{aligned}
   p_{t,g} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}5)
\\
   p_{t,g} + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}8\text{-}6)
\end{aligned}
$$

| 機能名                                         | デフォルト | 設定ファイル上での設定名 | False としたときの上記式からの変更内容 |
| :--------------------------------------------- | :--------- | :----------------------- | :------------------------------------- |
| 原子力・火力発電機の出力変化速度制約の考慮 | True       | set_ramp_constr          | 上記式を考慮しない                     |

## 9. 原子力・火力発電機の計画停止期間制約

$$
\begin{aligned}
   u_{t,g}
    & = 0
    & \forall t \in T_{g}^{\text{Planned Outage}} , \forall g \in G_{N\\&T}
    & \qquad (2\text{-}2\text{-}9\text{-}1)
\end{aligned}
$$

## 10. 原子力のマストラン運用制約

$$
\begin{aligned}
   u_{t,g}
    & =1
    & \forall t \in \left( T^{\text{INHE,A}} \cup T \right) \setminus T_{g}^{\text{Planned Outage}}, \forall g \in G_{NUCL}
    & \qquad (2\text{-}2\text{-}10\text{-}1)
\end{aligned}
$$

| 機能名                                 | デフォルト | 設定ファイル上での設定名               | False としたときの上記式からの変更内容 |
| :------------------------------------- | :--------- | :------------------------------------- | :------------------------------------- |
| 原子力発電機のマストラン運転制約の考慮 | True       | set_must_run_operation_of_nucl_constrs | 上記式を考慮しない                     |
