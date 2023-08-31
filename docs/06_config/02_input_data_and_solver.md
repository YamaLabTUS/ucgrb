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

### areas

- **書式:　文字列または配列**

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



### nuclear_and_thermal_generation_type

- **書式: 文字列または配列**

- **デフォルト値: `["NUCL", "COAL", "GAS", "OIL"]`**

原子力発電機と火力発電機に相当する種類名。

### nuclear_generation_type

- **書式: 文字列または配列**

- **デフォルト値: `["NUCL"]`**

原子力発電機に相当する種類名。

### hydro_generation_type

- **書式: 文字列または配列**

- **デフォルト値: `["HYDRO"]`**

水力発電機に相当する種類名。

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
