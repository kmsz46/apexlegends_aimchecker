# Apex Legendsのプレイ動画から戦闘シーンのみを自動抽出するコード
## 背景
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
python main.py rensyu.mp4 edit_rensyu.mp4
```
