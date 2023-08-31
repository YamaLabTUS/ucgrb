# 設定ファイルの記述方法

- 対応ファイル形式は[YAML](http://yaml.org/)である。

- 関数"ucgrb"を呼び出す際か、クラス「UCData」のインスタンスを生成する際に、実行ディレクトリ内のファイル**"config.yml"**を読み込む。

  - 異なる設定ファイルを読み込みたい場合は、インスタンス生成時の第一引数に設定ファイルへの相対パスを指定する。

    例: 設定ファイル"config-test.yml"を読み込みたい場合

    ```python
    ucgrb("config-test.yml")
    ```

    ~~~python
    uc_data = UCData("config-test.yml")
    ~~~

