# 電力系統モデル - ミニマムモデル -

**[Click here for the README in English.](./README_EN.md)**

- 限定ライセンス版Gurobi Optimizerでのデータ形式の例示や動作確認を目的に作成。
- 東京地域をモデルとした「Area_A」と北海道地域をモデルとした「Area_B」で構成される。**設定値や結果自体に特別な意味はない事に注意が必要。**
- 時系列データの期間は2016年4月1日（金）から2017年3月31日（金）の1年間である。
- 上記一年間を受渡日とするためには、検討期間の前後にそれぞれ1日のダミーデータが必要である。ダミーデータとして、2016年3月31日（木）と2017年4月1日（土）のデータを追記している。
  - demand.csv、demand_M_req.csv、PV_ACT.csv、WF_ACT.csv、others.csvには2016年3月31日（木）として2016年4月1日（金）のデータを、2017年4月1日（土）として2017年3月31日（金）のデータを記載している
  - demand_R_GF_LFC_UP.csv、demand_R_GF_LFC_DOWN.csv、PV_R_GF_LFC_UP.csv、PV_R_GF_LFC_DOWN.csv、WF_R_GF_LFC_UP.csv、WF_R_GF_LFC_DOWN.csvには2016年3月31日（木）として3月のデータを、2017年4月1日（土）として4月のデータを記載している
  - tie_calculation_section_day.csvの2016年3月31日（木）には3月後半平日のデータを、2017年4月1日（土）には4月休日のデータを記載している
  - 各ファイルの書式はreadmeの第5章[「電力系統データCSVファイルの記述方法」](../../README.md#目次)を参照。
## 発電機データ

### 発電機

対象CSVファイル: generation/generation.csv

- 動作確認用の適当な数値で設定

### 発電機タイプ

対象CSVファイル: generation/generation\_type.csv

- 起動に関する燃料はすべてA重油を想定
  - emission_factor_startup: 環境省HP「[算定方法・排出係数一覧](https://ghg-santeikohyo.env.go.jp/calc)」より「算定・報告・公表制度における算定方法・排出係数一覧」[itiran_2020_rev.pdf](https://ghg-santeikohyo.env.go.jp/files/calc/itiran_2020_rev.pdf)を参照
  - fuel_price_startup: [東海農政局](https://www.maff.go.jp/tokai/index.html)HP「[原油価格及びＡ重油価格の推移](https://www.maff.go.jp/tokai/seisan/kankyo/ondanka/attach/pdf/index-7.pdf)」を参照し、2014年1月から2020年12月までの原油とA重油の価格差平均値を算出（38.29[千円/kl]）。OIL（原油）のfuel priceに価格差平均値を加算。

### エネルギー貯蔵システム

対象CSVファイル: ESS/ESS.csv

- 各エネルギー貯蔵システムの設定値を記述
- C_ess_short、C_ess_surplusは、C_short、C_surplusより一桁少ない10000千円/KWhに設定

## 地域データ

### 地域

対象CSVファイル: area

- 動作確認用の適当な値で設定

## 連系線データ

### 連系線

対象CSVファイル: tie.csv

- 動作確認用の適当な値を設定

## 時系列データ

### 電力需要

対象CSVファイル: demand/demand.csv

- 動作確認用の適当な値で設定

### 電力需要短周期（GF&LFC成分）変動予測誤差率

対象CSVファイル: demand/demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv

- 一率2%で固定。

### 最低確保単位系統慣性

対象CSVファイル: demand/demand_M_req.csv

- 一率0MW·s/MVAで固定。

### 太陽光発電実出力

対象CSVファイル: PV/PV_ACT.csv

- 動作確認用の適当な値で設定

### 太陽光発電短周期（GF&LFC成分）変動予測誤差率

対象CSVファイル: PV/PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv

- 一率10%で固定。

### 風力発電実出力

対象CSVファイル: WF/WF_ACT.csv

- 動作確認用の適当な値で設定

### 風力発電短周期（GF&LFC成分）変動予測誤差率

対象CSVファイル: WF/WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv

- 一率10%で固定。

### その他の発電設備の出力値

対象CSVファイル: others.csv

- 各地域の流込式水力や地熱発電の出力値を適当に設定
