# Power system model - Test model -

**[README in JP](./README.md)**

- This is a test model created to illustrate the configuration and execution of the ucgrb.
- This example consists of "Area_A" with the scale of the Tokyo area multiplied by about 0.1 and "Area_B" with the scale of the Hokkaido area multiplied by about 0.3. **Note that the set values and results themselves have no academic or practical implications..**
- To use the above one-year period as the delivery date, dummy data for one day each before and after the period under consideration is required. Data for March 31, 2016, and April 1, 2017, are added as dummy data.
- Data for March 31, 2016 and April 1, 2017 are added as dummy data to perform the optimization with the above one-year period as the delivery date.
  - demand.csv, demand_M_req.csv, PV_ACT.csv, PV_FCST_U.csv, PV_FCST_M.csv, PV_FCST_L.csv, WF_ACT.csv, WF_FCST_U.csv, WF_FCST_M.csv, WF_FCST_L. csv, and others.csv contain data for April 1, 2016 as March 31, 2016, and for March 31, 2017 as April 1, 2017.
  - demand_R_GF_LFC_UP.csv、demand_R_GF_LFC_DOWN.csv、PV_R_GF_LFC_UP.csv、PV_R_GF_LFC_DOWN.csv、WF_R_GF_LFC_UP.csv、WF_R_GF_LFC_DOWN.csv contain data for March as March 31, 2016 and April as April 1, 2017.
  - Tie_calculation_section_day.csv contains data for late March weekdays as March 31, 2016 and April holidays as April 1, 2017.
  - See chapter 5 ["How to describe power system data CSV file"](../../README_EN.md#table-of-contents) in the readme for the format of each file.

## Generation data

### Generation

Target CSV file: generation/generation__01_thermal.csv, generation/generation__02_nuclear.csv,  generation/generation__03_hydro.csv

- The csv files are placed in the directory "generation".
- The data regarding generation are separated into three files: "thermal," "nuclear," and "hydro."
- COAL, OIL, and GAS Generators are listed in "thermal."

### Generation type

Target CSV file: generation/generation\_type.csv,

- All fuels related to startup are assumed to be Fuel Oil A.
  - emission_factor_startup: See "List of Calculation Methods and Emission Factors in the Calculation, Reporting, and Publication System" [itiran_2020_rev.pdf](https://ghg-santeikohyo.env.go.jp/files/calc/itiran_2020_rev.pdf) from the Ministry of the Environment website ["List of Calculation Methods and Emission Factors"](https://ghg-santeikohyo.env.go.jp/calc)
  - fuel_price_startup: Calculate the average price difference between crude oil and Fuel Oil A from January 2014 to December 2020 (38.29 [thousand yen/kl]) by referring to ["Crude Oil Price and Fuel Oil A Price Trends"](https://www.maff.go.jp/tokai/seisan/kankyo/ondanka/attach/pdf/index-7.pdf) on [the Tokai Agricultural Administration Bureau](https://www.maff.go.jp/tokai/index.html) website.

### Energy storage system

Target CSV file: ESS/ESS.csv

- C_ess_short and C_ess_surplus are set to 10,000 thousand Yen/KWh, one digit less than C_short and C_surplus.

### Planned outage

Target CSV file: planned_outage.csv

- Dummy data for execution check

### Output Descent

Target CSV file: descent.csv

- Dummy data for execution check

## Area data

### Area

Target CSV file: area

- Dummy data for execution check

## Tie line data

### Tie line

Target CSV file: tie/tie.csv

- Name of the tie line and the connection relationship


### Tie line operation

Target CSV file: CSV file in the directory "tie/season/operation"

- The CSV file is divided into directories for each of the four time periods and further divided into CSV files for each tie line.

## Time series data

### Electricity demand

Target CSV file: demand/demand.csv

- The electricity demand data of Area_A and Area_B are fictional data but are significantly revised data from Tokyo Electric Power Company and Hokkaido Electric Power Company, respectively.



### Electricity demand short cycle (GF&LFC Component) variation forecast error rate

Target CSV file: demand/demand_R_GF_LFC_UP.csv, demand_R_GF_LFC_DOWN.csv

- A forecast error rate of variation of electricity demand for each area in a short period (GF&LFC component).
- Fixed at 2%.

### Minimum requirement of system inertia in unit

Target CSV file: demand/demand_M_req.csv

- The minimum requirement of system inertia in unit for each area.
- Fixed at 0 MW-s/MVA.

### Actual value of PV output

Target CSV file: PV/PV_ACT.csv

### Forecasted upper bound of PV output

Target CSV file: PV/PV_FCST_U.csv

### Forecasted PV output

Target CSV file: PV/PV_FCST_M.csv

### Forecasted lower bound of PV output

Target CSV file: PV/PV_FCST_L.csv

### PV short-period (GF&LFC component) variability forecast error rate

Target CSV file: PV/PV_R_GF_LFC_UP.csv, PV_R_GF_LFC_DOWN.csv

- Fixed at 10%.

### Actual value of WF output

Target CSV file: WF/WF_ACT.csv

### Forecasted upper bound of WF output

Target CSV file: WF/WF_FCST_U.csv

### Forecasted WF output

Target CSV file: WF/WF_FCST_M.csv

### Forecasted lower bound of WF output

Target CSV file: WF/WF_FCST_L.csv

### WF short-period (GF&LFC component) variability forecast error rate

Target CSV file: WF/WF_R_GF_LFC_UP.csv, WF_R_GF_LFC_DOWN.csv

- Fixed at 10%.

### Total transmission capacity and margin of tie lines

Target CSV file: tie/timeline/TTC_forward.csv, TTC_counter.csv, Margin_forward.csv, Margin_counter

- Appropriate values are entered, and the values themselves have no particular meaning.

### Maximum interchange flexibility

Target CSV file: tie/timeline/ GF_LFC_UP_forward_MAX.csv, GF_LFC_UP_counter_MAX.csv, GF_LFC_DOWN_forward_MAX.csv, GF_LFC_DOWN_counter_MAX.csv, Tert_UP_forward_MAX.csv, Tert_UP_counter_MAX.csv, Tert_DOWN_forward_MAX.csv, Tert_DOWN_counter_MAX.csv


- Appropriate values are entered, and the values themselves have no particular meaning.


### Definition of day/night/seasonal time periods for total transmission capacity and margin

Target CSV file: tie/season/tie_calculation_section_day.csv, tie_calculation_section_of_the_clock.csv,

- Daytime hours are defined as "8 to 10 p.m." and the rest as nighttime.
- As the period division to be entered in month_section, 15 period divisions are used, dividing the year into 12 months and September, November, and March in two. The three-letter abbreviations of the months ("Jan", "Feb"...) are used as the basis. The three-letter abbreviations for the months of September, November, and March ("\_1st" and "\_2nd" as suffixes ("Sep_1st", "Sep_2nd", "Nov_1st", "Nov_2nd", "Mar_1st", "Mar_2nd") are used to separate the first and second halves of the year.[^1]

[^1]: See page 8 of the document ["Review and Validation of the Calculation Methodology for Total Transmission Capacity"](https://www.occto.or.jp/renkeisenriyou/oshirase/2015/files/02_unyouyouryou_sansyutsuhouhou.pdf) by the Office for Promotion of Wide-Area Operations of Electricity (OCCTO).

### Scheduled energy storage operation of ESS
Target CSV file: ESS/E_R_plan.csv

- Assuming weekly operation, the following values are used.
  - Monday at 0:00   : 90%
  - Tuesday at 0:00  : 74%
  - Wednesday at 0:00: 58%
  - Thursday at 0:00 : 42%
  - Friday at 0:00   : 26%
  - Saturday at 0:00 : 10%
  - Sunday at 0:00   : 50%


### Maximum daily energy from a generator

Target CSV file: generation/E_1_day_MAX.csv

- Set maximum daily energy of hydro generation.

### Output values of other power generation facilities

Target CSV file: others.csv

- Dummy data of output of run-of-river hydro and geothermal generation in each area.
