import pandas as pd
import random
from datetime import datetime, timedelta

# Make results reproducible
random.seed(42)

# Number of transactions
num_transactions = 120

# Starting date
start_date = datetime(2026, 8, 1)

payments = []
settlements = []

for i in range(1, num_transactions + 1):

    order_id = f"ORD{i:04d}"
    transaction_id = f"TX{i:04d}"
    customer_id = f"CUST{i:04d}"

    payment_date = start_date + timedelta(days=random.randint(0, 20))

    amount = random.choice([
        500, 750, 1000, 1200, 1500,
        2000, 2500, 3000, 3500, 5000
    ])

    payments.append({
        "transaction_id": transaction_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "payment_date": payment_date.strftime("%Y-%m-%d"),
        "amount": amount,
        "payment_status": "SUCCESS"
    })

    # Normally settlement equals payment amount
    settlement_amount = amount

    # Introduce some amount mismatches
    if i % 15 == 0:
        settlement_amount = amount - 100

    # Some transactions will have no settlement
    if i % 20 != 0:
        settlement_id = f"ST{i:04d}"

        settlement_date = payment_date + timedelta(days=random.randint(1, 3))

        settlements.append({
            "settlement_id": settlement_id,
            "order_id": order_id,
            "settlement_date": settlement_date.strftime("%Y-%m-%d"),
            "settled_amount": settlement_amount,
            "settlement_status": "SETTLED"
        })


# Add a few unmatched settlements
for i in range(121, 126):

    order_id = f"ORD{i:04d}"

    settlement_date = start_date + timedelta(days=random.randint(1, 20))

    settlements.append({
        "settlement_id": f"ST{i:04d}",
        "order_id": order_id,
        "settlement_date": settlement_date.strftime("%Y-%m-%d"),
        "settled_amount": random.choice([1000, 1500, 2000, 2500]),
        "settlement_status": "SETTLED"
    })


# Add one duplicate settlement
if settlements:
    settlements.append(settlements[0].copy())


# Convert to DataFrames
payments_df = pd.DataFrame(payments)
settlements_df = pd.DataFrame(settlements)


# Save CSV files
payments_df.to_csv("data/payments.csv", index=False)
settlements_df.to_csv("data/settlements.csv", index=False)


print("Data generation completed successfully!")
print(f"Payments generated: {len(payments_df)}")
print(f"Settlements generated: {len(settlements_df)}")
print("Files saved inside the data folder.")