# 電力系統データCSVファイルの記述方法

- 電力系統データのセット例として、[「data-example」](../data_set/data-example/)、[「data-mini」](../data_set/data-mini/)が用意されている。

## プログラム内でのデータの取り扱い方

- クラス「UCData」のインスタンス作成時、電力系統モデルデータは属性「power_system」に保存される。CSVファイル名が「power_system」に属する属性名となり、属性値としてCSVファイル内のテーブルがpythonパッケージ「pandas」のdataFrame形式でインポートされる。
- インポート対象は設定値「csv_data_dir」で指定されたディレクトリ内のCSVファイルである。


## ディレクトリ構成に関して

- 対象ディレクトリ内でさらにディレクトリを作成し、CSVファイルをまとめて配置してもよい。その場合、インポートされたデータの属性名にディレクトリ名は反映されない。
- CSVファイル名の頭にアンダースコア ”_” がある場合、そのファイルはインポート対象外となる。
- CSVファイル名の途中に2連続のアンダースコア "__" がある場合、2連アンダースコア後の記載は無視され、2連アンダースコア前の記載が属性名となる。
- 異なるディレクトリに配置されていたり、2連アンダースコアを利用するなどの理由で、同じ属性名となるCSVファイルが複数有る場合、それぞれのcsvテーブルから生成されたdataFrameが結合され、一つの属性として記録される。


## 時系列データに関して

1行A列が「time」のcsvファイルは時系列データとして扱う。

- A列目はB列目以降の値の対象時間。Hour End表記で，一日を1:00～0:00で表す。
  - 例1: 「2040/8/2 1:00:00」は，2040/8/2 0:00～1:00 を指す。
  - 例2: 「2040/8/3 0:00:00」は，2040/8/2 23:00～8/3 0:00 を指す。**8/3 0:00 のデータは，8/2を対象としていることに注意。**