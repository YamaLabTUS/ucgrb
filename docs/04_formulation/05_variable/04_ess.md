# エネルギー貯蔵システム（ESS）に関する決定変数

> **注**: 本ページの ΔkW／kWh／p^id 等の項目は ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ使用される。`delta-kW-no-market`（既定）では参照されない。

特に記載がない場合、決定変数 x は全て非負の実数。 $x \in R_{+}$ （非負の実数）

## 両モード共通の決定変数

$$
\begin{array}{ll}
      p_{t,ess}^{\text{discharge}}
       & : 時刻 t におけるエネルギー貯蔵システム ess の発電出力平均値 [\text{MW}]
      \\
      p_{t,ess}^{\text{charge}}
       & : 時刻 t におけるエネルギー貯蔵システム ess の充電力平均値 [\text{MW}]
      \\
      p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する\text{GF\\&LFC}上げ調整力 [\text{MW}]
      \\
      p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する\text{GF\\&LFC}下げ調整力 [\text{MW}]
      \\
      e_{t,ess}
       & : 時刻 t におけるエネルギー貯蔵システム ess の蓄電量 [\text{MWh}]
      \\
      e_{t,ess}^{\text{short}}
       & : 時刻 t におけるエネルギー貯蔵システム ess の蓄電量計画不足分 [\text{MWh}]
      \\
      e_{t,ess}^{\text{surplus}}
       & : 時刻 t におけるエネルギー貯蔵システム ess の蓄電量計画余剰分 [\text{MWh}]
      \\
      dchg_{t,ess} \in \\{0,1\\}
       & : 時刻 t におけるエネルギー貯蔵システム ess の発電状態(バイナリ変数、1: 運転、0: 停止)
      \\
      chg_{t,ess} \in \\{0,1\\}
       & : 時刻 t におけるエネルギー貯蔵システム ess の充電状態(バイナリ変数、1: 運転、0: 停止)
\end{array}
$$

## `delta-kW-no-market` のみで使用される決定変数

$$
\begin{array}{ll}
      p_{t,ess}^{\text{Tert}\,\text{UP}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次上げ調整力 [\text{MW}]
      \\
      p_{t,ess}^{\text{Tert}\,\text{DOWN}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次下げ調整力 [\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される決定変数（前日計画）

$$
\begin{array}{ll}
      p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次上げ調整力（ΔkW）[\text{MW}]
      \\
      p_{t,ess}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次下げ調整力（ΔkW）[\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される決定変数（当日計画）

$$
\begin{array}{ll}
      p_{t,ess}^{\text{id},\text{UP}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が提供する三次上げ調整電力量（kWh）[\text{MWh}]
      \\
      p_{t,ess}^{\text{id},\text{DOWN}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が提供する三次下げ調整電力量（kWh）[\text{MWh}]
      \\
      u_{t,ess}^{\text{id is UP}} \in \\{0,1\\}
       & : 時刻 t におけるエネルギー貯蔵システム ess が三次上げ調整電力量を提供するか否か (バイナリ変数、1: 上げ調整、0: 下げ調整)
\end{array}
$$
