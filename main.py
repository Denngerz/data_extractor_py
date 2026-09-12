import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

def get_reviews(slug):
    # 1. Download the HTML page (not JSON this time)
    url = f"https://www.metacritic.com/movie/{slug}/user-reviews/"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # stop with an error if the request failed

    # 2. Parse the HTML into a searchable tree
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. Find every review card on the page
    cards = soup.find_all("div", attrs={"data-testid": "review-card"})

    rows = []
    for card in cards:
        # 4. Inside each card, find the parts we need
        score_tag = card.select_one("div.c-siteReviewScore span")
        date_tag  = card.find(attrs={"data-testid": "review-card-date"})
        user_tag  = card.find("a", attrs={"data-testid": "review-card-header"})
        quote_tag = card.find(attrs={"data-testid": "review-quote-text"})

        rows.append({
            "score":  int(score_tag.get_text(strip=True)) if score_tag else None,
            "date":   date_tag.get_text(strip=True) if date_tag else None,
            "author": user_tag["href"].strip("/").split("/")[-1] if user_tag else None,
            "quote":  quote_tag.get_text(strip=True) if quote_tag else None,
        })

    return pd.DataFrame(rows)

df = get_reviews("parasite")
print(len(df))
print(df[["score", "date", "quote"]].head())