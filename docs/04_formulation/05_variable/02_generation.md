# 大規模発電機に関する決定変数

> **注**: 本ページの ΔkW／kWh／p^id 等の項目は ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ使用される。`delta-kW-no-market`（既定）では参照されない。

特に記載がない場合、決定変数 x は全て非負の実数。 $x \in R_{+}$ （非負の実数）

## 両モード共通の決定変数

$$
\begin{array}{ll}
      p_{t,g}
       & : 時刻 t における大規模発電機 g の出力平均値 [\text{MW}]
      \\
      p_{t,g}^{\text{GF\\&LFC}\,\text{UP}}
       & : 時刻 t における大規模発電機 g が確保する\text{GF\\&LFC}上げ調整力 [\text{MW}]
      \\
      p_{t,g}^{\text{GF\\&LFC}\,\text{DOWN}}
       & : 時刻 t における大規模発電機 g が確保する\text{GF\\&LFC}下げ調整力 [\text{MW}]
\end{array}
$$

## `delta-kW-no-market` のみで使用される決定変数

$$
\begin{array}{ll}
      p_{t,g}^{\text{Tert}\,\text{UP}}
       & : 時刻 t における大規模発電機 g が確保する三次上げ調整力 [\text{MW}]
      \\
      p_{t,g}^{\text{Tert}\,\text{DOWN}}
       & : 時刻 t における大規模発電機 g が確保する三次下げ調整力 [\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される決定変数（前日計画）

$$
\begin{array}{ll}
      p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : 時刻 t における大規模発電機 g が確保する三次上げ調整力（ΔkW）[\text{MW}]
      \\
      p_{t,g}^{\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : 時刻 t における大規模発電機 g が確保する三次下げ調整力（ΔkW）[\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される決定変数（当日計画）

$$
\begin{array}{ll}
      p_{t,g}^{\text{id},\text{UP}}
       & : 時刻 t における大規模発電機 g が提供する三次上げ調整電力量（kWh）[\text{MWh}]
      \\
      p_{t,g}^{\text{id},\text{DOWN}}
       & : 時刻 t における大規模発電機 g が提供する三次下げ調整電力量（kWh）[\text{MWh}]
      \\
      u_{t,g}^{\text{id is UP}} \in \\{0,1\\}
       & : 時刻 t における大規模発電機 g が三次上げ調整電力量を提供するか否か (バイナリ変数、1: 上げ調整、0: 下げ調整)
\end{array}
$$

## 原子力・火力発電機のみに関する決定変数

$$
\begin{array}{ll}
      u_{t,g} \in \\{0,1\\}
       & : 時刻 t における原子力・火力発電機 g の運転状態 (バイナリ変数、1: 運転、0: 停止)
      \\
      su_{t,g} \in \\{0,1\\}
       & : 時刻 t における原子力・火力発電機 g が起動したか否か (バイナリ変数)
      \\
      sd_{t,g} \in \\{0,1\\}
       & : 時刻 t における原子力・火力発電機 g が停止したか否か (バイナリ変数)
\end{array}
$$
