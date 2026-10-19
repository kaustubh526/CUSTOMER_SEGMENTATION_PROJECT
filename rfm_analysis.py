"""Customer Segmentation using RFM (Recency, Frequency, Monetary) analysis."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


def build_rfm(path="data/transactions.csv"):
    df = pd.read_csv(path, parse_dates=["transaction_date"])
    df = df.dropna().drop_duplicates("transaction_id")
    df = df[df["amount"] > 0]

    # Snapshot = one day after the last transaction in the data
    snapshot = df["transaction_date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_id").agg(
        recency=("transaction_date", lambda s: (snapshot - s.max()).days),
        frequency=("transaction_id", "count"),
        monetary=("amount", "sum"),
    )

    # Score 1-5 (5 = best). Lower recency is better, so labels are reversed.
    rfm["R"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["rfm_score"] = rfm["R"] + rfm["F"] + rfm["M"]
    return rfm


def segment(row):
    r, f = row["R"], row["F"]
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal Customers"
    if r >= 4 and f <= 2:
        return "New / Promising"
    if r <= 2 and f >= 4:
        return "At Risk"
    if r <= 2 and f <= 2:
        return "Lost"
    return "Needs Attention"


def main():
    rfm = build_rfm()
    rfm["segment"] = rfm.apply(segment, axis=1)

    summary = (
        rfm.groupby("segment")
        .agg(customers=("monetary", "size"),
             avg_recency_days=("recency", "mean"),
             avg_frequency=("frequency", "mean"),
             avg_spend=("monetary", "mean"),
             total_revenue=("monetary", "sum"))
        .round(1)
        .sort_values("total_revenue", ascending=False)
    )
    summary["revenue_share_pct"] = (100 * summary["total_revenue"] / summary["total_revenue"].sum()).round(1)
    print(summary.to_string())

    rfm.to_csv(OUT / "rfm_segments.csv")
    summary.to_csv(OUT / "segment_summary.csv")

    # Chart 1: customers per segment
    fig, ax = plt.subplots(figsize=(8, 4.5))
    summary["customers"].plot.bar(ax=ax, color="#2a6f97", rot=25)
    ax.set_title("Customers per Segment", fontweight="bold")
    ax.set_ylabel("Customers")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(OUT / "customers_per_segment.png", dpi=150)
    plt.close(fig)

    # Chart 2: revenue share per segment
    fig, ax = plt.subplots(figsize=(8, 4.5))
    summary["revenue_share_pct"].plot.bar(ax=ax, color="#e07a5f", rot=25)
    ax.set_title("Revenue Share by Segment (%)", fontweight="bold")
    ax.set_ylabel("% of total revenue")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(OUT / "revenue_share_by_segment.png", dpi=150)
    plt.close(fig)

    # Chart 3: frequency vs monetary scatter
    fig, ax = plt.subplots(figsize=(8, 5))
    for name, g in rfm.groupby("segment"):
        ax.scatter(g["frequency"], g["monetary"], s=12, alpha=0.6, label=name)
    ax.set_title("Frequency vs Monetary by Segment", fontweight="bold")
    ax.set_xlabel("Frequency (orders)")
    ax.set_ylabel("Monetary (INR)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "frequency_vs_monetary.png", dpi=150)
    plt.close(fig)

    print("\nSaved rfm_segments.csv, segment_summary.csv and charts in outputs/")


if __name__ == "__main__":
    main()
