# 連系線に関する決定変数

特に記載がない場合、決定変数xは全て非負の実数。 $\left(x \in R_{+} = \left\\{y \in R | y \geq 0\right\\}\right)$

$$
   \begin{array}{ll}
      p_{t,tie}^{\text{forward}}
       & : 時刻 t における連系線 tie で順方向に融通される電力平均値 [\text{MW}]
      \\
      p_{t,tie}^{\text{counter}}
       & : 時刻 t における連系線 tie で逆方向に融通される電力平均値 [\text{MW}]
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, forward}}
       & : 時刻 t における連系線 tie で順方向に融通される\text{GF\\&LFC}上げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{UP, counter}}
       & : 時刻 t における連系線 tie で逆方向に融通される\text{GF\\&LFC}上げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, forward}}
       & : 時刻 t における連系線 tie で順方向に融通される\text{GF\\&LFC}下げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN, counter}}
       & : 時刻 t における連系線 tie で逆方向に融通される\text{GF\\&LFC}下げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{Tert}\,\text{UP, forward}}
       & : 時刻 t における連系線 tie で順方向に融通される三次上げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{Tert}\,\text{UP, counter}}
       & : 時刻 t における連系線 tie で逆方向に融通される三次上げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{Tert}\,\text{DOWN, forward}}
       & : 時刻 t における連系線 tie で順方向に融通される三次下げ調整力 [\text{MW}]
      \\
      p_{t,tie}^{\text{Tert}\,\text{DOWN, counter}}
       & : 時刻 t における連系線 tie で逆方向に融通される三次下げ調整力 [\text{MW}]
      \\
      d_{t,tie} \in \{0,1\}
       & : 時刻 t における連系線 tie の潮流方向 (バイナリ変数、1: 順方向、0: 逆方向)
      \\
      d_{t,tie}^{\text{GF\\&LFC}\,\text{UP}} \in \{0,1\}
       & : 時刻 t における連系線 tie の\text{GF\\&LFC}上げ調整力の潮流方向 (バイナリ変数、1: 順方向、0: 逆方向)
      \\
      d_{t,tie}^{\text{GF\\&LFC}\,\text{DOWN}} \in \{0,1\}
       & : 時刻 t における連系線 tie の\text{GF\\&LFC}下げ調整力の潮流方向 (バイナリ変数、1: 順方向、0: 逆方向)
      \\
      d_{t,tie}^{\text{Tert}\,\text{UP}} \in \{0,1\}
       & : 時刻 t における連系線 tie の三次上げ調整力の潮流方向 (バイナリ変数、1: 順方向、0: 逆方向)
      \\
      d_{t,tie}^{\text{Tert}\,\text{DOWN}} \in \{0,1\}
       & : 時刻 t における連系線 tie の三次下げ調整力の潮流方向 (バイナリ変数、1: 順方向、0: 逆方向)
   \end{array}
$$
