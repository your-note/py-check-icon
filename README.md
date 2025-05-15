# py-check-icon

## 概要
py-check-icon は、78x78ピクセルの画像データセット（ok, warn, other）を用いた画像分類プロジェクトです。画像ファイルを前処理し、機械学習モデル（SVM）で分類を行います。

## ディレクトリ構成
```
dataset/
  ├─ ok/
  ├─ warn/
  └─ other/
detect.py
preprocess.py
requirements.txt
label_encoder.pkl
svm_model.pkl
```

## セットアップ方法

1. 必要なPythonパッケージをインストールします。
   ```
   pip install -r requirements.txt
   ```

2. あらかじめ `有線接続アイコン(ok)` `無線接続アイコン(warn)` `それ以外の画像(other)` で前処理を行ったデータが label_encoder.pkl, svm_model.pkl になります。

3. (必要なら)データセットを`dataset/ok`, `dataset/warn`, `dataset/other`に配置してください。

## 使い方

### 前処理

(必要なら)画像データの前処理を行うには、以下を実行します。

```
python preprocess.py
```

これにより label_encoder.pkl, svm_model.pkl が生成されます

### 推論

画像の分類を行うには、以下を実行して特定プログラムを起動させます。

```
python detect.py
```

これは、特定プログラムが動いているとき、一定間隔で特定ウィンドウタイトルをキャプチャし、特定位置の画像を ok, warn, other のどれであるかを識別します。

ok が検知されたときには ok.mp3 が、 warn が検知されたときには ng.mp3 が再生されます。

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。

## 謝辞

音声ファイルは `効果音ラボ` のものを利用しております。