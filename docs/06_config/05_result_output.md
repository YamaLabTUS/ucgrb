# 結果出力設定

## 結果出力のオプション設定

### result_dir

- **書式: 文字列**
- **デフォルト値: `"result"`**

最適化結果を保存するディレクトリパス

### export_mps_file

- **書式: ブール値**
- **デフォルト値: `False`**

各最適化問題の定式をMPSファイル形式で保存するか否かを決める変数。

参考URL: [MPS format](https://www.gurobi.com/documentation/9.5/refman/mps_format.html)

### export_json_file

- **書式: ブール値**
- **デフォルト値: `True`**

各最適化結果と各制約式のシャドウプライスをJSONファイル形式で保存するか否かを決める変数。

参考URL: [JSON solution format](https://www.gurobi.com/documentation/9.5/refman/json_solution_format.html)

### export_xlsx_file

- **書式: ブール値 or 辞書型**
- **デフォルト値: `{"shadow_price": True, "generaion": False,"ESS": False, "tie": True}`**

関数「make_grb_model」の中で、最適化結果をxlsxファイルに保存するか否かを決める変数。

全エリア合計の結果が出力されるシート"total"と、各地域の結果が出力されるシートが出力される。

オプションで、下記のシートも出力する事ができ、辞書型で出力するか否かを設定することができる。

- **shadow_price**: 地域毎に設定されている制約のシャドウプライスの時系列を記録したシートが出力する。
- **generation**: 地域毎に設置されている各大規模発電機の発電力や確保予備力の時系列を記録したシートが出力される。
- **ESS**: 地域毎に設置されている各ESSの充放電量や確保予備力の時系列を記録したシートが出力される。
- **tie**: 連系線の電力融通の時系列を記録したシートが出力される。

Falseの場合はxlsxファイルそのものを出力しない。各シートに対する記載がない場合は、デフォルト値の辞書型に基づいて出力される。

**記載例: 大規模発電機とESSのシートを出力したい場合**

```yaml
export_xlsx_file:
    generation: True
    ESS: True
```

または

```yaml
export_xlsx_file: {"generation": True, "ESS": True}
```

### graphical_prop_for_xlsx_graph

- **書式: 辞書型**
- **デフォルト値:**

```yaml
{
  "bar"{
    "Others": {"solidFill": "4F6228", "line": {"solidFill": "4F6228", "width": 1.5},},  # 暗い黄緑,
    "HYDRO": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "558ED5",  # 鈍い青紫
            "background": "FFFFFF",
        },
        "line": {"solidFill": "558ED5", "width": 1.5},  # 鈍い青紫
    },
    "NUCL": {
        "pattFill": {
            "preset": "smGrid",  # 格子(小)
            "foreground": "002060",  # あざやかな青紫
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060", "width": 1},  # あざやかな青紫
    },
    "COAL": {
        "pattFill": {
            "preset": "dkVert",  # 縦ストライプ: 暗い
            "foreground": "583822",  # 深い橙
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822", "width": 1},  # 深い橙
    },
    "GAS": {
        "pattFill": {
            "preset": "pct20",  # 点線: 20%
            "foreground": "C0504D",  # 鈍い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D", "width": 1},  # 鈍い赤
    },
    "OIL": {
        "pattFill": {
            "preset": "dkDnDiag",  # 対角ストライプ: 右下がり（反転）
            "foreground": "781E1E",  # 深い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E", "width": 1},  # 深い赤
    },
    "Charge of ESS": {
        "solidFill": "FFFF00",  # あざやかな黄
        "line": {"solidFill": "C0504D", "width": 1},  # 鈍い赤
    },
    "Discharge of ESS": {
        "solidFill": "FFFF00",  # あざやかな黄
        "line": {"solidFill": "4F81BD", "width": 1},  # 鈍い青紫
    },
    "ESS": {
        "solidFill": "FFFF00",  # あざやかな黄
        "line": {"solidFill": "BBBF4D", "width": 1},  # 鈍い黄緑
    },
    "PV": {"solidFill": "ED7D31"},  # 明るい橙
    "WF": {"solidFill": "4472C4"},  # 深い青紫
    "Suppression of PV": {"solidFill": "F8CBAD"},  # 明るい灰みの橙
    "Suppression of WF": {"solidFill": "B4C7E7"},  # 明るい灰みの青紫
    "Outflow by tie": {
        "noFill": True,
        "line": {"solidFill": "C0504D", "width": 1.5, "dashStyle": "sysDash"},  # 鈍い赤
    },
    "Inflow by tie": {
        "noFill": True,
        "line": {"solidFill": "4F81BD", "width": 1.5, "dashStyle": "sysDash"},  # 鈍い青紫
    },
    "Short": {"solidFill": "FF0000"},  # あざやかな赤
    "Surplus": {"solidFill": "CCA3A3"},  # やや灰色い赤
    "Coef (NUCL)": {
        "pattFill": {
            "preset": "smGrid",  # 格子(小)
            "foreground": "002060",  # あざやかな青紫
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060", "width": 1},  # あざやかな青紫
    },
    "Intc (NUCL)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "002060",  # あざやかな青紫
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060"},  # あざやかな青紫
    },
    "Start Up (NUCL)": {"solidFill": "002060"},  # あざやかな青紫
    "Coef (COAL)": {
        "pattFill": {
            "preset": "dkVert",  # 縦ストライプ: 暗い
            "foreground": "583822",  # 深い橙
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822", "width": 1},  # 深い橙
    },
    "Intc (COAL)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "583822",  # 深い橙
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822"},  # 深い橙
    },
    "Start Up (COAL)": {"solidFill": "583822"},  # 深い橙
    "Coef (GAS)": {
        "pattFill": {
            "preset": "pct20",  # 点線: 20%
            "foreground": "C0504D",  # 鈍い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D", "width": 1},  # 鈍い赤
    },
    "Intc (GAS)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "C0504D",  # 鈍い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D"},  # 鈍い赤
    },
    "Start Up (GAS)": {"solidFill": "C0504D"},  # 鈍い赤
    "Coef (OIL)": {
        "pattFill": {
            "preset": "dkDnDiag",  # 対角ストライプ: 右下がり（反転）
            "foreground": "781E1E",  # 深い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E", "width": 1},  # 深い赤
    },
    "Intc (OIL)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "781E1E",  # 深い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E"},  # 深い赤
    },
    "Start Up (OIL)": {"solidFill": "781E1E"},  # 深い赤
    "Short of Tertiary (UP)": {"solidFill": "CCB333"},  # 深い黄
    "Short of Tertiary (DOWN)": {"solidFill": "334DCC"},  # 深い青紫
    "ESS Short Penalty": {
        "pattFill": {
            "preset": "openDmnd",  # 横ストライプ: 細い
            "foreground": "376092",  # 深い青紫
            "background": "FFFFFF",
        },
        "line": {"solidFill": "376092"},  # 深い青紫
    },
    "ESS Surplus Penalty": {
        "pattFill": {
            "preset": "openDmnd",  # 横ストライプ: 細い
            "foreground": "953735",  # 深い赤
            "background": "FFFFFF",
        },
        "line": {"solidFill": "953735"},  # 深い赤
    },
    "Tie Line Used Penalty": {"solidFill": "B3BEDF"},  # やや灰色い青紫
    "Tie Line Used Penalty (GF&LFC, Up)": {"solidFill": "376092"},  # 深い青紫
    "Tie Line Used Penalty (Tert, Up)": {"solidFill": "B9CDE5"},  # やや灰色い青紫
    "Tie Line Used Penalty (GF&LFC, Down)": {"solidFill": "953735"},  # 深い赤
    "Tie Line Used Penalty (Tert, Down)": {"solidFill": "E6B9B8"},  # やや灰色い赤
    "GF&LFC (Up)": {"solidFill": "376092"},  # 深い青紫
    "Tertiary (Up)": {"solidFill": "B9CDE5"},  # やや灰色い青紫
    "GF&LFC (Down)": {"solidFill": "953735"},  # 深い赤
    "Tertiary (Down)": {"solidFill": "E6B9B8"},  # やや灰色い赤
    "Forward": {"solidFill": "4F81BD"},  # 鈍い青紫
    "GF&LFC Forward": {"solidFill": "376092"},  # 深い青紫
    "Tertiary Forward": {"solidFill": "B9CDE5"},  # やや灰色い青紫
    "Counter": {"solidFill": "AA4643"},  # 深い赤
    "GF&LFC Counter": {"solidFill": "953735"},  # 深い赤
    "Tertiary Counter": {"solidFill": "E6B9B8"},  # やや灰色い赤
    "Descent": {
        "pattFill": {
            "preset": "ltHorz",  # 横ストライプ: 細い
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # 黒
    },
    "Descent (Discharge)": {
        "pattFill": {
            "preset": "ltHorz",  # 横ストライプ: 細い
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # 黒
    },
    "Descent (Charge)": {
        "pattFill": {
            "preset": "ltHorz",  # 横ストライプ: 細い
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # 黒
    },
    "Planned Outage": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
    },
    "Planned Outage (Discharge)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
    },
    "Planned Outage (Charge)": {
        "pattFill": {
            "preset": "pct75",  # 点線: 75%
            "foreground": "000000",  # 黒
            "background": "FFFFFF",
        },
    },
  }
  "line" {
    "Demand": {"line": {"solidFill": "7F7F7F"}},  # とても暗い無彩色
    "Output": {"line": {"solidFill": "5D4971", "width": 3}},  # 暗い灰みの紫
    "Max Output": {"line": {"solidFill": "376092", "width": 1.5}},  # 深い青紫
    "Max Output (Discharge)": {"line": {"solidFill": "376092", "width": 1.5}},  # 深い青紫
    "Max Output (Charge)": {"line": {"solidFill": "376092", "width": 1.5}},  # 深い青紫
    "Min Output": {"line": {"solidFill": "953735", "width": 1.5}},  # 深い赤
    "Min Output (Discharge)": {"line": {"solidFill": "953735", "width": 1.5}},  # 深い赤
    "Min Output (Charge)": {"line": {"solidFill": "953735", "width": 1.5}},  # 深い赤
    "Required": {"line": {"solidFill": "7F7F7F"}},  # とても暗い無彩色
    "Required (demand)": {"line": {"solidFill": "7F7F7F"}},  # とても暗い無彩色
    "Required (PV)": {"line": {"solidFill": "ED7D31"}},  # 明るい橙
    "Required (WF)": {"line": {"solidFill": "4472C4"}},  # 深い青紫
    "PV Net": {"line": {"solidFill": "ED7D31"}},  # 明るい橙
    "PV Output": {"line": {"solidFill": "F8CBAD"}},  # 明るい灰みの橙
    "WF Net": {"line": {"solidFill": "4472C4"}},  # 深い青紫
    "WF Output": {"line": {"solidFill": "B4C7E7"}},  # 明るい灰みの青紫
    "Reserve limit (Up)": {
        "line": {"solidFill": "376092", "width": 1.5, "dashStyle": "sysDash"}
    },  # 深い青紫
    "Reserve limit (Down)": {
        "line": {"solidFill": "953735", "width": 1.5, "dashStyle": "sysDash"}
    },  # 深い赤
    "Energy Plan": {
        "marker": {
            "symbol": "diamond",
            "size": 10,
            "spPr": {"solidFill": "5D4971", "line": {"solidFill": "5D4971"}},  # 暗い灰みの紫
        },
        "line": {"noFill": True},
    },
  }
}
```

xlsxファイル内のグラフのグラフィック要素を指定する辞書型リスト。
棒グラフと線グラフに分けて記載する。
デフォルトから変更したい要素のみ選んで記載する。

**記載例: 棒グラフ要素の"Charge of ESS"の塗りつぶしを"000000"に、枠線をなしに変更したい場合**

```yaml
graphical_prop_for_xlsx_graph:
  bar:
    "Discharge of ESS":
      solidFill: "000000"
```

または

```yaml
graphical_prop_for_xlsx_graph: {"bar": {"Discharge of ESS": {"solidFill": "000000"}}}
```

## 決定変数引き継ぎのオプション設定

#### export_inherited_vars_to_json

- **書式: ブール値**
- **デフォルト値: `False`**

クラス「UCVars」の中で、引き継ぎ対象の変数の値をjsonファイルで出力するか否かを決める変数

#### inherited_vars_dir

- **書式: 文字列**
- **デフォルト値: `"inherited-vars"`**

引き継ぎ対象の変数の値が記録されたjsonファイルを保存するディレクトリパス
