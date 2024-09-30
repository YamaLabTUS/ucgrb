# Output MPS files, Execute in other solvers

If you do not have a paid license for Gurobi Optimizer but still want to solve a large problem, you can output the MILP problem to an MPS file and solve it with another solver.

As an example, the procedure is shown for the Python package [PuLP](https://pypi.org/project/PuLP/) and the open source [MILP](https://github.com/coin-or/Cbc) solver CBC.

1. Set `export_mps_file: True` in the configuration file to output MPS files. See [Execution methods - If you have a Gurobi Optimizer license -](../03_01_run_with_licence/01_run.md) and [Setting file examples Example 11: MPS file output](../03_01_run_with_licence/02_example.md#example-11-mps-file-output),

2. Perform ucgrb. If you do not have a paid version license, the following error message will be output.

   ```cmd
   gurobipy.GurobiError: Model too large for size-limited license; visit https://www.gurobi.com/free-trial for a full license
   ```

3.	Even if it is an error, a result directory is generated. In the directory "MPS" in the result directory, a file "mps.zip" is output, which is a text file in MPS format compressed in zip format.

   - Only the optimization problems that were scheduled to be performed at the beginning of the rolling optimization are saved as mps.zip files, since the optimization is not performed due to errors caused by lack of licenses.

   - When performed with the configuration file in [Setting file examples Example 11: MPS file output](../03_01_run_with_licence/02_example.md#example-11-mps-file-output), the April 1, 2016 day-ahead scheduling optimization problem is output with the file name "2016-04-01_day-ahead_scheduling.mps.zip".

4.	Create a virtual environment (pyenv) with PuLP installed.

5. Download the CBC onto a computer and store it in a specific location.

   - CBC Releases archived at: https://github.com/coin-or/Cbc/releases

   - In this example, the file is saved in "C:\Program Files\cbc".

6. Unzip the mps.zip file whose existence was confirmed in step 3, convert it to an MPS file, and save it in a specific directory.

   - In this example, the file is saved with the file name "2016-04-01_scheduling.mps".

7. Create the following source code "mps.py" in the same directory as the MPS file and implement it in the virtual environment created in step 4.

   **mps.py**

   ```python
   import pulp

   # MPS file path
   MPS_PATH = "2016-04-01_scheduling.mps"

   # CBC Solver Path
   CBC_PATH = r"C:\Program Files\cbc\bin\cbc.exe"

   # Defining the Problem with PuLP
   var, prob = pulp.LpProblem.fromMPS(MPS_PATH)

   # Performing optimization with solvers
   prob.solve(pulp.apis.COIN_CMD(path=CBC_PATH))

   # Output Results
   print("Status:", pulp.LpStatus[prob.status])
   if prob.status == pulp.constants.LpStatusOptimal:
       print("Objective Value:", pulp.value(prob.objective))

   ```
