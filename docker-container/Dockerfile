FROM python:3.11.9-slim

# パッケージインストール$
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    python3-dev python3-pip gcc libpq-dev sudo wget vim

# pipのアップグレード
RUN python3 -m pip install --upgrade pip

# アプリのディレクトリ作成
WORKDIR /var/docker-flask/flaskion
