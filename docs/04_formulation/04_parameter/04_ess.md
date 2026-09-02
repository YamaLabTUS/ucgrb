# エネルギー貯蔵システム（ESS）に関する定数

> **注**: 本ページの ΔkW／kWh／p^id 等の項目は ΔkW価値考慮版（`formulation_type: "delta-kW-bid"`）でのみ使用される。`delta-kW-no-market`（既定）では参照されない。

## 両モード共通の定数

`delta-kW-no-market` / `delta-kW-bid` のどちらでも使用される、蓄電量ペナルティ・充放電能力・効率・蓄電容量などの定数。

$$
\begin{array}{ll}
      C_{ess}^{\text{short}}
       & : エネルギー貯蔵システム ess の蓄電量計画不足分ペナルティ係数 [千円/\text{MWh}]
      \\
      C_{ess}^{\text{surplus}}
       & : エネルギー貯蔵システム ess の蓄電量計画余剰分ペナルティ係数 [千円/\text{MWh}]
      \\
      P_{ess}^{\text{discharge}\,\text{MAX}}
       & :エネルギー貯蔵システム ess の最大発電能力 [\text{MW}]
      \\
      P_{ess}^{\text{charge}\,\text{MAX}}
       & :エネルギー貯蔵システム ess の最大充電能力 [\text{MW}]
      \\
      P_{t,ess}^{\text{discharge}\,\text{des}}
       & :時刻 t におけるエネルギー貯蔵システム ess の最大発電能力低下量 [\text{MW}]
      \\
      P_{t,ess}^{\text{charge}\,\text{des}}
       & :時刻 t におけるエネルギー貯蔵システム ess の最大充電能力低下量 [\text{MW}]
      \\
      P_{ess}^{\text{discharge}\,\text{MIN}}
       & : エネルギー貯蔵システム ess の最小発電能力 [\text{MW}]
      \\
      P_{ess}^{\text{charge}\,\text{MIN}}
       & : エネルギー貯蔵システム ess の最小充電能力 [\text{MW}]
      \\
      R_{ess}^{\text{GF\\&LFC}\,\text{MAX}}
       & : エネルギー貯蔵システム ess の調整力確保可能量 [\\%]
      \\
      \eta_{ess}
       & : エネルギー貯蔵システム ess の発電運転時総合効率 [\\%]
      \\
      \gamma_{ess}
       & : エネルギー貯蔵システム ess の充電運転時総合効率 [\\%]
      \\
      E_{ess}^{\text{CAP}}
       & : エネルギー貯蔵システム ess の蓄電容量 [\text{MWh}]
      \\
      ER_{ess}^{\text{MAX}}
       & : エネルギー貯蔵システム ess の蓄電量上限 [\\%]
      \\
      ER_{ess}^{\text{MIN}}
       & : エネルギー貯蔵システム ess の蓄電量下限 [\\%]
      \\
      ER_{ess}^{\text{base}}
       & : エネルギー貯蔵システム ess の蓄電量の時間境界条件値 [\\%]
      \\
      ER_{t,ess}^{\text{plan}}
       & : エネルギー貯蔵システム ess の時刻 t における蓄電量計画値 [\\%]
      \\
      M_{ess}
       & : エネルギー貯蔵システム ess の単位慣性定数 [\text{MW}\cdot\text{s/MVA}]
      \\
      E_{t,ess}^{\text{INHE}}
       & : 前回最適化で決定された時刻 t におけるエネルギー貯蔵システム ess の蓄電量 [\text{MWh}]
\end{array}
$$

## `delta-kW-bid` のみで使用される定数（前日計画）

三次調整力（ΔkW、kW価値）の調達費単価。

$$
\begin{array}{ll}
      C_{ess}^{\Delta\text{kW}\,\text{UP}}
       & : エネルギー貯蔵システム ess の三次上げ調整力（ΔkW）の調達費単価 [千円/\text{MW}]
      \\
      C_{ess}^{\Delta\text{kW}\,\text{DOWN}}
       & : エネルギー貯蔵システム ess の三次下げ調整力（ΔkW）の調達費単価 [千円/\text{MW}]
\end{array}
$$

## `delta-kW-bid` のみで使用される定数（当日計画）

三次調整電力量（kWh）の調達費単価、および前日計画から引き継ぐ充放電力平均値・三次調整力（ΔkW）。

$$
\begin{array}{ll}
      C_{ess}^{\text{kWh}\,\text{UP}}
       & : エネルギー貯蔵システム ess の三次上げ調整電力量（kWh）の調達費単価 [千円/\text{MWh}]
      \\
      C_{ess}^{\text{kWh}\,\text{DOWN}}
       & : エネルギー貯蔵システム ess の三次下げ調整電力量（kWh）の調達費単価 [千円/\text{MWh}]
      \\
      P_{t,ess}^{\text{da},\text{discharge}}
       & : 前日計画で決定された時刻 t におけるエネルギー貯蔵システム ess の発電出力平均値 [\text{MW}]
      \\
      P_{t,ess}^{\text{da},\text{charge}}
       & : 前日計画で決定された時刻 t におけるエネルギー貯蔵システム ess の充電力平均値 [\text{MW}]
      \\
      P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{UP}}
       & : 前日計画で決定された時刻 t におけるエネルギー貯蔵システム ess の三次上げ調整力（ΔkW）[\text{MW}]
      \\
      P_{t,ess}^{\text{da},\Delta\text{kW}\,\text{Tert}\,\text{DOWN}}
       & : 前日計画で決定された時刻 t におけるエネルギー貯蔵システム ess の三次下げ調整力（ΔkW）[\text{MW}]
\end{array}
$$
