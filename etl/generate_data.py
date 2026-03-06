# etl/generate_data.py
# FinanceIQ – Dummy Data Generator
# Generates realistic finance data for 2023-2024

import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

START_DATE = date(2023, 1, 1)
END_DATE   = date(2024, 12, 31)
NUM_TRANSACTIONS = 5000

# ---------------------------------------------------------------------------
# 1. dim_date
# ---------------------------------------------------------------------------
dates = pd.date_range(START_DATE, END_DATE, freq="D")
dim_date = pd.DataFrame({
    "date_id":    dates.strftime("%Y%m%d").astype(int),
    "full_date":  dates.date,
    "year":       dates.year,
    "quarter":    dates.quarter,
    "month":      dates.month,
    "month_name": dates.strftime("%B"),
    "week":       dates.isocalendar().week.astype(int),
    "day":        dates.day,
    "day_name":   dates.strftime("%A"),
})

# ---------------------------------------------------------------------------
# 2. dim_account
# ---------------------------------------------------------------------------
dim_account = pd.DataFrame([
    (1, "4000", "Personalkosten",    "Opex"),
    (2, "4100", "Miete & Nebenkosten","Opex"),
    (3, "4200", "IT-Lizenzen",       "Opex"),
    (4, "4300", "Marketing & Werbung","Opex"),
    (5, "4400", "Reisekosten",       "Opex"),
    (6, "5000", "Hardware / Capex",  "Capex"),
    (7, "6000", "Umsatzerlöse",      "Revenue"),
    (8, "6100", "Sonstige Erträge",  "Revenue"),
], columns=["account_id", "account_code", "account_name", "category"])

# ---------------------------------------------------------------------------
# 3. dim_costcenter
# ---------------------------------------------------------------------------
dim_costcenter = pd.DataFrame([
    (1, "CC-100", "Finance",   "Finance & Controlling", "Anna Müller"),
    (2, "CC-200", "Marketing", "Sales & Marketing",     "Ben Schmidt"),
    (3, "CC-300", "IT",        "Technology",            "Clara Weber"),
    (4, "CC-400", "HR",        "Human Resources",       "David Koch"),
    (5, "CC-500", "Sales",     "Sales & Marketing",     "Eva Bauer"),
], columns=["costcenter_id", "costcenter_code", "costcenter_name", "department", "manager"])

# ---------------------------------------------------------------------------
# 4. fact_transactions  – with realistic patterns
# ---------------------------------------------------------------------------
# Amount ranges per account (negative = expense, positive = revenue)
AMOUNT_RANGES = {
    1: (-12000, -8000),   # Personalkosten  – stable, high
    2: (-3500,  -2800),   # Miete           – very stable
    3: (-1500,   -800),   # IT-Lizenzen     – stable
    4: (-5000,   -500),   # Marketing       – varies a lot
    5: (-800,    -100),   # Reisekosten     – small, varies
    6: (-15000, -5000),   # Capex           – occasional spikes
    7: (20000,  80000),   # Umsatz          – main revenue
    8: (500,    3000),    # Sonstige Erträge
}

rows = []
for i in range(1, NUM_TRANSACTIONS + 1):
    acc_id  = random.choice(dim_account["account_id"].tolist())
    cc_id   = random.choice(dim_costcenter["costcenter_id"].tolist())
    d_id    = random.choice(dim_date["date_id"].tolist())
    lo, hi  = AMOUNT_RANGES[acc_id]
    amount  = round(random.uniform(lo, hi), 2)

    # 20 % budget entries, 80 % actual
    t_type  = "budget" if random.random() < 0.2 else "actual"

    # Inject ~2 % anomalies (budget overruns) for the AI agent to find later
    if t_type == "actual" and random.random() < 0.02:
        amount = round(amount * random.uniform(2.5, 4.0), 2)

    rows.append((i, d_id, acc_id, cc_id, amount, "EUR", t_type))

fact_transactions = pd.DataFrame(
    rows,
    columns=["transaction_id", "date_id", "account_id",
             "costcenter_id", "amount", "currency", "transaction_type"]
)

# ---------------------------------------------------------------------------
# 5. Save to data/raw/
# ---------------------------------------------------------------------------
dim_date.to_csv("data/raw/dim_date.csv", index=False)
dim_account.to_csv("data/raw/dim_account.csv", index=False)
dim_costcenter.to_csv("data/raw/dim_costcenter.csv", index=False)
fact_transactions.to_csv("data/raw/fact_transactions.csv", index=False)

print(f"✅ Dummy-Daten generiert!")
print(f"   dim_date:          {len(dim_date):>5} rows")
print(f"   dim_account:       {len(dim_account):>5} rows")
print(f"   dim_costcenter:    {len(dim_costcenter):>5} rows")
print(f"   fact_transactions: {len(fact_transactions):>5} rows")
print(f"\n💡 ~{int(NUM_TRANSACTIONS*0.02)} Anomalien eingebaut – für den AI-Agent später!")