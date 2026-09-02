# How to write power system data into CSV files

- As examples of the sets of power system data, [data-example](../../data_set/data-example/) and [data-mini](../../data_set/data-mini/) are provided.

## How to handle data in the program

- When an instance of class "UCData" is created, the power system model data is stored in attribute "power_system". The CSV file name becomes the attribute name belonging to "power_system", and the tables in the CSV file are imported in DataFrame format in the python package "pandas" as attribute values.
- The import target is a CSV file in the directory specified by the "csv_data_dir" configuration value.


## Regarding directory structure

- Further directories may be created within the target directory and CSV files may be placed together. In this case, the directory name may not be reflected in the attribute names of the imported data.
- If a CSV file name begins with an underscore "_", the file is not eligible for import.
- If there are two consecutive underscores "__" in the middle of a CSV file name, the entry characters after the two consecutive underscores are ignored, and the entry characters before the two consecutive underscores become the attribute name.
- If there are multiple CSV files with the same attribute name because they are located in different directories or use double underscores, the DataFrames generated from each CSV table will be combined and recorded as a single attribute.


## Regarding data validation

- For columns named "name", only ASCII characters (alphanumeric characters and symbols) are allowed. If non-ASCII characters such as Japanese are included, a validation error will occur during CSV file reading.
- When the validation error occurs, the name of the CSV file, the column name and the invalid values (with the row numbers in that file) are displayed.

## Regarding time series data

A CSV file with one row, column A, as "time" is treated as time series data.

- Column A is the target time for the values in column B and after, expressed in Hour End notation, where a day is represented as 1:00 to 0:00.
  - Example 1: "2040/8/2 1:00:00" means 2040/8/2 0:00 to 1:00.
  - Example 2: "2040/8/3 0:00:00" refers to the period from 2040/8/2 23:00 to 8/3 0:00. **Note that the data for 8/3 0:00:00 refers to 8/2.**
