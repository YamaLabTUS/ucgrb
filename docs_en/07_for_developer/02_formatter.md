# Regarding automatic formatting

Use "isort" and "Black" for formatting and checking source code.
- isort is a package that can sort imported sentences alphabetically or automatically by section or type.
- Black is one of the Python code formatters. It has the distinction of imposing stricter rules than other formatters.
- Various settings are described in [pyproject.toml](../../pyproject.toml).

## Manual formatting method on command line

1. Install the package "[Poe the Poet](https://poethepoet.natn.io/index.html)" in the Windows Python environment (not in the virtual environment).
  - "Poe the Poet" is a package that allows you to run task runners with poetry.
  - The most recommended installation method is to install "[pipx](https://github.com/pypa/pipx)" on Windows and then enter the following command:
       ```cmd
       pipx install poethepoet
       ```
2. Execute the following command lines to perform various formatting.

- isort
    ```cmd
    poe isort
    ```
- Black
    ```cmd
    poe black
    ```
## Automatic formatting method in VScode
- By installing the following extensions listed in [.vscode/extensions.json](../../.vscode/extensions.json) to VScode, files will be automatically formatted when saved.
    - [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
    - [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- Settings for automatic formatting in VScode are described in [.vscode/settings.json](../../.vscode/settings.json).
- You need to specify the Python virtual environment to be used in the workspace to the environment (.venv) created in ucgrb.
  - Open the command palette (Windows: `Ctrl`+`shift`+`P`) and select the appropriate path from `Python Select Interpreter`.

> **Note (when using Cursor)**: In Cursor, instead of Pylance (`ms-python.vscode-pylance`), Cursor's own language server extension `anysphere.cursorpyright` is used. Because this extension automatically sets `python.languageServer` to `"None"`, it is normal for that value in `.vscode/settings.json` to be `"None"`, and completion and type checking are provided by Cursor Pyright. Even if you manually change it back to `"Pylance"`, Cursor rewrites it to `"None"` again. This does not affect the behavior of automatic formatting by isort / Black Formatter.
>
> For this reason, in Cursor `.vscode/settings.json` keeps showing up as a `git` diff every time. If you want to keep the shared tracked version (`"Pylance"`) while ignoring your local rewrites, run the following in your own environment (this setting is local only and does not propagate to other members).
>
> ```bash
> # Make git ignore local changes
> git update-index --skip-worktree .vscode/settings.json
> # Undo and return to normal tracking
> git update-index --no-skip-worktree .vscode/settings.json
> ```

## Notes when using a directory above this repository (ucgrb) as workspace
The above execution method is for when this repository (ucgrb) itself is used as the workspace. For example, in "[How to Run - When you have a Gurobi Optimizer commercial license -](../03_01_run_with_licence/01_run.md)", main.py is created in a directory above this repository (ucgrb), so the workspace may be in the upper directory. In this case, the following points should be noted.

### Manual formatting method on command line
- You need to use the `cd` command to move to this repository (ucgrb) before executing the commands.

### Automatic formatting method in VScode
- You need to copy the directory [ucgrb/.vscode](../../.vscode) and paste it into the workspace directory.
- You need to specify the Python virtual environment to be used in the workspace to the environment (.venv) created in this repository (ucgrb).
