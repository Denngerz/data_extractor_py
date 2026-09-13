import reviews_scraper as scraper
import pandas as pd, seaborn as sns, scipy.stats as stats, matplotlib.pyplot as plt

def analyze_reviews(slug1, slug2):
    slug1_data = scraper.get_reviews(slug1)
    slug2_data = scraper.get_reviews(slug2)
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

analyze_reviews("the-dark-knight", "joker")