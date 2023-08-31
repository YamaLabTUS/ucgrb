# 集合と添字

$$
\begin{array}{ll}
      t \in T=\{ 1, 2, ... , end-1, end \}
       & : 最適化対象期間
      \\
      t \in T_{g}^{\text{Planned Outage}} \\;\\;\\;\\; \forall g \in G_{N\\&T}
       & : 原子力・火力発電機 g の計画停止期間
      \\
      t \in T_{ess}^{\text{PLAN}}
       & : エネルギー貯蔵システム ess の蓄電量計画運用指定時刻(ESSの蓄電量計画運用制約を考慮時に使用)
      \\
      t \in T_{ess}^{\text{Planned Outage}}
       & : エネルギー貯蔵システム ess の計画停止期間
      \\
      t \in T^{\text{INHE,A}}
       & : 大規模発電機の出力、ESSの蓄電量を対象とした、前回最適化からの決定変数引き継ぎ期間
      \\
      t \in T^{\text{INHE,A}}
       & : 原子力・火力発電機の運転状態に関するバイナリ変数を対象とした、前回最適化からの決定変数引き継ぎ期間
      \\
      a \in A
       & : 地域
      \\
      g \in G=\{ G_{N\\&T} \cup G_{HYDRO} \}
       & : 大規模発電機
      \\
      g \in G_{N\\&T}
       & : 原子力・火力発電機
      \\
      g \in G_{NUCL}
       & : 原子力発電
      \\
      g \in G_{HYDRO}
       & : 水力発電機
      \\
      g \in G_{a}
       & : 地域 a に存在する大規模発電機
      \\
      g \in G_{N\\&T,a}
       & : 地域 a に存在する原子力・火力発電機
      \\
      g \in G_{HYDRO,a}
       & : 地域 a に存在する水力発電機
      \\
      ess \in ESS
       & : エネルギー貯蔵システム
      \\
      ess \in ESS_{a}
       & : 地域 a に存在するエネルギー貯蔵システム
      \\
      tie \in TIE
       & : 連系線
      \\
      tie \in TIE_{\text{to}=a}
       & : 地域 a に順方向で接続する連系線
      \\
      tie \in TIE_{\text{from}=a}
       & : 地域 a に逆方向で接続する連系線
\end{array}
$$
