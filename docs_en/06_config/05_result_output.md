# Result output settings

## Setting Options for Result Output

### result_dir

- **Type: String**
- **default value: `"result"`**

Directory path to save optimization results

### export_mps_file

- **Type: Boolean**
- **default value: `False`**

A variable that determines whether or not to save the formulation of each optimization problem in MPS file format.

URL for reference: [MPS format](https://www.gurobi.com/documentation/9.5/refman/mps_format.html)

### export_json_file

- **Type: Boolean**
- **default value: `True`**

A variable that determines whether or not to save each optimization result and the shadow price of each constraint in JSON file format.

URL for reference: [JSON solution format](https://www.gurobi.com/documentation/9.5/refman/json_solution_format.html)

### export_xlsx_file

- **Type: Boolean or dictionary type**
- **default value: `{"shadow_price": True, "generation": False,"ESS": False, "tie": True}`**

This variable determines whether or not to save the optimization results in an xlsx file in the function "make_grb_model".

A sheet "total" for the total results for all areas, and another sheet for the results for each area are output.

Optionally, the following sheets can also be output, and whether or not to output them can be configured using dictionary type.

- **shadow_price**: A sheet recording the time series of shadow prices of the constraints set for each area is output.
- **generation**: A sheet is output that records the time series of power generation and reserve power secured by each large-scale generator installed in each area.
- **ESS**: A sheet that records the time series of recharge/discharge and secured reserve power for each ESS installed in each area is output.
- **tie**: A sheet is output that records the time series of the power interchange of the tie lines.

If the value is False, the xlsx file itself is not output. If there is no description for each sheet, the output is based on the dictionary type of default value.

**Example: You want to output a large generator and an ESS sheet**

```yaml
export_xlsx_file:
    generation: True
    ESS: True
```

or

```yaml
export_xlsx_file: {"generation": True, "ESS": True}
```

### graphical_prop_for_xlsx_graph

- **Type: dictionary**
- **default value:**

```yaml
{
  "bar": {
    "Others": {"solidFill": "4F6228", "line": {"solidFill": "4F6228", "width": 1.5}},  # Dark yellowish green
    "HYDRO": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "558ED5",  # dull bluish purple
            "background": "FFFFFF",
        },
        "line": {"solidFill": "558ED5", "width": 1.5},  # dull bluish purple
    },
    "NUCL": {
        "pattFill": {
            "preset": "smGrid",  # small grid
            "foreground": "002060",  # Bright blue-purple
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060", "width": 1},  # Bright blue-purple
    },
    "COAL": {
        "pattFill": {
            "preset": "dkVert",  # dark vertical stripes
            "foreground": "583822",  # Deep orange
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822", "width": 1},  # Deep orange
    },
    "GAS": {
        "pattFill": {
            "preset": "pct20",  # 20%
            "foreground": "C0504D",  # Dull red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D", "width": 1},  # Dull red
    },
    "OIL": {
        "pattFill": {
            "preset": "dkDnDiag",  # diagonal stripes: down-right (inverted)
            "foreground": "781E1E",  # Deep red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E", "width": 1},  # Deep red
    },
    "Charge of ESS": {
        "solidFill": "FFFF00",  # Bright yellow
        "line": {"solidFill": "C0504D", "width": 1},  # Dull red
    },
    "Discharge of ESS": {
        "solidFill": "FFFF00",  # Bright yellow
        "line": {"solidFill": "4F81BD", "width": 1},  # Dull blue-purple
    },
    "ESS": {
        "solidFill": "FFFF00",  # Bright yellow
        "line": {"solidFill": "BBBF4D", "width": 1},  # Dull yellow-green
    },
    "PV": {"solidFill": "ED7D31"},  # Light orange
    "WF": {"solidFill": "4472C4"},  # Deep blue-violet
    "Suppression of PV": {"solidFill": "F8CBAD"},  # Light grayish orange
    "Suppression of WF": {"solidFill": "B4C7E7"},  # Light grayish blue-purple
    "Outflow by tie": {
        "noFill": True,
        "line": {"solidFill": "C0504D", "width": 1.5, "dashStyle": "sysDash"},  # Dull red
    },
    "Inflow by tie": {
        "noFill": True,
        "line": {"solidFill": "4F81BD", "width": 1.5, "dashStyle": "sysDash"},  # Dull blue-purple
    },
    "Short": {"solidFill": "FF0000"},  # Bright red
    "Surplus": {"solidFill": "CCA3A3"},  # Slightly grayish red
    "Coef (NUCL)": {
        "pattFill": {
            "preset": "smGrid",  # small grid
            "foreground": "002060",  # Bright blue-purple
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060", "width": 1},  # Bright blue-purple
    },
    "Intc (NUCL)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "002060",  # Bright blue-purple
            "background": "FFFFFF",
        },
        "line": {"solidFill": "002060"},  # Bright blue-purple
    },
    "Start Up (NUCL)": {"solidFill": "002060"},  # Bright blue-purple
    "Coef (COAL)": {
        "pattFill": {
            "preset": "dkVert",  # dark vertical stripes
            "foreground": "583822",  # Deep orange
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822", "width": 1},  # Deep orange
    },
    "Intc (COAL)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "583822",  # Deep orange
            "background": "FFFFFF",
        },
        "line": {"solidFill": "583822"},  # Deep orange
    },
    "Start Up (COAL)": {"solidFill": "583822"},  # Deep orange
    "Coef (GAS)": {
        "pattFill": {
            "preset": "pct20",  # 20%
            "foreground": "C0504D",  # Dull red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D", "width": 1},  # Dull red
    },
    "Intc (GAS)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "C0504D",  # Dull red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "C0504D"},  # Dull red
    },
    "Start Up (GAS)": {"solidFill": "C0504D"},  # Dull red
    "Coef (OIL)": {
        "pattFill": {
            "preset": "dkDnDiag",  # diagonal stripes: down-right (inverted)
            "foreground": "781E1E",  # Deep red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E", "width": 1},  # Deep red
    },
    "Intc (OIL)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "781E1E",  # Deep red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "781E1E"},  # Deep red
    },
    "Start Up (OIL)": {"solidFill": "781E1E"},  # Deep red
    "Short of Tertiary (UP)": {"solidFill": "CCB333"},  # Deep yellow
    "Short of Tertiary (DOWN)": {"solidFill": "334DCC"},  # Deep blue-violet
    "ESS Short Penalty": {
        "pattFill": {
            "preset": "openDmnd",  # thin horizontal stripes
            "foreground": "376092",  # Deep blue-violet
            "background": "FFFFFF",
        },
        "line": {"solidFill": "376092"},  # Deep blue-violet
    },
    "ESS Surplus Penalty": {
        "pattFill": {
            "preset": "openDmnd",  # thin horizontal stripes
            "foreground": "953735",  # Deep red
            "background": "FFFFFF",
        },
        "line": {"solidFill": "953735"},  # Deep red
    },
    "Tie Line Used Penalty": {"solidFill": "B3BEDF"},  # Slightly grayish blue-purple
    "Tie Line Used Penalty (GF&LFC, Up)": {"solidFill": "376092"},  # Deep blue-violet
    "Tie Line Used Penalty (Tert, Up)": {"solidFill": "B9CDE5"},  # Slightly grayish blue-purple
    "Tie Line Used Penalty (GF&LFC, Down)": {"solidFill": "953735"},  # Deep red
    "Tie Line Used Penalty (Tert, Down)": {"solidFill": "E6B9B8"},  # Slightly grayish red
    "GF&LFC (Up)": {"solidFill": "376092"},  # Deep blue-violet
    "Tertiary (Up)": {"solidFill": "B9CDE5"},  # Slightly grayish blue-purple
    "GF&LFC (Down)": {"solidFill": "953735"},  # Deep red
    "Tertiary (Down)": {"solidFill": "E6B9B8"},  # Slightly grayish red
    "Forward": {"solidFill": "4F81BD"},  # Dull blue-purple
    "GF&LFC Forward": {"solidFill": "376092"},  # Deep blue-violet
    "Tertiary Forward": {"solidFill": "B9CDE5"},  # Slightly grayish blue-purple
    "Counter": {"solidFill": "AA4643"},  # Deep red
    "GF&LFC Counter": {"solidFill": "953735"},  # Deep red
    "Tertiary Counter": {"solidFill": "E6B9B8"},  # Slightly grayish red
    "Descent": {
        "pattFill": {
            "preset": "ltHorz",  # thin horizontal stripes
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # Black
    },
    "Descent (Discharge)": {
        "pattFill": {
            "preset": "ltHorz",  # thin horizontal stripes
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # Black
    },
    "Descent (Charge)": {
        "pattFill": {
            "preset": "ltHorz",  # thin horizontal stripes
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
        "line": {"solidFill": "000000"},  # Black
    },
    "Planned Outage": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
    },
    "Planned Outage (Discharge)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
    },
    "Planned Outage (Charge)": {
        "pattFill": {
            "preset": "pct75",  # 75%
            "foreground": "000000",  # Black
            "background": "FFFFFF",
        },
    },
  },
  "line": {
    "Demand": {"line": {"solidFill": "7F7F7F"}},  # Very dark achromatic color
    "Output": {"line": {"solidFill": "5D4971", "width": 3}},  # Dark grayish purple
    "Max Output": {"line": {"solidFill": "376092", "width": 1.5}},  # Deep blue-purple
    "Max Output (Discharge)": {"line": {"solidFill": "376092", "width": 1.5}},  # Deep blue-purple
    "Max Output (Charge)": {"line": {"solidFill": "376092", "width": 1.5}},  # Deep blue-purple
    "Min Output": {"line": {"solidFill": "953735", "width": 1.5}},  # Deep red
    "Min Output (Discharge)": {"line": {"solidFill": "953735", "width": 1.5}},  # Deep red
    "Min Output (Charge)": {"line": {"solidFill": "953735", "width": 1.5}},  # Deep red
    "Required": {"line": {"solidFill": "7F7F7F"}},  # Very dark achromatic color
    "Required (demand)": {"line": {"solidFill": "7F7F7F"}},  # Very dark achromatic color
    "Required (PV)": {"line": {"solidFill": "ED7D31"}},  # Light orange
    "Required (WF)": {"line": {"solidFill": "4472C4"}},  # Deep blue-purple
    "PV Net": {"line": {"solidFill": "ED7D31"}},  # Light orange
    "PV Output": {"line": {"solidFill": "F8CBAD"}},  # Light grayish orange
    "WF Net": {"line": {"solidFill": "4472C4"}},  # Deep blue-purple
    "WF Output": {"line": {"solidFill": "B4C7E7"}},  # Light grayish blue-purple
    "Reserve limit (Up)": {
        "line": {"solidFill": "376092", "width": 1.5, "dashStyle": "sysDash"}
    },  # Deep blue-purple
    "Reserve limit (Down)": {
        "line": {"solidFill": "953735", "width": 1.5, "dashStyle": "sysDash"}
    },  # Deep red
    "Energy Plan": {
        "marker": {
            "symbol": "diamond",
            "size": 10,
            "spPr": {"solidFill": "5D4971", "line": {"solidFill": "5D4971"}},  # Dark grayish purple
        },
        "line": {"noFill": True},
    },
  }
}
```

Dictionary type list that specifies graphic elements of graphs in xlsx files.
Described separately for bar graphs and line graphs.
Only list the elements you want to change from the default.

**Example: When you want to change the fill of the bar graph element "Charge of ESS" to "000000" and remove the border line**

```yaml
graphical_prop_for_xlsx_graph:
  bar:
    "Discharge of ESS":
      solidFill: "000000"
```

or

```yaml
graphical_prop_for_xlsx_graph: {"bar": {"Discharge of ESS": {"solidFill": "000000"}}}
```

## Option settings for inheriting decision variables

#### export_inherited_vars_to_json

- **Type: Boolean**
- **default value: `False`**

Variable that determines whether or not to output the values of variables to be inherited in json file in the class "UCVars"

#### inherited_vars_dir

- **Type: String**
- **default value: `"inherited-vars"`**

Directory path to save json files containing the values of variables to be inherited
