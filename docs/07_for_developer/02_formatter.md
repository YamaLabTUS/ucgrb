# 自動整形に関して

ソースコードの書式整形・チェックに「isort」「Black」を使用する。
- isortは、インポート文をアルファベット順に並べたり、セクションや種類ごとに自動分類したりすることができるパッケージである。
- BlackはPythonコードフォーマッターの一つである。他のフォーマッターよりも厳しいルールを課しているという特徴がある。
- 各種設定は[pyproject.toml](../../pyproject.toml)に記載されている。

## コマンドライン上での手動整形方法

1. (仮想環境上ではなく)windowsのpython環境上にパッケージ「[Poe the Poet](https://poethepoet.natn.io/index.html)」をインストールする。
  - 「Poe the Poet」はpoetryでタスクランナーを実行することができるようになるパッケージである。
  - 最も推奨されるインストール方法はwindowsに「[pipx](https://github.com/pypa/pipx)」をインストールしてから、以下のコマンドを入力する方法である。
       ```cmd
       pipx install poethepoet
       ```
2. 以下のコマンドラインを実行することで、各種整形が実行される。

- isort
    ```cmd
    poe isort
    ```
- Black
    ```cmd
    poe black
    ```
## VScode上での自動整形方法
- [.vscode/extensions.json](../../.vscode/extensions.json)に記載されている以下のエクステンションをVScodeにインストールすることで、ファイルセーブ時に自動的に整形されるようになる。
    - [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
    - [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- VScode上の自動整形に関する設定は[.vscode/settings.json](../../.vscode/settings.json)に記載されている
- ワークスペース内で使うPythonの仮想環境を、ucgrb内で作成された環境(.venv)に指定する必要がある。
  - コマンドパレット(Windows: `Ctrl`+`shift`+`P`)を開き、`Python Select Interpreter`から適切なパスを選択する。

> **補足（Cursor を使う場合）**: Cursor では Pylance（`ms-python.vscode-pylance`）の代わりに Cursor 独自の言語サーバー拡張 `anysphere.cursorpyright` が使われる。この拡張が `python.languageServer` を自動的に `"None"` に設定するため、`.vscode/settings.json` の当該値が `"None"` になっていても正常であり、補完・型チェックは Cursor Pyright が提供する。手動で `"Pylance"` に戻しても Cursor が再度 `"None"` に書き戻す。isort / Black Formatter による自動整形の動作には影響しない。
>
> このため Cursor では `.vscode/settings.json` が毎回 `git` の差分として出続ける。共有される追跡版（`"Pylance"`）を保ちつつローカルの書き換えを無視したい場合は、各自の環境で以下を実行する（この設定はローカルのみで他メンバーには伝播しない）。
>
> ```bash
> # ローカルの変更を git に無視させる
> git update-index --skip-worktree .vscode/settings.json
> # 解除して通常の追跡に戻す
> git update-index --no-skip-worktree .vscode/settings.json
> ```

## 本リポジトリ(ucgrb)より上のディレクトリをワークスペースとしている場合の注意点
上記の実行方法は、本リポジトリ(ucgrb)そのものをワークスペースとしている場合の実行方法である。例えば、「[実行方法 - Gurobi Optimizer有償版ライセンスがある場合 -](../03_01_run_with_licence/01_run.md)」では、本リポジトリ(ucgrb)より上のディレクトリでmain.pyを作成しているため、ワークスペースが上のディレクトリとなる可能性がある。その際には、以下の点を注意する必要がある。

### コマンドライン上での手動整形方法
- `cd`コマンドを利用して、本リポジトリ(ucgrb)に移動してから、コマンドを実行する必要がある。

### VScode上での自動整形方法
- ディレクトリ[ucgrb/.vscode](../../.vscode)をコピーして、ワークスペースのディレクトリにペーストする必要がある。
- ワークスペース内で使うPythonの仮想環境を、本リポジトリ(ucgrb)内で作成された環境(.venv)に指定する必要がある。

