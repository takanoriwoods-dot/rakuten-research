"""
楽天市場 商品検索CSV出力スクリプト

使い方:
    python search_rakuten.py "キーワード"

事前準備:
    1. .env.example を .env にコピーし、RAKUTEN_APP_ID に取得したアプリIDを設定する
    2. pip install -r requirements.txt
"""

import csv
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
OUTPUT_DIR = Path(__file__).parent / "output"


def search_items(app_id: str, keyword: str) -> list[dict]:
    params = {
        "applicationId": app_id,
        "keyword": keyword,
        "format": "json",
        "hits": 30,  # 1ページあたりの最大件数
    }
    response = requests.get(API_URL, params=params, timeout=10)
    if not response.ok:
        print(f"APIエラー詳細: {response.text}")
    response.raise_for_status()
    data = response.json()

    items = []
    for entry in data.get("Items", []):
        item = entry["Item"]
        items.append({
            "商品名": item.get("itemName"),
            "価格": item.get("itemPrice"),
            "レビュー件数": item.get("reviewCount"),
            "レビュー評価": item.get("reviewAverage"),
            "URL": item.get("itemUrl"),
        })
    return items


def save_to_csv(items: list[dict], keyword: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{keyword}.csv"

    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["商品名", "価格", "レビュー件数", "レビュー評価", "URL"])
        writer.writeheader()
        writer.writerows(items)

    return output_path


def main():
    if len(sys.argv) != 2:
        print("使い方: python search_rakuten.py \"キーワード\"")
        sys.exit(1)

    keyword = sys.argv[1]

    load_dotenv()
    app_id = os.getenv("RAKUTEN_APP_ID")
    if not app_id:
        print("エラー: .env に RAKUTEN_APP_ID が設定されていません。")
        print(".env.example を参考に .env ファイルを作成してください。")
        sys.exit(1)

    print(f"「{keyword}」で楽天市場を検索中...")
    items = search_items(app_id, keyword)
    print(f"{len(items)}件の商品を取得しました。")

    output_path = save_to_csv(items, keyword)
    print(f"CSVを保存しました: {output_path}")


if __name__ == "__main__":
    main()
