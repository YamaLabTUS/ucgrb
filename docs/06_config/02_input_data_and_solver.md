# 入力データとソルバに関するオプション設定

## 設定ファイルの名称

### config_name

- **書式: 文字列**

設定ファイルを識別するために用意される名称。

**記述例: 設定ファイルに「Case_A」という名称をつけたい場合**

```yaml
config_name: "Case_A"
```

## 入力データに関するオプション値

### csv_data_dir

- **書式: 文字列またはリスト**

- **デフォルト値: `"data"`**

CSV形式で書かれた電力系統データが収められているディレクトリパス。リスト形式で複数のディレクトリを指定することができる。

**記述例: CSVデータをディレクトリ「data1」と「data2」に分けて収められている場合**

```yaml
csv_data_dir:
  - "data1"
  - "data2"
```
### time_series_granularity

- **書式: 数字**

- **デフォルト値: `60`**

最適化の時間粒度。分単位で表記。60以下の場合は、60の約数でなくてはいけない。
60より大きい値の場合は、1440（24時間の分表記）の約数または倍数でなくてはいけない。

### time_series_to_be_linearly_interpolated

- **書式: 配列**

- **デフォルト値: `["demand", "PV_ACT", "PV_FCST_L", "PV_FCST_M", "PV_FCST_U", "WF_ACT", "WF_FCST_L", "WF_FCST_M", "WF_FCST_U", "others"]`**

入力時系列が設定時間粒度よりも粗い場合、自動で補間が実行される。その時の補間方法を線形とする時系列名を指定する。
この項目で指定されていない時系列は、矩形補間となる。

記載例：

```yaml
time_series_to_be_linearly_interpolated:
    - "demand"
    - "PV_ACT"
    - "PV_FCST_L"
    - "PV_FCST_M"
    - "PV_FCST_U"
    - "WF_ACT"
    - "WF_FCST_L"
    - "WF_FCST_M"
    - "WF_FCST_U"
    - "others"

```

または

```yaml
time_series_to_be_linearly_interpolated: ["demand", "PV_ACT", "PV_FCST_L", "PV_FCST_M", "PV_FCST_U", "WF_ACT", "WF_FCST_L", "WF_FCST_M", "WF_FCST_U", "others"]
```


### time_series_not_to_be_interpolated

- **書式: 配列**

- **デフォルト値: `["E_R_plan"]`**

入力時系列が設定時間粒度よりも粗い場合、自動で補間が実行される。その時に補間が実行されない時系列名を指定する。
この項目で指定されていない時系列は、矩形補間または線形補間となる。

記載例：

```yaml
time_series_not_to_be_interpolated:
    - "E_R_plan"
```

または

```yaml
time_series_to_be_linearly_interpolated: ["E_R_plan"]
```


### areas

- **書式: 文字列または配列**

- **デフォルト値: `"ALL"`**

最適化対象となる地域を配列で表示。CSVデータに記載されている全ての地域を対象としたい場合、`ALL`と記載する。

記載例:

```yaml
areas:
    - "Hokkaido"
    - "Tohoku"
    - "Tokyo"
    - "Chubu"
    - "Hokuriku"
    - "Kansai"
    - "Chugoku"
    - "Shikoku"
    - "Kyushu"
```

または

```yaml
areas: ["Hokkaido", "Tohoku", "Tokyo", "Chubu", "Hokuriku", "Kansai", "Chugoku", "Shikoku", "Kyushu"]
```


### setting_method_of_TTC_and_Margin

- **書式: 文字列**
- **デフォルト値: `"fixed"`**

連系線の運用容量とマージンの考慮方法を決定する変数。以下の3種類を選択することができる。

- `"fixed"` : 全期間固定値（デフォルト値）
- `"season"`: 月や時間帯で指定
- `"timeline"`: 最適化時間粒度毎に設定

## Guribiソルバのパラメータ設定

### grb_MIPGap

- **書式: 数字**

- **デフォルト値: `0.01`**

GurobiモデルパラメーターのMIP最適化相対ギャップ”[MIPGap](https://www.gurobi.com/documentation/9.5/refman/mipgap2.html)”の設定

### grb_MIPGapAbs

- **書式: 数字**

- **デフォルト値: `0.01`**

GurobiモデルパラメーターのMIP最適化絶対ギャップ”[MIPGapAbs](https://www.gurobi.com/documentation/9.5/refman/mipgapabs.html)”の設定

### grb_IntegralityFocus

- **書式: 数字**

- **デフォルト値: `1`**

Gurobiモデルパラメーターのインテグリティ・フォーカス”[IntegralityFocus](https://www.gurobi.com/documentation/9.5/refman/integralityfocus.html)”の設定

### grb_FeasibilityTol

- **書式: 数字**

- **デフォルト値: `1.0e-6`**

GurobiモデルパラメーターのFeasibility Tolerance(実現可能性許容範囲”)[FeasibilityTol](https://www.gurobi.com/documentation/9.5/refman/integralityfocus.html)”の設定

### grb_FeasibilityTol_for_Pi_calc

- **書式: 数字**

- **デフォルト値: `1.0e-5`**

シャドウプライス計算ためのGurobiモデルパラメーターのFeasibility Tolerance(実現可能性許容範囲”)[FeasibilityTol](https://www.gurobi.com/documentation/9.5/refman/feasibilitytol.html)”の設定
