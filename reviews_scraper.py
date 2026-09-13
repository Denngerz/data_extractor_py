import time
import requests
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

def get_reviews(slug, page_size=50, max_reviews=400):
    url = f"https://backend.metacritic.com/reviews/metacritic/user/movies/{slug}/web"
    rows, offset = [], 0

    while True:
        response = requests.get(url, params={"offset": offset, "limit": page_size},headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()["data"]

        for item in data["items"]:
            rows.append({
                "score":  item.get("score"),
                "date":   item.get("date"),
                "author": item.get("author"),
                "quote":  item.get("quote"),
            })

        offset += page_size
        total_results = min(data["totalResults"], max_reviews)

        print(f"{slug}: {len(rows)} / {total_results} reviews")

        if offset >= total_results or not data["items"]:
            break

        time.sleep(1)

    return pd.DataFrame(rows)