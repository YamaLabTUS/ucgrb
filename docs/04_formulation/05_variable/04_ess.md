# エネルギー貯蔵システム（ESS）に関する決定変数

特に記載がない場合、決定変数xは全て非負の実数。 $\left(x \in R_{+} = \left\\{y \in R | y \geq 0\right\\}\right)$

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
      p_{t,ess}^{\text{Tert}\,\text{UP}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次上げ調整力 [\text{MW}]
      \\
      p_{t,ess}^{\text{Tert}\,\text{DOWN}}
       & : 時刻 t におけるエネルギー貯蔵システム ess が確保する三次下げ調整力 [\text{MW}]
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
      dchg_{t,ess} \in \{0,1\}
       & : 時刻 t におけるエネルギー貯蔵システム ess の発電状態(バイナリ変数、1: 運転、0: 停止)
      \\
      chg_{t,ess} \in \{0,1\}
       & : 時刻 t におけるエネルギー貯蔵システム ess の充電状態(バイナリ変数、1: 運転、0: 停止)
\end{array}
$$
