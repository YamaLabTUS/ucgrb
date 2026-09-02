# エネルギー貯蔵システム（ESS）に関する制約

> **[`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type) による条件分岐**
> 本ページの ΔkW（前日計画）／kWh（当日計画）に関する項目は、ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ有効。`delta-kW-no-market`（既定）では三次調整力を単一の予備力量として扱い、これらの項目は無効。

揚水発電所等をイメージした大規模のエネルギー貯蔵システム（Energy Storage System: ESS）を考慮することができる。

- 最大発電能力・充電能力、最小発電能力・充電能力制約を考慮することができる。
  - 最大発電能力・充電能力制約には各能力低下状態を考慮できるように $P_{t,ess}^{\text{discharge}\,\text{des}}$ , $P_{t,ess}^{\text{charge}\,\text{des}}$ が追記されている（出力低下を設定することができる CSV ファイル[「descent.csv」](../../05_csvfile/02_generation.md#出力低下)を参照）。
- 運転状態や蓄電量の許す限りに GF&LFC 調整力や三次調整力を提供することができると想定している。
- 蓄電量の運用に関しては以下の 2 つの制約を考慮することができる。２つの制約を同時に考慮することもできる。デフォルトでは境界条件制約のみ考慮する。
  - 開始時間・終了時間の蓄電量一致条件制約: 最適化対象期間前時刻と終了時刻の蓄電量を基準値に固定する制約
    - 特定時間の蓄電量指定制約: CSV ファイルで指定された時刻、蓄電量を満たすように決定変数を固定する制約

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

## 当日計画における発電量・充電量平均値（`delta-kW-bid` のみ）

前日計画からの引き継ぎとして、以下の前提条件がある

$$
\begin{aligned}
    P_{t,ess}^{\text{da},\text{discharge}}&=p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}1)
\\
    P_{t,ess}^{\text{da},\text{charge}}&=p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}2)
\end{aligned}
$$

その上で、当日計画の発電量・充電量平均値は以下の値となる。

$$
\begin{aligned}
    p_{t,ess}^{\text{discharge}} &\geq P_{t,ess}^{\text{da},\text{discharge}} - P_{t,ess}^{\text{da},\text{charge}} + p_{t,ess}^{\text{id},\text{UP}} - p_{t,ess}^{\text{id},\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}3)
    \\
    p_{t,ess}^{\text{discharge}} &\leq P_{t,ess}^{\text{da},\text{discharge}} - P_{t,ess}^{\text{da},\text{charge}} + p_{t,ess}^{\text{id},\text{UP}} - p_{t,ess}^{\text{id},\text{DOWN}} + \max \left( P_{ess}^{\text{discharge}\,\text{MAX}},  P_{ess}^{\text{charge}\,\text{MAX}}  \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
    p_{t,ess}^{\text{charge}} &\geq P_{t,ess}^{\text{da},\text{charge}} - P_{t,ess}^{\text{da},\text{discharge}} + p_{t,ess}^{\text{id},\text{DOWN}} - p_{t,ess}^{\text{id},\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}5)
    \\
    p_{t,ess}^{\text{charge}} &\leq P_{t,ess}^{\text{da},\text{charge}} - P_{t,ess}^{\text{da},\text{discharge}} + p_{t,ess}^{\text{id},\text{DOWN}} - p_{t,ess}^{\text{id},\text{UP}} + \max \left( P_{ess}^{\text{discharge}\,\text{MAX}},  P_{ess}^{\text{charge}\,\text{MAX}}  \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}6)
\end{aligned}
$$

$$
\begin{aligned}
    p_{t,ess}^{\text{id},\text{UP}} &\leq u_{t,ess}^{\text{id is UP}} \left( P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}} \right)
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}7)
    \\
    p_{t,ess}^{\text{id},\text{DOWN}} &\leq \left( 1 - u_{t,ess}^{\text{id is UP}} \right) \left( P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}} \right)
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}0\text{-}8)
\end{aligned}
$$

ここで $u_{t,ess}^{\text{id is UP}}$ は調整方向を表すバイナリ変数（1: 上げ、0: 下げ）である。式 (2-4-0-7)・(2-4-0-8) は上げと下げの同時提供を禁止する **方向選択制約** であり、右辺の $P_{ess}^{\text{discharge}\,\text{MAX}} + P_{ess}^{\text{charge}\,\text{MAX}}$ は調整電力量の実際の上限ではなく、方向選択のための十分大きな定数（big-M）として用いている。上げ方向のとき $u_{t,ess}^{\text{id is UP}} = 1$ となり下げ調整量 $p_{t,ess}^{\text{id},\text{DOWN}}$ は 0 に固定される（下げ方向はその逆）。調整電力量の実際の上限は、前日計画で確保した三次調整力 $P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}}$ により別途課される。

## 1. エネルギー貯蔵システムの最大発電能力・充電能力制約

$$
\begin{aligned}
   p_{t,ess}^{\text{discharge}}
    & \leq \left( P_{ess}^{\text{discharge}\,\text{MAX}} - P_{t,ess}^{\text{discharge}\,\text{des}} \right) dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}1\text{-}1)
\\
   p_{t,ess}^{\text{charge}}
    & \leq \left( P_{ess}^{\text{charge}\,\text{MAX}} - P_{t,ess}^{\text{charge}\,\text{des}} \right) chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}1\text{-}2)
\end{aligned}
$$

## 2. エネルギー貯蔵システムの最小発電能力・充電能力制約

$$
\begin{aligned}
   p_{t,ess}^{\text{discharge}}
    & \geq P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}2\text{-}1)
\\
   p_{t,ess}^{\text{charge}}
    & \geq P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}2\text{-}2)
\end{aligned}
$$

## 3. エネルギー貯蔵システムの運転状況判定

$$
\begin{aligned}
   dchg_{t,ess} + chg_{t,ess}
    & \leq 1
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}3\text{-}1)
\end{aligned}
$$

| 機能名                                                       | デフォルト | 設定ファイル上での設定名     | True としたときの上記式からの変更内容                   |
| :----------------------------------------------------------- | :--------- | :--------------------------- | :------------------------------------------------------ |
| エネルギー貯蔵システムの運転状況に関するバイナリ変数の連続化 | False      | make_dchg_chg_ess_continuous | バイナリ変数 $dchg_{t,ess}, chg_{t,ess}$ を連続変数にする |

## 4. エネルギー貯蔵システムの GF&LFC 調整力確保可能量制約

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{discharge}\,\text{MAX}} \frac{R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}}{100}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}2)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \leq & \; P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess}
   \- p_{t,ess}^{\text{discharge}} \notag
   \\
        &  + p_{t,ess}^{\text{charge}}
   \- P_{ess}^{\text{charge}\,\text{MIN}} chg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}3)
\\
  p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \leq &  P_{ess}^{\text{charge}\,\text{MAX}} chg_{t,ess}
   \- p_{t,ess}^{\text{charge}} \notag
   \\
        &  + p_{t,ess}^{\text{discharge}}
   \- P_{ess}^{\text{discharge}\,\text{MIN}} dchg_{t,ess}
        & \forall t \in T, \forall ess \in ESS
        & \qquad (2\text{-}4\text{-}4\text{-}4)
\end{aligned}
$$

## 5. エネルギー貯蔵システムの調整力確保可能量制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,ess}^{\text{Tert}\,\text{UP/DOWN}}$ として扱う。

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}1)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}2)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

前日計画では三次調整力を ΔkW（ $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$ ）として、当日計画では実運用電力量（ $p_{t,ess}^{\text{id}\,\text{UP/DOWN}}$ ）として扱う。

#### 前日計画

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}3)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}4)
\end{aligned}
$$

#### 当日計画

前日計画からの引き継ぎとして、以下の前提条件がある

$$
\begin{aligned}
    P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}&=p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}5)
\\
    P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}&=p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}6)
\end{aligned}
$$

その上で、本制約式は以下の通りとなる。当日計画では、 $p_{t,ess}^{\text{id},\text{UP}}$ と $p_{t,ess}^{\text{id},\text{DOWN}}$ が既に $p_{t,ess}^{\text{discharge}}$ と $p_{t,ess}^{\text{charge}}$ に含まれているため（式(2-4-0-3),(2-4-0-4)参照）、二重カウントを避けるために $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ と $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ を 0 として扱う。

$$
\begin{aligned}
   p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
    & \leq P_{ess}^{\text{discharge}\,\text{MAX}}
   \- p_{t,ess}^{\text{discharge}}
   \+ p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}7)
\\
   p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq P_{ess}^{\text{charge}\,\text{MAX}}
   \- p_{t,ess}^{\text{charge}}
   \+ p_{t,ess}^{\text{discharge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}8)
\\
    p_{t,ess}^{\text{id},\text{UP}} \leq P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}9)
\\
    p_{t,ess}^{\text{id},\text{DOWN}} \leq P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}5\text{-}10)
\end{aligned}
$$

## 6. エネルギー貯蔵システムの蓄電量運用制約

$$
\begin{aligned}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}}}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}6\text{-}1)
\end{aligned}
$$

## 7. エネルギー貯蔵システムの最大蓄電量制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,ess}^{\text{Tert}\,\text{DOWN}}$ として扱う。

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}1)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

前日計画では三次調整力を ΔkW（ $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ ）として扱う。

#### 前日計画

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}} \right)
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}2)
\end{aligned}
$$

#### 当日計画

当日計画では、 $p_{t,ess}^{\text{id},\text{DOWN}}$ が既に $p_{t,ess}^{\text{charge}}$ に含まれているため（式(2-4-0-4)参照）、二重カウントを避けるために $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}$ を 0 として扱う。

$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}7\text{-}3)
\end{aligned}
$$

## 8. エネルギー貯蔵システムの最小蓄電量制約

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一の予備力量 $p_{t,ess}^{\text{Tert}\,\text{UP}}$ として扱う。

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}1)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

前日計画では三次調整力を ΔkW（ $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ ）として扱う。

#### 前日計画

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}2)
\end{aligned}
$$

#### 当日計画

当日計画では、 $p_{t,ess}^{\text{id},\text{UP}}$ が既に $p_{t,ess}^{\text{discharge}}$ に含まれているため（式(2-4-0-3)参照）、二重カウントを避けるために $p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}$ を 0 として扱う。

$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}}{\frac{\eta_{ess}}{100}}
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}8\text{-}3)
\end{aligned}
$$

## 9. エネルギー貯蔵システムの開始時間・終了時間の蓄電量一致条件制約

$$
\begin{aligned}
   e_{0,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
           \ \ \left( E_{0,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{0,ess}^{\text{INHE}}
           \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}9\text{-}1)
\\
   e_{end,ess} + e_{end,ess}^{\text{short}} - e_{end,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{base}}}{100}
    & \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}9\text{-}2)
\end{aligned}
$$

| 機能名                         | デフォルト | 設定ファイル上での設定名  | False としたときの上記式からの変更内容       |
| :----------------------------- | :--------- | :------------------------ | :------------------------------------------- |
| ESS の蓄電量境界条件制約の考慮 | True       | set_e_ess_balance_constrs | 上記式(2-4-9-1),(2-4-9-2)を考慮しない       |

## 10. エネルギー貯蔵システムの特定時間の蓄電量指定制約

$$
\begin{aligned}
   e_{t,ess}
    & = \begin{cases}
           E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}                    \\
           \ \ \ \ \ \ \ \left( E_{t,ess}^{\text{INHE}} \text{ is undefined} \right) \\
           E_{t,ess}^{\text{INHE}}                                                   \\
           \ \ \ \ \ \ \ \ \left( \text{Otherwise} \right)
        \end{cases}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T^{\text{INHE}},
   \forall ess \in ESS
   & \qquad (2\text{-}4\text{-}10\text{-}1)
\\
   e_{t,ess} + e_{t,ess}^{\text{short}} - e_{t,ess}^{\text{surplus}}
    & = E_{ess}^{\text{CAP}} \frac{ER_{t,ess}^{\text{plan}}}{100}
    & \forall t \in T_{ess}^{\text{PLAN}} \cap T,
   \forall ess \in ESS
   & \qquad (2\text{-}4\text{-}10\text{-}2)
\end{aligned}
$$

| 機能名                         | デフォルト | 設定ファイル上での設定名   | False としたときの上記式からの変更内容         |
| :----------------------------- | :--------- | :------------------------- | :--------------------------------------------- |
| ESS の蓄電量計画運用制約の考慮 | False      | set_e_ess_schedule_constrs | 上記式(2-4-10-1),(2-4-10-2)を考慮しない       |

## 11. エネルギー貯蔵システムの計画停止期間制約

$$
\begin{aligned}
   dchg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}11\text{-}1)
\\
   chg_{t,ess}
    & = 0
    & \forall t \in T_{ess}^{\text{Planned Outage}} , \forall ess \in ESS
    & \qquad (2\text{-}4\text{-}11\text{-}2)
\end{aligned}
$$
