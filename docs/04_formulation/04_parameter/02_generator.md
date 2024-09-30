# 大規模発電機に関する定数

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
       & : 時刻 t における大規模発電機 g の出力低下量 [\text{MW}]
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
       & : 原子力・火力発電機 g の最大出力変化速 [\\%\text{MW}\/分]
\end{array}
$$

## 水力発電機のみに関する定数

$$
\begin{array}{ll}
      U_{t,g}
       & : 時刻 t における水力発電所 g の運転状態 (1: 運転、0: 停止)
\end{array}
$$
