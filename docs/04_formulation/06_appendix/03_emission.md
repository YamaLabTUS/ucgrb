# 大規模発電機のCO<sub>2</sub>排出量算出方法

各添字、集合、定数、決定変数の定義は以下のページを参照。
- [添字と集合](../03_set_and_index.md)
- 定数
  1. [地域に関する定数](../04_parameter/01_area.md)
  2. [大規模発電機に関する定数](../04_parameter/02_generator.md)
  3. [再生可能エネルギーに関する定数](../04_parameter/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する定数](../04_parameter/04_ess.md)
  5. [連系線に関する定数](../04_parameter/05_tie.md)
  6. [計画種に依存する定数](../04_parameter/06_depend_on_scheduling_kind.md)
- 決定変数
  1. [地域に関する決定変数](../05_variable/01_area.md)
  2. [大規模発電機に関する決定変数](../05_variable/02_geneation.md)
  3. [再生可能エネルギーに関する決定変数](../05_variable/03_re.md)
  4. [エネルギー貯蔵システム（ESS）に関する決定変数](../05_variable/04_ess.md)
  5. [連系線に関する決定変数](../05_variable/05_tie.md)


$$
\begin{align}
   F_{t,g,\text{CO} _ {2}}
    & = \begin{cases}
           0 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  \ \ \ \ \ \ \ \left(g \\_ type_{g} \in \{\text{HYDRO},\text{NUCL}\}\right) \\
           C_{g,\text{CO} _ 2}^{\text{coef}}\ p_{t,g} + C_{g,\text{CO} _ 2}^{\text{intc}}\ u_{t,g} + C_{g,\text{CO} _ 2}^{\text{startup}}\ su_{t,g}
           \\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \left(g \\_ type_{g} \in \{\text{OIL},\text{GAS},\text{COAL}\}\right)
        \end{cases}
    & \forall t \in T, \forall g \in G
    & \qquad (1)
\end{align}
$$

$$
\begin{align}
   C_{g,\text{CO} _ {2}}^{\text{coef}}
    & = \frac{EMIS_{g}^{\text{MAX}} - EMIS_{g}^{\text{MIN}}}{P_{g}^{\text{MAX}} - P_{g}^{\text{MIN}}}
    & \forall g \in G
    & \qquad (2)
\\
   C_{g,\text{CO} _ 2}^{\text{intc}}
    & = EMIS_{g}^{\text{MIN}} - C_{g,\text{CO} _ 2}^{\text{coef}} P_{g}^{\text{MIN}}
    & \forall g \in G
    & \qquad (3)
\\
   C_{g,\text{CO} _ 2}^{\text{startup}}
    & = \frac{C_{g}^{\text{startup}}EF_{g \\_ type_{g}}^{\text{startup}}}{FuelPrice_{g \\_ type_{g}}^{\text{startup}}}
    & \forall g \in G
    & \qquad (4)
\end{align}
$$

$$
\begin{align}
   EMIS_{g}^{\text{MAX}}
    & = EF_{g \\_ type_{g}} FCPUMC_{g \\_ type_{g}} HR_{g}^{\text{MAX}} P_{g}^{MAX,GENE \\_ END}
    & \forall g \in G
    & \qquad (5)
   \\
   EMIS_{g}^{\text{MIN}}
    & = EF_{g \\_ type_{g}} FCPUMC_{g \\_ type_{g}} HR_{g}^{\text{MIN}} P_{g}^{MIN,GENE \\_ END}
    & \forall g \in G
    & \qquad (6)
\end{align}
$$

$$
\begin{array}{ll}
      F_{t,g,\text{CO} _ 2}
       & : 時刻 t における大規模発電機 g の\text{CO} _ 2排出量 [t\text{CO} _ 2]
      \\
      C_{g,\text{CO} _ 2}^{\text{coef}}
       & : 大規模発電機 g の単位出力あたりの\text{CO} _ 2排出量[t\text{CO} _ 2/\text{MWh}]
      \\
      C_{g,\text{CO} _ 2}^{\text{intc}}
       & : 大規模発電機 g の単位時間あたりの\text{CO} _ 2排出量[t\text{CO} _ 2]
      \\
      C_{g,\text{CO} _ {2}}^{\text{startup}}
       & : 大規模発電機 g の1回起動あたりの\text{CO} _ 2排出量[t\text{CO} _ 2]
      \\
      EMIS_{g}^{\text{MAX}}
       & : 大規模発電機 g の最大出力時の\text{CO} _ 2排出量[t\text{CO} _ 2]
      \\
      EMIS_{g}^{\text{MIN}}
       & : 大規模発電機 g の最小出力時の\text{CO} _ 2排出量[t\text{CO} _ 2]
      \\
      EF_{g \\_ type_{g}}
       & : 大規模発電機の種類 g \\_ type の排出係数[t\text{CO} _ 2/t\ or\ kl]
      \\
      FCPUMC_{g \\_ type_{g}}
       & : 大規模発電機の種類 g \\_ type の単位発熱量あたりの燃料消費量[t\ or\ kl/Mcal]
      \\
      HR_{g}^{\text{MAX}}
       & : 大規模発電機 g の最大出力時のヒートレート（熱消費率）[Mcal/\text{MWh}]
      \\
      HR_{g}^{\text{MIN}}
       & : 大規模発電機 g の最小出力時のヒートレート（熱消費率）[Mcal/\text{MWh}]
      \\
      EF_{g \\_ type_{g}}^{\text{startup}}
       & : 大規模発電機の種類 g \\_ type の起動時の排出係数[t\text{CO} _ 2/t\ or\ kl]
      \\
      FuelPrice_{g \\_ type_{g}}^{\text{startup}}
       & : 大規模発電機の種類 g \\_ type の起動時の燃料費係数[千円/t\ or\ kl]
\end{array}
$$

※ 大規模発電機の種類 $`g\_type`$ が水力または原子力の場合、CO<sub>2</sub>排出量 $F_{t,g,\text{CO} _ 2}$ は0で固定される。
