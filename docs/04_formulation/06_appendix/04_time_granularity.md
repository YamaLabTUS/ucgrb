# 時間粒度の変更による定式内容の変化

本定式化は、最適化実行時における時間粒度が1時間（60分）であることを想定して記載している。
本プログラムでは、設定値[`time_series_granularity`](../../06_config/02_input_data_and_solver.md#time_series_granularity)を変更することで、任意の時間粒度で最適化を実施することができる。
その際、各種データや定式内容は以下のように変更される。

以下、設定時間粒度と60分の比率を $TSGRatio$ と表記する。例えば、設定時間粒度が30分の場合、 $TSGRatio=0.5$ であり、設定時間粒度が2時間の場合、 $TSGRatio=2$ である。

$TSGRatio$ 以外の各添字、集合、定数、決定変数の定義は以下のページを参照。
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


## 時系列データの補間
時間粒度設定に合わせて、入力データ時系列の粒度も本プログラム内部で自動的に変換される。変換方法は、**入力データの粒度と設定粒度の関係**で決まる。

- 入力データ時系列の粒度が設定粒度よりも**細かい**場合（例: 入力15分間隔・設定60分）、そのデータは**平均値に集約**して扱われる。
- 入力データ時系列の粒度が設定粒度よりも**粗い**場合（例: 入力60分間隔・設定15分）、途中の値は線形または矩形**補間**によって生成される。

> 入力粒度を一定とすると、**設定粒度を細かくするほど補間**が、**粗くするほど平均（集約）**が働く。

具体的には、設定値[`time_series_to_be_linearly_interpolated`](../../06_config/02_input_data_and_solver.md#time_series_to_be_linearly_interpolated)に設定されている時系列が線形補間され、その他の時系列が矩形補間される。


## 最小運転時間、最小停止時間の変更
[大規模発電機に関する定数](../04_parameter/02_generation.md)に記載されている最小運転時間、最小停止時間は時間単位で表記されているため、時間粒度に合わせて変更する必要がある。具体的には $TSGRatio$ で除算を行った後、小数点一位で四捨五入し整数とする。なお、四捨五入の結果、0となってしまった場合は1に置き換える。これは[原子力・火力発電機の必要最小運転時間制約](../02_constraint/02_generation.md#原子力・火力発電機の必要最小運転時間制約)・[必要最小停止時間制約](../02_constraint/02_generation.md#原子力・火力発電機の必要最小停止時間制約)の条件式を成り立たせるための措置である。

## 定式内容の変更
### [目的関数](../01_objective_function.md)
起動費以外の要素はすべて $TSGRatio$ が乗算される。

$$
\begin{aligned}
         \min \ F = &  \sum_{t \in T} \left[\sum_{g \in G_{N\\&T}} Cost_{g,t} + \sum_{a \in A} \left(
                  Cost_{a,t}^{\text{short}} + Cost_{a,t}^{\text{surplus}} +
                  Cost_{a,t}^{\text{Tert,short}} +
                  Cost_{a,t,\text{RE}}^{\text{suppr}} \right) TSGRatio \right.
                  \notag \\
                  & \left.  + \sum_{ess \in \textit{ESS}} Penalty_{ess,t} TSGRatio +
                  \sum_{tie \in \textit{TIE}} Penalty_{tie,t} TSGRatio \right]
    & \qquad (6\text{-}4\text{-}1)
                  \\
         Cost_{g,t} = &
         C_{g}^{\text{coef}}\ p_{t,g} TSGRatio + C_{g}^{\text{intc}}\ u_{t,g} TSGRatio
         \+ C_{g}^{\text{startup}}\ su_{t,g}
         & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}2)
\end{aligned}
$$


### [大規模発電機のN日毎の発電量上限制約](../02_constraint/02_generation.md#大規模発電機のn日毎の発電量上限制約)

$$
\begin{aligned}
   \sum_{i = t}^{t + \frac{24N}{TSGRatio} - 1 } p_{i,g}
    & \leq E_{g}^{N\text{day}\text{MAX}}
    & \forall t \in t^{EN\text{day}\text{MAX}} + \frac{24N}{TSGRatio} \times m \; (m = 0,1,2\dots), \forall g \in G
    & \qquad (6\text{-}4\text{-}3)
\end{aligned}
$$

### [原子力・火力発電機の出力変化速度制約](../02_constraint/02_generation.md#原子力・火力発電機の出力変化速度制約)

$$
\begin{aligned}
   p_{t,g} + p_{t,g}^{\text{Tert}\,\text{UP}} - P_{g}^{\text{MAX}} (1-u_{t,g})
    & \leq p_{t-1,g} + 60 \frac{R_{g}^{\text{ramp,MAX}}TSGRatio}{100}  P_{g}^{\text{MAX}} + P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}4)
\\
   p_{t,g} - p_{t,g}^{\text{Tert}\,\text{DOWN}}  + P_{g}^{\text{MAX}} (1-u_{t,g})
    & \geq p_{t-1,g} - 60 \frac{R_{g}^{\text{ramp,MAX}}TSGRatio}{100} P_{g}^{\text{MAX}} - P_{g}^{\text{MAX}} (1-u_{t-1,g})
    & \forall t \in T, \forall g \in G_{N\\&T}
    & \qquad (6\text{-}4\text{-}5)
\end{aligned}
$$

### [エネルギー貯蔵システムの蓄電量運用制約](../02_constraint/04_ess.md#エネルギー貯蔵システムの蓄電量運用制約)

$$
\begin{aligned}
   e_{t,ess}
    & = e_{t-1,ess}
   \- \frac{p_{t,ess}^{\text{discharge}} TSGRatio}{\frac{\eta_{ess}}{100}}
   \+ \frac{\gamma_{ess}}{100} p_{t,ess}^{\text{charge}} TSGRatio
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}6)
\end{aligned}
$$

### [エネルギー貯蔵システムの最大蓄電量制約](../02_constraint/04_ess.md#エネルギー貯蔵システムの最大蓄電量制約)
$$
\begin{aligned}
   e_{t,ess} + \frac{\gamma_{ess}}{100} \left( p_{t,ess}^{\text{GF\\&LFC}\,\text{DOWN}}
   \+ p_{t,ess}^{\text{Tert}\,\text{DOWN}} \right) TSGRatio
    & \leq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MAX}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}7)
\end{aligned}
$$

### [エネルギー貯蔵システムの最小蓄電量制約](../02_constraint/04_ess.md#エネルギー貯蔵システムの最小蓄電量制約)
$$
\begin{aligned}
   e_{t,ess} - \frac{p_{t,ess}^{\text{GF\\&LFC}\,\text{UP}}
      \+ p_{t,ess}^{\text{Tert}\,\text{UP}}}{\frac{\eta_{ess}}{100}} TSGRatio
    & \geq E_{ess}^{\text{CAP}} \frac{ER_{ess}^{\text{MIN}}}{100}
    & \forall t \in T, \forall ess \in ESS
    & \qquad (6\text{-}4\text{-}8)
\end{aligned}
$$
