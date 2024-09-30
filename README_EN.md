# ucgrb

**[README in JP](README.md)**

This Python package can perform unit commitment (UC) optimization for multi-area power systems connected by tie lines using Gurobi Optimizer.


## Table of contents

1. [Feature](docs_en/01_feature.md)
2. [Requirement](docs_en/02_requirement.md)
3. Execution methods and examples
   1. If you have a Gurobi Optimizer license
      1. [Execution method](docs_en/03_01_run_with_licence/01_run.md)
      2. [Setting file examples](docs_en/03_01_run_with_licence/02_example.md)
   2. If you don't have a Gurobi Optimizer license
      1. [Execute on a small model](docs_en/03_02_run_without_licence/01_run.md)
      2. [Output MPS files, Execute in other solvers](docs_en/03_02_run_without_licence/02_mps.md)
4. Formulation of the optimization problem
   1. [Objective function](docs_en/04_formulation/01_objective_function.md)
   2. Constraints
      1. [Constraints on area](docs_en/04_formulation/02_constraint/01_area.md)
      2. [Constraints on large-scale power generation](docs_en/04_formulation/02_constraint/02_generation.md)
      3. [Constraints on renewable energy](docs_en/04_formulation/02_constraint/03_re.md)
      4. [Constraints on energy storage system](docs_en/04_formulation/02_constraint/04_ess.md)
      5. [Constraints on tie line](docs_en/04_formulation/02_constraint/05_tie.md)
      6. [Constraints on rolling optimization](docs_en/04_formulation/02_constraint/06_inheritance.md)
   3. [Sets and indies](docs_en/04_formulation/03_set_and_index.md)
   4. Parameters
      1. [Parameters for area](docs_en/04_formulation/04_parameter/01_area.md)
      2. [Parameters for large-scale　power generation](docs_en/04_formulation/04_parameter/02_generator.md)
      3. [Parameters for renewable energy](docs_en/04_formulation/04_parameter/03_re.md)
      4. [Parameters for energy storage system](docs_en/04_formulation/04_parameter/04_ess.md)
      5. [Parameters for tie line](docs_en/04_formulation/04_parameter/05_tie.md)
      6. [Parameters that depends on scheduling kind](docs_en/04_formulation/04_parameter/06_depend_on_scheduling_kind.md)
   5. Variables
      1. [Variables for area](docs_en/04_formulation/05_variable/01_area.md)
      2. [Variables for large-scale　power generation](docs_en/04_formulation/05_variable/02_geneation.md)
      3. [Variables for renewable energy](docs_en/04_formulation/05_variable/03_re.md)
      4. [Variables for energy storage system](docs_en/04_formulation/05_variable/04_ess.md)
      5. [Variables for tie line](docs_en/04_formulation/05_variable/05_tie.md)
   6. Appendix
      1. [Fuel cost function coefficient calculation method for nuclear and thermal generators](docs_en/04_formulation/06_appendix/01_fuel_cost.md)
      2. [Maximum and minimum output calculation method for nuclear and thermal generators](docs_en/04_formulation/06_appendix/02_max_min_output.md)
      3. [CO<sub>2</sub> emission calculation method for nuclear and thermal generators](docs_en/04_formulation/06_appendix/03_emission.md)
5. How to describe power system data CSV file
   1. [Overview](docs_en/05_csvfile/01_about.md)
   2. [Generation data](docs_en/05_csvfile/02_generation.md)
   3. [Area data](docs_en/05_csvfile/03_area.md)
   4. [Tie line data](docs_en/05_csvfile/04_tie.md)
   5. [Timeline data](docs_en/05_csvfile/05_timeline.md)
6. List of setting values
   1. [How to describe a configuration file](docs_en/06_config/01_how_to_write.md)
   2. [Optional settings for input data and solver](docs_en/06_config/02_input_data_and_solver.md)
   3. [Unit commitment problem settings](docs_en/06_config/03_unit_commitment.md)
   4. [Rolling optimized list settings](docs_en/06_config/04_rolling_optimization_list.md)
   5. [Result output settings](docs_en/06_config/05_result_output.md)
7. For Developers
   1. [Settings values for developers](docs_en/07_for_developer/01_config_setting.md)
   2. [About automatic formatting](docs_en/07_for_developer/02_formatter.md)


## License

[MIT License](LICENSE)
