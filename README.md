# Customer Segmentation using RFM Analysis

Segment customers into actionable groups (Champions, Loyal, At Risk, Lost...) using **Recency, Frequency and Monetary (RFM)** analysis in Python, so a business knows who to reward, retain or win back.

> **Note:** The transactions are **synthetic** (generated with a fixed seed in `generate_data.py`). Customers are created with different behaviour profiles so the segmentation has meaningful structure.

## Business Problem
Marketing budgets are limited. Treating every customer the same wastes money. RFM answers:
- **Recency** - how recently did the customer buy?
- **Frequency** - how often do they buy?
- **Monetary** - how much do they spend?

## Tech Stack
Python | Pandas | NumPy | Matplotlib

## Project Structure
```
customer-segmentation-rfm/
├── data/transactions.csv      # 11,289 synthetic transactions, 1,500 customers
├── outputs/                   # rfm_segments.csv, segment_summary.csv, charts
├── generate_data.py           # creates the dataset
├── rfm_analysis.py            # RFM scoring + segmentation + charts
└── requirements.txt
```

## Methodology
1. Clean data (remove nulls, duplicates, non-positive amounts).
2. Set the snapshot date as the day after the last transaction.
3. Calculate per customer: Recency (days since last purchase), Frequency (order count), Monetary (total spend).
4. Score each metric from 1 to 5 using quintiles (`pd.qcut`); 5 is best.
5. Assign segments with simple, explainable rules:

| Segment | Rule |
|---|---|
| Champions | R >= 4 and F >= 4 |
| Loyal Customers | R >= 3 and F >= 3 |
| New / Promising | R >= 4 and F <= 2 |
| At Risk | R <= 2 and F >= 4 |
| Lost | R <= 2 and F <= 2 |
| Needs Attention | everyone else |

## How to Run
```bash
git clone https://github.com/<your-username>/customer-segmentation-rfm.git
cd customer-segmentation-rfm
pip install -r requirements.txt

python generate_data.py
python rfm_analysis.py
```

## Sample Output (seed = 7)
| Segment | Customers | Revenue Share |
|---|---|---|
| Champions | 419 | 66.2% |
| Loyal Customers | 292 | 17.4% |
| Needs Attention | 243 | 6.3% |
| Lost | 410 | 5.7% |
| At Risk | 50 | 3.1% |
| New / Promising | 86 | 1.3% |

**Insight:** Champions are about 28% of customers but bring about two-thirds of revenue, so retention of this group is the top priority. The 50 "At Risk" customers used to buy often, making them the best target for a win-back campaign.

## Recommended Actions
- **Champions:** loyalty rewards, early access to new products
- **Loyal:** upsell and cross-sell offers
- **At Risk:** personalised win-back discount
- **Lost:** low-cost reactivation email, or deprioritise
- **New / Promising:** onboarding offers to drive a second purchase

## Key Learnings
- Customer analytics with RFM and quantile scoring
- Using `groupby`, `agg`, `qcut` and custom functions in Pandas
- Turning analysis into business recommendations

## Author
**Kaustubh Parashar** - B.Tech CSE | Aspiring Data Analyst
[LinkedIn](#) | [GitHub](#)
