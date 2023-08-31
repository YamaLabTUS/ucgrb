# 電力系統モデル - テストモデル -

- データ形式の例示や動作確認を目的に作成。
- 東京地域の規模を0.1倍程度にした「Area_A」と北海道地域の規模を0.3倍程度にした「Area_B」で構成される。**設定値や結果自体に特別な意味はない事に注意が必要。**
- 時系列データの期間は2016年4月1日（金）から2017年3月31日（金）の1年間である。
- 上記一年間を受渡日とした最適化を実施するためのダミーデータとして、2016年3月31日（木）と2017年4月1日（土）のデータを追記している。
  - demand.csv、demand_M_req.csv、PV_ACT.csv、PV_FCST_U.csv、PV_FCST_M.csv、PV_FCST_L.csv、WF_ACT.csv、WF_FCST_U.csv、WF_FCST_M.csv、WF_FCST_L.csv、others.csvの2016年3月31日（木）には2016年4月1日（金）のデータを、2017年4月1日（土）には2017年3月31日（金）のデータを記載している
  - demand_R_GF_LFC_UP.csv、demand_R_GF_LFC_DOWN.csv、PV_R_GF_LFC_UP.csv、PV_R_GF_LFC_DOWN.csv、WF_R_GF_LFC_UP.csv、WF_R_GF_LFC_DOWN.csvの2016年3月31日（木）には3月のデータを、2017年4月1日（土）には4月のデータを記載している
  - tie_calculation_section_day.csvの2016年3月31日（木）には3月後半平日のデータを、2017年4月1日（土）には4月休日のデータを記載している
  - 各ファイルの書式は[5. 電力系統データCSVファイルの記述方法](../../docs/05_csvfile/)を参照。

## 発電機データ

### 発電機

対象CSVファイル: generation/generation__01_thermal.csv, generation/generation__02_nuclear.csv,  generation/generation__03_hydro.csv

- ディレクトリ「generation」の中にcsvファイルを配置
- 「thermal」「nuclear」「hydro」の3種のCSVファイルに分けて記載
- 「thermal」はCOAL、OIL、GASの三種類をまとめて記載する。

### 発電機タイプ

対象CSVファイル: generation/generation\_type.csv,

- 起動に関する燃料はすべてA重油を想定
  - emission_factor_startup: 環境省HP「[算定方法・排出係数一覧](https://ghg-santeikohyo.env.go.jp/calc)」より「算定・報告・公表制度における算定方法・排出係数一覧」[itiran_2020_rev.pdf](https://ghg-santeikohyo.env.go.jp/files/calc/itiran_2020_rev.pdf)を参照
  - fuel_price_startup: [東海農政局](https://www.maff.go.jp/tokai/index.html)HP「[原油価格及びＡ重油価格の推移](https://www.maff.go.jp/tokai/seisan/kankyo/ondanka/attach/pdf/index-7.pdf)」を参照し、2014年1月から2020年12月までの原油とA重油の価格差平均値を算出（38.29[千円/kl]）。OIL（原油）のfuel priceに価格差平均値を加算。

### エネルギー貯蔵システム

対象CSVファイル: ESS/ESS.csv

- C_ess_short、C_ess_surplusは、C_short、C_surplusより一桁少ない10000千円/KWhに設定

### 計画停止

対象CSVファイル: planned_outage.csv

- 動作確認用の適当なデータを設定

### 出力低下

対象CSVファイル: descent.csv

- 動作確認用の適当なデータを設定

### 地域データ

### 地域

対象CSVファイル: area

- 動作確認用の適当なデータを設定

## 連系線データ

### 連系線

対象CSVファイル: tie/tie.csv

- 連系線の名称と接続関係を表す


### 連系線運用

対象CSVファイル: ディレクトリ「tie/season/operation」内のCSVファイル

- 4つの時間帯毎にディレクトリ分けをし、更に連系線毎にCSVファイルを分割している。

## 時系列データ

### 電力需要

対象CSVファイル: demand/demand.csv

- Area_Aは東京電力の需要データを、Area_Bは北海道電力の需要データを元に作成

### 電力需要短周期（GF&LFC成分）変動予測誤差率

対象CSVファイル: demand/demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv

- 各地域の電力需要の短周期（GF&LFC成分）変動予測誤差率を示す。
- 一率2%で固定。

### 最低確保単位系統慣性

対象CSVファイル: demand/demand_M_req.csv

- 各地域の最低確保単位系統慣性を示す。
- 一率0MW·s/MVAで固定。

### 太陽光発電実出力

対象CSVファイル: PV/PV_ACT.csv

### 太陽光発電出力予測最大値

対象CSVファイル: PV/PV_FCST_U.csv

### 太陽光発電出力予測値

対象CSVファイル: PV/PV_FCST_M.csv

### 太陽光発電出力予測最小値

対象CSVファイル: PV/PV_FCST_L.csv

### 太陽光発電短周期（GF&LFC成分）変動予測誤差率

対象CSVファイル: PV/PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv

- 一率10%で固定。

### 風力発電実出力 - WF_ACT -

対象CSVファイル: WF/WF_ACT.csv

### 風力発電出力予測最大値 - WF_FCST_U -

対象CSVファイル: WF/WF_FCST_U.csv

### 風力発電出力予測値 - WF_FCST_M -

対象CSVファイル: WF/WF_FCST_M.csv

### 風力発電出力予測最小値 - WF_FCST_L -

対象CSVファイル: WF/WF_FCST_L.csv

### 風力発電短周期（GF&LFC成分）変動予測誤差率 - WF_R_GF_LFC_UP, WF_R_GF_LFC_DOWN -

対象CSVファイル: WF/WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv

- 一率10%で固定。

### 連系線運用容量・マージン

対象CSVファイル: tie/timeline/TTC_forward.csv, TTC_counter.csv, Margin_forward.csv, Margin_counter

- 適当な値が入力されており、値自体に意味は特にない。

### 融通調整量最大値

対象CSVファイル: tie/timeline/ GF_LFC_UP_forward_MAX.csv, GF_LFC_UP_counter_MAX.csv, GF_LFC_DOWN_forward_MAX.csv, GF_LFC_DOWN_counter_MAX.csv, Tert_UP_forward_MAX.csv, Tert_UP_counter_MAX.csv, Tert_DOWN_forward_MAX.csv, Tert_DOWN_counter_MAX.csv


- 適当な値が入力されており、値自体に意味は特にない。


### 各時期連系線運用容量・マージン算出断面　- tie_calculation_section_day, tie_calculation_section_of_the_clock-

対象CSVファイル: tie/season/tie_calculation_section_day.csv, tie_calculation_section_of_the_clock.csv,

- 昼時間を「8～22時」、それ以外を夜時間とする
- month_sectionに入力する季節の区分として、年間を12ヶ月と9月・11月・3月を二分割する、全15時期分割を用いる。<br />月の英語3文字略称（「Jan」「Feb」...）を基本とし、9月、11月、3月は前半と後半を分けるために「\_1st」、「\_2nd」を接尾語として用いる（「Sep_1st」「Sep_2nd」「Nov_1st」「Nov_2nd」「Mar_1st」「Mar_2nd」）。[^1]

[^1]: 電力広域的運営推進期間(OCCTO)の資料[「運用容量の算出方法見直しおよび妥当性確認について」](https://www.occto.or.jp/renkeisenriyou/oshirase/2015/files/02_unyouyouryou_sansyutsuhouhou.pdf)8ページ目を参照
### エネルギー貯蔵システムの蓄電量計画運用 - E_R_plan -

対象CSVファイル: ESS/E_R_plan.csv

- 週間運用を想定し、以下の値を用いる
  - 月曜日 0時: 90%
  - 火曜日 0時: 74%
  - 水曜日 0時: 58%
  - 木曜日 0時: 42%
  - 金曜日 0時: 26%
  - 土曜日 0時: 10%
  - 日曜日 0時: 50%


### 発電機の***N***日毎の発電量上限制約 - Maximum energy constraints -

対象CSVファイル: generation/E_1_day_MAX.csv

- 水力発電機の1日毎の発電量上限値を設定
### その他の発電設備の出力値 - others -

対象CSVファイル: others.csv

- 各地域の流込式水力や地熱発電の出力値を適当に設定
