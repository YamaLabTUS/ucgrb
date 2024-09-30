# 原子力・火力発電機の燃料費関数出力比例係数算出方法

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
   C_{g}^{\text{coef}}
    & = \frac{C_{g}^{\text{fuel}}}{\left( 1 - \frac{ICR_{g}}{100}\right)}
    & \forall g \in G_{N\\&T}
\end{align}
$$

$$
\begin{array}{ll}
      C_{g}^{{\text{fuel}}}
       & : 原子力・火力発電機 g の燃料費比例係数 [千円/\text{MWh}]
      \\
      ICR_{g}
       & : 原子力・火力発電機 g の所内率[\\%]
\end{array}
$$
