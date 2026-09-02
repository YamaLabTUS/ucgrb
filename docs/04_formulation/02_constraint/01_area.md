# 地域に関する制約

> **[`formulation_type`](../../06_config/03_unit_commitment.md#formulation_type) による条件分岐**
> 本ページの ΔkW（前日計画）／kWh（当日計画）に関する項目は、ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ有効。`delta-kW-no-market`（既定）では三次調整力を単一の予備力量として扱い、これらの項目は無効。

地域毎に、以下の制約を考慮することができる。

- 需給バランス制約
- GF&LFC 調整力制約
- 三次調整力制約
  - RE 電源の予測値と予測最小値の差を補償する上げ調整力と、予測値と予測最大値の差を補償する下げ調整力の 2 種類がある。
- 必要慣性定数制約

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

## 1. 需給バランス制約

$$
\begin{aligned}
   \sum_{g \in G_{a}}
   p_{t,g}+ P_{t,a,\text{Others}}
  \+ \sum_{ess \in ESS_{a}} \left(
   p_{t,ess}^{\text{discharge}} - p_{t,ess}^{\text{charge}} \right) \notag
   \\
  \+ P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}}
  \+ P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}}
   \left( p_{t,tie}^{\text{forward}} - p_{t,tie}^{\text{counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}}
   \left( p_{t,tie}^{\text{counter}} - p_{t,tie}^{\text{forward}} \right) \notag
   \\
  \+ p_{t,a}^{\text{short}} - p_{t,a}^{\text{surplus}}
    & = D_{t,a}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}1\text{-}1)
\end{aligned}
$$

## 2. GF&LFC 調整力制約

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq D_{t,a}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}1)
\end{aligned}
$$

$$
\begin{aligned}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}2)
\end{aligned}
$$

$$
\begin{aligned}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}} \right)
    & \geq p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq D_{t,a}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
\sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}5)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}} - p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}} \right)
    & \geq p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}2\text{-}6)
\end{aligned}
$$

## 3. 必要 GF&LFC 調整力

$$
\begin{aligned}
   D_{t,a}^{\text{GF\\&LFC}\,\text{UP, req}}
    & =  D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}1)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}2)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{UP}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
   D_{t,a}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = D_{t,a} \frac{R_{t,a}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}4)
\\
   p_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{PV}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}5)
\\
   p_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} \right)
   \frac{R_{t,a,\text{WF}}^{\text{GF\\&LFC}\,\text{DOWN}}}{100}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}3\text{-}6)
\end{aligned}
$$

各式を考慮するか否かは、設定ファイルの記載を編集することで、簡単に変更することができる。各設定値は以下の通りである。

| 条件名                                     | デフォルト値 | 設定ファイル上での設定名                | False としたときの必要 GF＆LFC 調整力の変更内容 |
| :----------------------------------------- | :----------- | :-------------------------------------- | :---------------------------------------------- |
| 需要起因の必要 GF&LFC 上向き調整力の有無   | True         | consider_required_gf_lfc_up_by_demand   | 式（2-1-3-1）の右辺を 0 にする                  |
| 太陽光起因の必要 GF&LFC 上向き調整力の有無 | True         | consider_required_gf_lfc_up_by_pv       | 式（2-1-3-2）の右辺を 0 にする                  |
| 風力起因の必要 GF&LFC 上向き調整力の有無   | True         | consider_required_gf_lfc_up_by_wf       | 式（2-1-3-3）の右辺を 0 にする                  |
| 需要起因の必要 GF&LFC 下向き調整力の有無   | False        | consider_required_gf_lfc_down_by_demand | 式（2-1-3-4）の右辺を 0 にする                  |
| 太陽光起因の必要 GF&LFC 下向き調整力の有無 | False        | consider_required_gf_lfc_down_by_pv     | 式（2-1-3-5）の右辺を 0 にする                  |
| 風力起因の必要 GF&LFC 下向き調整力の有無   | False        | consider_required_gf_lfc_down_by_wf     | 式（2-1-3-6）の右辺を 0 にする                  |

## 4. 三次調整力制約

三次調整力の確保制約は `formulation_type` により扱う調整力量が異なる。`delta-kW-no-market` では三次調整力を単一量 $p_{t,g}^{\text{Tert}\,\text{UP/DOWN}}$ として確保する。`delta-kW-bid` では前日計画において ΔkW 価値の三次調整力 $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$ として確保する（`delta-kW-bid` で本制約を考慮するのは前日計画のみ。当日計画では考慮しない）。

### `formulation_type: "delta-kW-no-market"` の場合

（既定）三次調整力を単一量 $p_{t,g}^{\text{Tert}\,\text{UP/DOWN}}$ として確保する。

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}1)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}}
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}  \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}2)
\end{aligned}
$$

$p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}$ 、 $p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}$ は負の値を取る可能性があるため、
上げ調整力の合計値が 0 以上でなくていはいけない制約を式（2-1-4-3）として加える。

$$
\begin{aligned}
 \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq 0
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}3)
\end{aligned}
$$

$$
\begin{aligned}
  \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}4)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}5)
\end{aligned}
$$

### `formulation_type: "delta-kW-bid"` の場合

前日計画では、三次調整力を ΔkW 価値の $p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP/DOWN}}$ として確保する。`delta-kW-bid` で本制約を考慮するのは**前日計画のみ**であり、当日計画では考慮しない（当日は kWh 価値の調整電力量として扱う）。

#### 前日計画

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}} \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}6)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}}
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}  \notag
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}7)
\end{aligned}
$$

$p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}$ 、 $p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}$ は負の値を取る可能性があるため、
上げ調整力の合計値が 0 以上でなくていはいけない制約を式（2-1-4-8）として加える。

$$
\begin{aligned}
 \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, forward}} - p_{t,tie}^{\text{Tert}\,\text{UP, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{UP, counter}} - p_{t,tie}^{\text{Tert}\,\text{UP, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{UP, short}} \notag
    & \geq 0
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}8)
\end{aligned}
$$

$$
\begin{aligned}
  \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}9)
\end{aligned}
$$

$$
\begin{aligned}
   \sum_{g \in G_{a}} p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ \sum_{ess \in ESS_{a}} p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN}}
  \+ p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN}} \notag
   \\
  \+ \sum_{tie \in TIE_{\text{to}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} \right) \notag
   \\
  \+ \sum_{tie \in TIE_{\text{from}=a}} \left(
   p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}} - p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}} \right)
  \+ p_{t,a}^{\text{Tert}\,\text{DOWN, short}} \notag
    & \geq p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
   \\
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}4\text{-}10)
\end{aligned}
$$

## 5. 必要三次調整力

$$
\begin{aligned}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{output}} - p_{t,a,\text{PV}}^{\text{suppr}} - P_{t,a,\text{PV}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}1)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{UP, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{output}} - p_{t,a,\text{WF}}^{\text{suppr}} - P_{t,a,\text{WF}}^{\text{lower}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}2)
\end{aligned}
$$

$$
\begin{aligned}
   p_{t,a,\text{PV}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{PV}}^{\text{upper}} - P_{t,a,\text{PV}}^{\text{output}}+ p_{t,a,\text{PV}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}3)
\\
   p_{t,a,\text{WF}}^{\text{Tert}\,\text{DOWN, req}}
    & = \left( P_{t,a,\text{WF}}^{\text{upper}} - P_{t,a,\text{WF}}^{\text{output}}+ p_{t,a,\text{WF}}^{\text{suppr}} \right) U^{\text{Tert}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}5\text{-}4)
\end{aligned}
$$

各式を考慮するか否かは、設定ファイルの記載を編集することで、簡単に変更することができる。各設定は以下の通りである。

| 条件名                                 | デフォルト値 | 設定ファイル上での設定名          | False としたときの必要三次調整力の変更内容 |
| :------------------------------------- | :----------- | :-------------------------------- | :----------------------------------------- |
| 太陽光起因の必要三次上向き調整力の有無 | True         | consider_required_tert_up_by_pv   | 式（2-1-5-1）の右辺を 0 にする             |
| 風力起因の必要三次上向き調整力の有無   | True         | consider_required_tert_up_by_wf   | 式（2-1-5-2）の右辺を 0 にする             |
| 太陽光起因の必要三次下向き調整力の有無 | False        | consider_required_tert_down_by_pv | 式（2-1-5-3）の右辺を 0 にする             |
| 風力起因の必要三次下向き調整力の有無   | False        | consider_required_tert_down_by_wf | 式（2-1-5-4）の右辺を 0 にする             |

## 6. 必要慣性定数制約

$$
\begin{aligned}
   \sum_{g \in G_{N\\&T,a}} P_{g}^{\text{MAX}} u_{t,g} M_{g}
  \+ \sum_{g \in G_{HYDRO,a}} P_{g}^{\text{MAX}} M_{g} \notag
   \\
  \+ \sum_{ess \in ESS_{a}} P_{ess}^{\text{discharge}\,\text{MAX}} dchg_{t,ess} M_{p}
    & \geq D_{t,a} M_{t,a}^{\text{req}}
    & \forall t \in T, \forall a \in A
    & \qquad (2\text{-}1\text{-}6\text{-}1)
\end{aligned}
$$

上記式を考慮するか否かは、設定ファイルの記載を編集することで、簡単に変更することができる。設定は以下の通りである。

| 条件名               | デフォルト値 | 設定ファイル上での設定名 | False としたときの必要慣性定数制約の変更内容 |
| :------------------- | :----------- | :----------------------- | :------------------------------------------- |
| 慣性定数必要量の有無 | True         | consider_require_inertia | 上記式の右辺を 0 にする                      |
