# Power system model - Minimalist model -

**[README in JP](./README.md)**

- This is a test model created to illustrate the configuration and execution of the ucgrb in the restricted license version of Gurobi Optimizer.
- This example consists of Area_A, modelled on the Tokyo area, and Area_B, modelled on the Hokkaido area. **Note that the set values and results themselves have no academic or practical implications.**
- To use the above one-year period as the delivery date, dummy data for one day each before and after the period under consideration is required. Data for March 31, 2016, and April 1, 2017, are added as dummy data.
- Data for March 31 2016 and April 1 2017 have been added as dummy data for carrying out the optimisation using the above one-year period as the delivery date.
  - demand.csv, demand_M_req.csv, PV_ACT.csv, WF_ACT.csv, and others.csv have data for April 1, 2016 as March 31, 2016 and for March 31, 2017 as April 1, 2017.
  - demand_R_GF_LFC_UP.csv、demand_R_GF_LFC_DOWN.csv、PV_R_GF_LFC_UP.csv、PV_R_GF_LFC_DOWN.csv、WF_R_GF_LFC_UP.csv、WF_R_GF_LFC_DOWN.cs have data for March as March 31, 2016 and for April as April 1, 2017.
  - Tie_calculation_section_day.csv contains data for late March weekdays as Thursday, March 31, 2016 and April holidays as April 1, 2017.
  - See chapter 5 ["How to describe power system data CSV file"](../../README_EN.md#table-of-contents) in the readme for the format of each file.

## Generation data

### Generation

Target CSV file: generation/generation.csv

- Dummy data for execution check

### Generation type

Target CSV file: generation/generation\_type.csv

- All fuels related to startup are assumed to be Fuel Oil A.
  - emission_factor_startup: See "List of Calculation Methods and Emission Factors in the Calculation, Reporting, and Publication System" [itiran_2020_rev.pdf](https://ghg-santeikohyo.env.go.jp/files/calc/itiran_2020_rev.pdf) from the Ministry of the Environment website ["List of Calculation Methods and Emission Factors"](https://ghg-santeikohyo.env.go.jp/calc)
  - fuel_price_startup: Calculate the average price difference between crude oil and Fuel Oil A from January 2014 to December 2020 (38.29 [thousand yen/kl]) by referring to ["Crude Oil Price and Fuel Oil A Price Trends"](https://www.maff.go.jp/tokai/seisan/kankyo/ondanka/attach/pdf/index-7.pdf) on [the Tokai Agricultural Administration Bureau](https://www.maff.go.jp/tokai/index.html) website.

### Energy storage system

Target CSV file: ESS/ESS.csv

- C_ess_short and C_ess_surplus are set to 10,000 thousand yen/KWh, one digit less than C_short and C_surplus

## Area data

### Area

Target CSV file: area.csv

- Dummy data for execution check

## Tie line data

### Tie line

Target CSV file: tie/tie.csv

- Dummy data for execution check

## Time series data

### Electricity demand

Target CSV file: demand/demand.csv

- Dummy data for execution check

### Electricity demand short cycle (GF&LFC Component) variation forecast error rate

Target CSV file: demand/demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv

- Fixed at 2%.

### Minimum requirement of system inertia in unit

Target CSV file: demand/demand_M_req.csv

- Fixed at 0 MW-s/MVA.

### Actual value of PV output

Target CSV file: PV/PV_ACT.csv

- Dummy data for execution check

### PV short-period (GF&LFC component) variability forecast error rate

Target CSV file: PV/PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv

- Fixed at 10%.

### Actual value of WF output

Target CSV file: WF/WF_ACT.csv

- Dummy data for execution check

### WF short-period (GF&LFC component) variability forecast error rate

Target CSV file: WF/WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv

- Fixed at 10%.

### Output values of other power generation facilities

Target CSV file: others.csv

- Appropriate output values for run-of-river hydro and geothermal generation each area.
