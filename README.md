# 楽天市場 商品リサーチツール

楽天市場のキーワード検索結果から商品情報（商品名・価格・レビュー件数・レビュー評価・URL）を取得し、CSVに保存するスクリプトです。

## 1. 楽天APIキー（アプリID）の取得

1. https://webservice.rakuten.co.jp/ にアクセスし、楽天会員でログイン
2. 「アプリID発行」からアプリを新規登録（アプリ名・用途は自由記入でOK）
3. 発行された **アプリID** をコピー

## 2. セットアップ

```bash
pip install -r requirements.txt
cp .env.example .env
```

`.env` を開き、`RAKUTEN_APP_ID` に取得したアプリIDを貼り付けてください。

## 3. 実行

```bash
python search_rakuten.py "キーワード"
```

例:
```bash
python search_rakuten.py "ワイヤレスイヤホン"
```

実行すると `output/キーワード.csv` に検索結果（最大30件）が保存されます。

## 今後の拡張予定

- 複数ページ取得への対応
- 独自の選定基準（世界観適合・語れる強さなど）によるフィルタリング・採点機能
