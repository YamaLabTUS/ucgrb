## 実行方法 - Gurobi Optimizer有償版ライセンスがある場合 -

## 1. 動作確認

特に指定をしなければ、以下の条件で最適化を実施する。

- 電力系統データ: 動作確認用の小規模系統データ[「data-example」](../../data_set/data-example)
- 対象期間（受渡日）: 2016年4月1日のみ

具体的な手順は以下の通りである。

1. 本レジストリをクローンする。

2. 本レジストリと同一ディレクトリ内に以下のスクリプト「main.py」を作成する。

   ```python:main.py
   from ucgrb.ucgrb import ucgrb

   ucgrb()
   ```

   <img src="../img/03/directories_1.png" width="300" alt="Construct of directories">

3. 本レポジトリのルートディレクトリにある、Anaconda環境設定ファイル「env.yml」を読み込んで、仮想環境を構築する。

   - 構築方法: [https://www.sandbox-ots.com/2021/12/anaconda-navigatorconda.html](https://www.sandbox-ots.com/2021/12/anaconda-navigatorconda.html)

4. 仮想環境上で「main.py」を実行する。主に以下の2つの方法がある。

   - spyderを起動して、「main.py」を開き、実行する。

   - コンソールを開いて、main.pyがある場所にcdコマンドで移動し、以下のコマンドを実行する。

     ```cmd
     python main.py
     ```

5. 本レポジトリのルートディレクトリの中にディレクトリ「result」が生成され、その中に、実行情報ファイル「info.txt」と結果ファイル（xlsx、json.zip）が出力される

## 2. 設定ファイル、電力系統データの読み込み

独自の設定ファイル「config.yml」、電力系統データ（CSVファイル）がおさめられているディレクトリ「data」を「main.py」、「ucgrb」と同一のディレクトリに配置して、「main.py」を実行する。

  <img src="../img/03/directories_2.png" width="300" alt="Construct of directories">

## 3. 設定ファイル名の変更

たとえば、設定ファイル名を「config_1.yml」に変更したい場合、「main.py」の記述を以下のように変更すればよい。

```python
from ucgrb.ucgrb import ucgrb

ucgrb("config_1.yml")
```

  <img src="../img/03/directories_3.png" width="300" alt="Construct of directories">

## 4. 電力系統データディレクトリ名の変更

たとえば、電力系統データ（CSVファイル）がおさめられているディレクトリ名を「data_example」に変更したい場合、「config.yml」に以下の記述を追加すればよい。

```yml
csv_data_dir: "data_example"
```

  <img src="../img/03/directories_4.png" width="300" alt="Construct of directories">
