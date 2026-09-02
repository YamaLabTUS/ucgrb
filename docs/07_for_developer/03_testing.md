# テスト実行方法

本プロジェクトでは、pytestを使用した単体テストを実施しています。

## テストディレクトリ構成

```
tests/
├── __init__.py
├── conftest.py          # pytest共通設定とフィクスチャ
├── unit/                # 単体テスト
│   ├── __init__.py
│   ├── test_gurobi_config.py          # Gurobi設定パラメータのテスト
│   ├── test_name_ascii_validation.py  # 「name」列のASCII文字チェックのテスト
│   └── ...                            # その他の単体テスト
└── integration/         # 統合テスト
    ├── __init__.py
    ├── test_data_mini_integration.py  # data-miniを使用した疎通テスト
    └── ...                            # その他の統合テスト
```

## テストの実行方法

### すべてのテストを実行

```bash
poetry run pytest tests/ -v
```

または、poethepoetタスクを使用:

```bash
poe test
```

### 特定のテストファイルを実行

```bash
# 単体テスト
poetry run pytest tests/unit/test_gurobi_config.py -v

# 統合テスト
poetry run pytest tests/integration/test_data_mini_integration.py -v
```

### カバレッジレポート付きで実行

```bash
poetry run pytest tests/ --cov=ucgrb --cov-report=html --cov-report=term
```

または、poethepoetタスクを使用:

```bash
poe test-cov
```

カバレッジレポートは `htmlcov/index.html` に生成されます。

### 特定のテストクラスまたはテスト関数を実行

```bash
# テストクラスを指定
poetry run pytest tests/unit/test_gurobi_config.py::TestGetPhysicalMemoryGB -v

# テスト関数を指定
poetry run pytest tests/unit/test_gurobi_config.py::TestGetPhysicalMemoryGB::test_get_physical_memory_gb_windows -v
```

### マーカーを使用したテストの実行

pytestマーカーを使用して、特定の種類のテストのみを実行できます。

```bash
# 単体テストのみ実行
poetry run pytest tests/ -m unit -v

# 統合テストのみ実行
poetry run pytest tests/ -m integration -v

# 実行に時間がかかるテストをスキップ
poetry run pytest tests/ -m "not slow" -v
```

## 新しいテストの追加方法

### 単体テストの追加

1. `tests/unit/` ディレクトリに新しいテストファイルを作成
2. ファイル名は `test_*.py` の形式にする
3. テストクラス名は `Test*` で始める
4. テスト関数名は `test_*` で始める
5. `@pytest.mark.unit` マーカーを追加（オプション）

例:

```python
# tests/unit/test_example.py
import pytest

@pytest.mark.unit
class TestExample:
    def test_example_function(self):
        assert True
```

### 統合テストの追加

1. `tests/integration/` ディレクトリに新しいテストファイルを作成
2. ファイル名は `test_*.py` の形式にする
3. テストクラス名は `Test*` で始める
4. テスト関数名は `test_*` で始める
5. `@pytest.mark.integration` マーカーを追加
6. 実行に時間がかかる場合は `@pytest.mark.slow` も追加

例:

```python
# tests/integration/test_example_integration.py
import pytest

@pytest.mark.integration
class TestExampleIntegration:
    @pytest.mark.slow
    def test_example_integration(self):
        # 実際のデータを使用した統合テスト
        assert True
```

## pytest設定

pytestの設定は `pyproject.toml` の `[tool.pytest.ini_options]` セクションに記載されています。

- `testpaths`: テストファイルの検索パス
- `python_files`: テストファイルの命名規則
- `python_classes`: テストクラスの命名規則
- `python_functions`: テスト関数の命名規則
- `markers`: 使用可能なマーカー
