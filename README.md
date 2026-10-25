# ImageEditingSoftware

とりあえず画像編集ソフトを自作してみた。機能は少ないです。
Json形式は、学科の自主プロで作ったロボットの通信の圧縮方法に対応させました。

> 2025年2月頃、学生時代に作った小さなツールです。

## 機能

- 画像の読み込み（ファイル選択 / ドラッグ&ドロップ）
- 切り抜き（座標指定、プレビュー枠表示）
- サイズ変更（縦横のピクセル指定）
- 回転・反転（左右90°回転、水平・垂直反転）
- 保存（PNG / JPEG / PDF、上書き保存）
- 独自JSON形式での保存・読み込み（PNG → zlib圧縮 → Base64）

※ PDFは保存のみ対応しています（Pillowの仕様上、PDFの読み込みはできません）。

## 動かし方

当時は Python 3.12 で作成しました。

```bash
pip install pillow tkinterdnd2
python application.py
```

## 構成

- `application.py` … GUI（tkinter）と編集処理
- `json_command.py` … 画像とJSON形式の相互変換
