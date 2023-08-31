# 大規模発電機に関する決定変数

特に記載がない場合、決定変数xは全て非負の実数。 $\left(x \in R_{+} = \left\\{y \in R | y \geq 0\right\\}\right)$

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
      \\
      p_{t,a}^{\text{Tert}\,\text{UP}}
       & : 時刻 t における大規模発電機 g が確保する三次上げ調整力 [\text{MW}]
      \\
      p_{t,a}^{\text{Tert}\,\text{DOWN}}
       & : 時刻 t における大規模発電機 g が確保する三次下げ調整力 [\text{MW}]
\end{array}
$$

## 原子力・火力発電機のみに関する決定変数

$$
\begin{array}{ll}
      u_{t,g} \in \{0,1\}
       & : 時刻 t における原子力・火力発電機 g の運転状態 (バイナリ変数、1: 運転、0: 停止)
      \\
      su_{t,g} \in \{0,1\}
       & : 時刻 t における原子力・火力発電機 g が起動したか否か (バイナリ変数)
      \\
      sd_{t,g} \in \{0,1\}
       & : 時刻 t における原子力・火力発電機 g が停止したか否か (バイナリ変数)
\end{array}
$$
