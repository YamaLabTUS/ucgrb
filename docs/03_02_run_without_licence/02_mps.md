# MPSファイルの出力、他のソルバーでの実施

Gurobi Optimizerの有償版ライセンスがない場合でも大規模問題を解きたい場合、MILPの問題をMPSファイルで出力し、他のソルバーで解くという手段がある。

実施例として、Python パッケージ [PuLP](https://pypi.org/project/PuLP/)とオープンソースMILPソルバー [CBC](https://github.com/coin-or/Cbc) を用いた場合の手順を示す。

1. [実行方法 - Gurobi Optimizer有償版ライセンスがある場合 -](../03_01_run_with_licence/01_run.md)や[設定ファイル記述例 例11: MPSファイルの出力](../run_with_licence/example.md#例11:-MPSファイルの出力)を参考に、設定ファイルに`export_mps_file: True`を記載して、MPSファイルを出力するように設定する。

2. ucgrbを実施する。有償版ライセンスがない場合、以下のようなエラーが出力される。

   ```cmd
   gurobipy.GurobiError: Model too large for size-limited license; visit https://www.gurobi.com/free-trial for a full license
   ```

3. エラーだとしても、resultディレクトリが生成される。その中のMPSディレクトリにMPS形式のテキストファイルがzip形式で圧縮された、拡張子が「mps.zip」となるファイルが出力される。

   - 最適化はライセンスがないことによるエラーによって実施されないため、ローリング最適化の最初に実施される予定だった最適化問題のみmps.zipファイルとして保存される。

   - [設定ファイル記述例 例11: MPSファイルの出力](../run_with_licence/example.md#例11: MPSファイルの出力)の設定ファイルで実施した場合、2016年4月1日前日計画最適化問題が「2016-04-01_day-ahead_scheduling.mps.zip」というファイル名で出力される。

4. PuLPがインストールされた仮想環境(pyenv)を作成する。

5. CBCを計算機上にダウンロードし、特定の場所に保存する。

   - CBCリリース保存場所: https://github.com/coin-or/Cbc/releases

   - 本例では、「C:\Program Files\cbc」に保存する。

6. 手順3で存在を確認したmps.zipファイルを解凍してMPSファイルに変換し、特定のディレクトリに保存する。

   - 本例では「2016-04-01\_scheduling.mps」というファイル名で保存する。

7. MPSファイルと同じディレクトリに以下のソースコード「mps.py」を作成し、手順4で作成した仮想環境で実施する。

   **mps.py**

   ```python
   import pulp

   # MPSファイルのパス
   MPS_PATH = "2016-04-01_scheduling.mps"

   # CBCソルバーのパス
   CBC_PATH = r"C:\Program Files\cbc\bin\cbc.exe"

   # PuLPによる問題の定義
   var, prob = pulp.LpProblem.fromMPS(MPS_PATH)

   # ソルバーによる最適化の実施
   prob.solve(pulp.apis.COIN_CMD(path=CBC_PATH))

   # 結果の出力
   print("Status:", pulp.LpStatus[prob.status])
   if prob.status == pulp.constants.LpStatusOptimal:
       print("Objective Value:", pulp.value(prob.objective))

   ```