# stockmarket-dashboard

## 概要

株価を取得してテクニカルを確認できるダッシュボードをplotlyとDashで作る。

## 開発環境

Dockerイメージ「python:3.8-slim」上で開発した。

## 使い方

1. dev-containerの設定かrequirements.txtに従って必要なパッケージをインストールする
2. ```python prepare.py```でDBファイルを用意する。```python download.py```でデータをダウンロードしてDBに保存する。
3. ```python app.py```でアプリケーションを起動する
4. ブラウザで```localhost:8050```を開く
5. 取得期間と証券コードを決めて送信する

## 機能

## テスト

テストコードの1番上で```app```ディレクトリをインポート時のsearch pathに追加しているので、```python test_*.py```で個別のテストを実行できる。
