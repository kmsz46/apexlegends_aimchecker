# Apex Legendsのプレイ動画から戦闘シーンのみを自動抽出するコード
## 概要
Apex Legendsのプレイ動画から画像解析技術を用いて、自動で戦闘シーンのみを切り抜くプログラム
## 環境構築
### Tesseractのインストール
コードを実行する事前にTesseractのインストールする必要があります。<br/>
[こちら](https://gammasoft.jp/blog/tesseract-ocr-install-on-windows/)が参考になったので使ってみてください。
### 各種ライブラリをインストール
python3.8.7で実装しています。<br/>
その他の環境での実装は試せていないのですが、python3.8以上の環境で実装してみてください<br/>
ライブラリのインストール:<br/>
```
pip install -r requirements.txt
```
## 使い方
```
# 形式について
python main.py 元動画のファイルパス 書き出すファイルパス
# 例
python cut.py movie_data/rensyu.mp4 movie_data/cut_rensyu.mp4
```
