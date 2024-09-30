# ucgrb（研究用リポジトリ）

**[Click here for the README in English.](README_EN.md)**

Gurobi Optimizerを用いた発電機起動停止計画（Unit Commitment: 以下UC）最適化を実施するためのPythonパッケージ。
連系線で接続された複数地域の電力系統を対象としたUC最適化を実施することができる。

- **本リポジトリはプライベートであり、山口研研究室のOrganization「[YamaLabTUS](https://github.com/YamaLabTUS/)」に属しているアカウントのみアクセスすることができる。**
- **従来のバージョンv2と入力CSVファイルのフォーマットが一部変化している。そのため、いままで用いていた入力CSVファイルを修正しなくてはいけない。「[v2で用いていた電力系統データCSVファイルからの変更方法](docs/08_how_to_modify_csvfile.md)」にその手順を示す。**
- **下記ドキュメントに記載する通りにucgrbを実施するためには、本リポジトリをクローンする際、ディレクトリ名を「ucgrb-private」ではなく、「ucgrb」に変更しなくてはいけない。例えば、コマンドでクローンを行う際には、以下のように記載する必要がある。**

   ```cmd
   git clone https://github.com/YamaLabTUS/ucgrb-private.git ucgrb
   ```
   **参考URL: [https://git-scm.com/book/ja/v2/Git-の基本-Git-リポジトリの取得](https://git-scm.com/book/ja/v2/Git-%E3%81%AE%E5%9F%BA%E6%9C%AC-Git-%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E5%8F%96%E5%BE%97)**


## 目次

1. [特徴](docs/01_feature.md)
2. [必要環境](docs/02_requirement.md)
3. 実行方法と実行例
   1. Gurobi Optimizerの有償ライセンスがある場合
      1. [実行方法](docs/03_01_run_with_licence/01_run.md)
      2. [設定ファイル記述例](docs/03_01_run_with_licence/02_example.md)
   2. Gurobi Optimizerの有償ライセンスがない場合
      1. [小規模モデルでの実行](docs/03_02_run_without_licence/01_run.md)
      2. [MPSファイルの出力、他のソルバーでの実施](docs/03_02_run_without_licence/02_mps.md)
4. 最適化問題の定式化
   1. [目的関数](docs/04_formulation/01_objective_function.md)
   2. 制約
      1. [地域に関する制約](docs/04_formulation/02_constraint/01_area.md)
      2. [大規模発電機に関する制約](docs/04_formulation/02_constraint/02_generation.md)
      3. [再生可能エネルギーに関する制約](docs/04_formulation/02_constraint/03_re.md)
      4. [エネルギー貯蔵システム（ESS）に関する制約](docs/04_formulation/02_constraint/04_ess.md)
      5. [連系線に関する制約](docs/04_formulation/02_constraint/05_tie.md)
      6. [ローリング最適化における決定変数に関する制約](docs/04_formulation/02_constraint/06_inheritance.md)
   3. [集合と添字](docs/04_formulation/03_set_and_index.md)
   4. 定数
      1. [地域に関する定数](docs/04_formulation/04_parameter/01_area.md)
      2. [大規模発電機に関する定数](docs/04_formulation/04_parameter/02_generator.md)
      3. [再生可能エネルギーに関する定数](docs/04_formulation/04_parameter/03_re.md)
      4. [エネルギー貯蔵システム（ESS）に関する定数](docs/04_formulation/04_parameter/04_ess.md)
      5. [連系線に関する定数](docs/04_formulation/04_parameter/05_tie.md)
      6. [計画種に依存する定数](docs/04_formulation/04_parameter/06_depend_on_scheduling_kind.md)
   5. 決定変数
      1. [地域に関する決定変数](docs/04_formulation/05_variable/01_area.md)
      2. [大規模発電機に関する決定変数](docs/04_formulation/05_variable/02_geneation.md)
      3. [再生可能エネルギーに関する決定変数](docs/04_formulation/05_variable/03_re.md)
      4. [エネルギー貯蔵システム（ESS）に関する決定変数](docs/04_formulation/05_variable/04_ess.md)
      5. [連系線に関する決定変数](docs/04_formulation/05_variable/05_tie.md)
   6. 備考
      1. [原子力・火力発電機の燃料費関数出力比例係数算出方法](docs/04_formulation/06_appendix/01_fuel_cost.md)
      2. [原子力・火力発電機の最大出力・最小出力算出方法](docs/04_formulation/06_appendix/02_max_min_output.md)
      3. [大規模発電機のCO<sub>2</sub>排出量算出方法](docs/04_formulation/06_appendix/03_emission.md)
      4. [時間粒度の変更による定式内容の変化](docs/04_formulation/06_appendix/04_time_series_granularity.md)
5. 電力系統データCSVファイルの記述方法
   1. [概要](docs/05_csvfile/01_about.md)
   2. [発電機データ](docs/05_csvfile/02_generation.md)
   3. [地域データ](docs/05_csvfile/03_area.md)
   4. [連系線データ](docs/05_csvfile/04_tie.md)
   5. [時系列データ](docs/05_csvfile/05_timeline.md)
6. 設定値一覧
   1. [設定ファイルの記述方法](docs/06_config/01_how_to_write.md)
   2. [入力データとソルバに関するオプション設定](docs/06_config/02_input_data_and_solver.md)
   3. [UC問題設定](docs/06_config/03_unit_commitment.md)
   4. [ローリング最適化リスト設定](docs/06_config/04_rolling_optimization_list.md)
   5. [結果出力設定](docs/06_config/05_result_output.md)
7. 開発者に向けて
   1. [開発者向け設定値](docs/07_for_developer/01_config_setting.md)
   2. [自動整形に関して](docs/07_for_developer/02_formatter.md)
8. [v2で用いていた電力系統データCSVファイルからの変更方法](docs/08_how_to_modify_csvfile.md)


## ライセンス

[MIT License](LICENSE)
