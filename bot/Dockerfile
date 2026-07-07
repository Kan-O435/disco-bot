# Python 3.13をベースイメージにする
FROM python:3.13-slim

# コンテナ内の作業ディレクトリ
WORKDIR /app

# ライブラリ一覧をコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# Botを起動
CMD ["python", "main.py"]