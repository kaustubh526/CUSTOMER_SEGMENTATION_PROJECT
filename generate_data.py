"""Generate a synthetic e-commerce transactions dataset (seeded, reproducible).

Customers are created with different behaviour profiles (loyal, regular,
occasional, churned) so the RFM segmentation has real structure to find.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N_CUSTOMERS = 1500
START, END = pd.Timestamp("2024-01-01"), pd.Timestamp("2025-12-31")
total_days = (END - START).days

profiles = {
    #            share, orders (min,max), avg spend, active window (days before END)
    "loyal":      (0.15, (12, 30), 2200, 90),
    "regular":    (0.30, (5, 12),  1500, 240),
    "occasional": (0.35, (1, 5),   1000, 540),
    "churned":    (0.20, (1, 6),   1200, 730),
}

rows, txn_id = [], 1
names, probs = list(profiles), [p[0] for p in profiles.values()]
for c in range(1, N_CUSTOMERS + 1):
    kind = rng.choice(names, p=probs)
    _, (lo, hi), spend, _ = profiles[kind]
    n_orders = int(rng.integers(lo, hi + 1))
    for _ in range(n_orders):
        if kind == "churned":   # last purchase happened long ago
            day = int(rng.integers(0, total_days - 300))
        elif kind == "loyal":
            day = int(rng.integers(total_days - 700, total_days + 1))
        else:
            day = int(rng.integers(0, total_days + 1))
        rows.append({
            "transaction_id": f"T{txn_id:06d}",
            "customer_id": f"C{c:04d}",
            "transaction_date": (START + pd.Timedelta(days=day)).strftime("%Y-%m-%d"),
            "amount": round(float(rng.gamma(shape=4, scale=spend / 4)), 2),
        })
        txn_id += 1

df = pd.DataFrame(rows).sort_values("transaction_date").reset_index(drop=True)
df.to_csv("data/transactions.csv", index=False)
print(f"Saved data/transactions.csv: {len(df)} transactions, {df['customer_id'].nunique()} customers")
