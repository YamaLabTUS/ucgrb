# 大規模発電機に関する定数

> **注**: 本ページの ΔkW／kWh／p^id 等の項目は ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ使用される。`delta-kW-no-market`（既定）では参照されない。

## 両モード共通の定数

`delta-kW-no-market` / `delta-kW-bid` のどちらでも使用される、燃料費・出力能力・起動費・運転制約などの定数。

$$
\begin{array}{ll}
      C_{g}^{\text{coef}}
       & : 大規模発電機 g の燃料費関数の出力比例係数 [千円/\text{MWh}]
      \\
      C_{g}^{\text{intc}}
       & : 大規模発電機 g の燃料費関数の定数項 [千円/\text{h}]
      \\
      C_{g}^{\text{startup}}
       & : 大規模発電機 g の起動費 [千円]
      \\
      P_{g}^{\text{MAX}}
       & : 大規模発電機 g の最大出力 [\text{MW}]
      \\
      P_{t,g}^{\text{des}}
       & : 時刻 t における大規模発電機 g の一時的な出力低下量 [\text{MW}]
      \\
      P_{g}^{\text{MIN}}
       & : 大規模発電機 g の最小出力 [\text{MW}]
      \\
      R_{t,g}^{\text{GF\\&LFC}\,\text{MAX}}
       & : 大規模発電機 g の\text{GF\\&LFC}調整力確保可能量 [\\%\text{MW}]
      \\
      M_{g}
       & : 大規模発電機 g の単位慣性定数 [\text{MW}\cdot\text{s/MVA}]
      \\
      E_{g}^{N\text{day}\text{MAX}}
       & : 大規模発電機 g の\textit{N}日毎の発電量上限制約 [\text{MWh}]
      \\
      t^{EN\text{day}\text{MAX}}
       & : 大規模発電機 g の\textit{N}日毎の発電量上限制約を考慮し始める時刻 [日時]
      \\
      P_{t,g}^{\text{INHE}}
       & : 前回最適化で決定された時刻 t における大規模発電機 g の出力平均値 [\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される定数（前日計画）

三次調整力（ΔkW、kW価値）の調達費単価。

$$
\begin{array}{ll}
      C_{g}^{\Delta\text{kW}\,\text{UP}}
       & : 大規模発電機 g の三次上げ調整力（ΔkW）の調達費単価 [千円/\text{MW}]
      \\
      C_{g}^{\Delta\text{kW}\,\text{DOWN}}
       & : 大規模発電機 g の三次下げ調整力（ΔkW）の調達費単価 [千円/\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される定数（当日計画）

三次調整電力量（kWh）の調達費単価、および前日計画から引き継ぐ発電量平均値・三次調整力（ΔkW）。

$$
\begin{array}{ll}
      C_{g}^{\text{kWh}\,\text{UP}}
       & : 大規模発電機 g の三次上げ調整電力量（kWh）の調達費単価 [千円/\text{MWh}]
      \\
      C_{g}^{\text{kWh}\,\text{DOWN}}
       & : 大規模発電機 g の三次下げ調整電力量（kWh）の調達費単価 [千円/\text{MWh}]
      \\
      P_{t,g}^{\text{da}}
       & : 前日計画で決定された時刻 t における大規模発電機 g の発電量平均値 [\text{MW}]
      \\
      P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : 前日計画で決定された時刻 t における大規模発電機 g の三次上げ調整力（ΔkW）[\text{MW}]
      \\
      P_{t,g}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : 前日計画で決定された時刻 t における大規模発電機 g の三次下げ調整力（ΔkW）[\text{MW}]
\end{array}
$$

## 原子力・火力発電機のみに関する定数

$$
\begin{array}{ll}
      MinUpTime_{g}
       & : 原子力・火力発電機 g の最小運転時間 [\text{h}]
      \\
      MinDownTime_{g}
       & : 原子力・火力発電機 g の最小停止時間 [\text{h}]
      \\
      U_{t,g}^{\text{INHE}}
       & : 前回最適化で決定された時刻 t における原子力・火力発電機 g の運転状態 (1: 運転、0: 停止)
      \\
      SU_{t,g}^{\text{INHE}}
       & : 前回最適化で時刻 t における原子力・火力発電機 g が起動したか否か
      \\
      SD_{t,g}^{\text{INHE}}
       & : 前回最適化で時刻 t における原子力・火力発電機 g が停止したか否か
      \\
      R_{g}^{\text{ramp,MAX}}
       & : 原子力・火力発電機 g の最大出力変化速度 [\\%\text{MW}/分]
\end{array}
$$

## 水力発電機のみに関する定数

$$
\begin{array}{ll}
      U_{t,g}
       & : 時刻 t における水力発電所 g の運転状態 (1: 運転、0: 停止)
\end{array}
$$
