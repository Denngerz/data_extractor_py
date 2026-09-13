import reviews_scraper as scraper
import pandas as pd, seaborn as sns, scipy.stats as stats, matplotlib.pyplot as plt
import argparse

def analyze_reviews(slug1, slug2, max_reviews_count=400):
    slug1_data = scraper.get_reviews(slug=slug1, max_reviews=max_reviews_count)
    slug2_data = scraper.get_reviews(slug=slug2, max_reviews=max_reviews_count)
    slug1_data["movie"] = slug1
    slug2_data["movie"] = slug2
    df = pd.concat([slug1_data, slug2_data], ignore_index=True)

    df["word_count"] = df["quote"].fillna("").str.split().str.len()

    scores_data = df.groupby("movie")["score"]
    print(scores_data.agg( 
        mean="mean",
        median="median",
        mode=lambda x: x.mode()[0],
        std="std",
        min="min",
        max="max",
        var="var",
        skew="skew",
        kurtosis=lambda x: x.kurt(),
    ).round(2))

    a = df.loc[df["movie"] == slug1, "score"]
    b = df.loc[df["movie"] == slug2, "score"]

    t, p = stats.ttest_ind(a, b, equal_var=False)
    print (f"T-test results (score): t-statistic = {t:.4f}, p-value = {p:.4f}")

    r, p = stats.pearsonr(df["word_count"], df["score"])
    print (f"Pearson correlation results (word count to score): r = {r:.4f}, p-value = {p:.4f}")

    sns.boxplot(data=df, x="movie", y="score")
    sns.stripplot(data=df, x="movie", y="score", color="black", alpha=0.3, jitter=0.25)
    plt.title(f"User scores: {slug1} vs {slug2}")
    plt.xlabel("Movie")
    plt.ylabel("User score (0–10)")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare Metacritic user reviews of two films.")
    parser.add_argument("movie1", help="Metacritic slug of the first film, e.g. the-dark-knight")
    parser.add_argument("movie2", help="Metacritic slug of the second film, e.g. joker")
    parser.add_argument("--max-reviews", type=int, default=400, help="maximum number of reviews per film (default: 400)")
    args = parser.parse_args()

    analyze_reviews(args.movie1, args.movie2, args.max_reviews)