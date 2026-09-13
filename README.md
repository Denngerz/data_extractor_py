# data_extractor_py

A Python program that automatically extracts user film reviews from [Metacritic](https://www.metacritic.com) and compares two films using descriptive and inferential statistics.

Created as Homework 1 for the *Fundamentals of AI* course (VGTU).

## What it does

1. **Extracts data:** downloads user reviews (score, date, author, review text) for two films from Metacritic's JSON review endpoint, page by page.
2. **Prepares data:** combines both films into one table and adds a `word_count` column computed from the review text.
3. **Descriptive statistics** of the user scores for each film: mean, median, mode, standard deviation, variance, minimum, maximum, skewness and kurtosis.
4. **Inferential statistics:**
   - **Welch's t-test:** do the two films have different mean user scores?
   - **Pearson correlation:** is review length (word count) related to the score?
5. **Visualization:** a box plot of scores for each film, with individual reviews overlaid as points.

## Project structure

```
data_extractor_py/
├── reviews_scraper.py    # extracts reviews from Metacritic (HTTP + JSON, with pagination)
├── reviews_analysis.py   # statistics, hypothesis testing and box plot
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10+
- Libraries: `requests`, `pandas`, `scipy`, `seaborn`, `matplotlib`

## Installation

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows (PowerShell)
# source .venv/bin/activate         # macOS / Linux

pip install requests pandas scipy seaborn matplotlib
```

## Usage

```bash
python reviews_analysis.py
```

The films are set in the last line of `reviews_analysis.py`:

```python
analyze_reviews("the-dark-knight", "joker")
```

Use the film's **slug**, the name as it appears in the Metacritic URL. For example, `https://www.metacritic.com/movie/the-dark-knight/` has the slug `the-dark-knight`.

### Number of reviews

`get_reviews()` in `reviews_scraper.py` downloads up to `max_reviews` reviews per film (default: **400**), 50 per request, with a 1-second pause between requests:

```python
get_reviews("joker", max_reviews=1000)
```

## How data extraction works

The Metacritic review web page contains only the first 50 reviews; the rest are loaded with JavaScript. The program therefore requests the JSON endpoint that the page itself uses:

```
https://backend.metacritic.com/reviews/metacritic/user/movies/<slug>/web?offset=0&limit=50
```

- `limit`: number of reviews per request (page size)
- `offset`: number of reviews to skip; it grows by 50 on each request until all reviews (or `max_reviews`) are collected
- `data.items`: the list of reviews in the response; `data.totalResults` is the total number of reviews for the film
- A browser `User-Agent` header is sent, because requests identifying as the default Python client may be blocked

## Output

**Console:**
- a table of descriptive statistics for each film
- the t-test result (t-statistic, p-value)
- the Pearson correlation result (r, p-value)

**Window:** a box plot comparing the score distributions of the two films.

### Interpreting the results

| Result | Meaning |
|---|---|
| t-test p < 0.05 | Reject H₀: the films' mean scores differ significantly. The sign of *t* shows which film has the higher mean (positive means the first film is higher). |
| t-test p ≥ 0.05 | Not enough evidence that the mean scores differ. |
| Correlation *r* | From −1 to +1; the sign gives the direction, \|r\| gives the strength (< 0.3 weak, 0.3–0.7 moderate, > 0.7 strong). |
| Correlation p < 0.05 | The correlation is statistically significant. |
| Skewness < 0 | Most scores are high, with a tail of low scores. |
| Kurtosis > 0 | Scores are more concentrated, with heavier tails (more extreme values) than a normal distribution. |

## Notes

- The Metacritic JSON endpoint is not an official public API and may change without notice.
- Review data is downloaded again on every run, so results can change slightly as new reviews are posted.
- Please keep the request pause in place and avoid downloading very large amounts of data.