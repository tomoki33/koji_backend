FROM public.ecr.aws/lambda/python:3.11 AS builder
# Python3.11と開発ツールインストール
RUN yum -y install \
    python3 \
    python3-devel \
    gcc \
    gcc-c++ \
    make \
    zip \
    openssl-devel \
    libffi-devel \
    rust \
    cargo \
    && yum clean all

# pip最新版をインストール
RUN python3 -m ensurepip && pip3 install --upgrade pip

# 作業ディレクトリ
WORKDIR /lambda-layer

# requirements.txt をコピー
COPY requirements.txt .

# Pythonパッケージを Amazon Linux 環境でビルド
RUN pip3 install --target python -r requirements.txt

# layerのzip作成
RUN zip -r /tmp/lambda-layer.zip python