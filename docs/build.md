# ビルド手順

必要に応じて仮想環境を作成

```bash
python3 -m venv .venv
source .venv/bin/activate
```

パッケージをインストール

```bash
pip install -r requirements.txt
```

ビルド

```bash
jupyter-book build source --path-output .
```

または

```bash
jb build source --path-output .
```