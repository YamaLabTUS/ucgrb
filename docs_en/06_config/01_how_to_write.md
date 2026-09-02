# How to write a configuration file

- The supported file format is [YAML](http://yaml.org/).

- When calling the function "ucgrb" or creating an instance of the class "UCData", read the file **"config.yml"** in the execution directory.

  - If you want to load a different configuration file, specify the relative path to the configuration file as the first argument when creating the instance.

    Example: You want to load the configuration file "config-test.yml"

    ```python
    ucgrb("config-test.yml")
    ```

    ~~~python
    uc_data = UCData("config-test.yml")
    ~~~
