import pandas as pd
from pathlib import Path


# Load payment data
payments = pd.read_csv("data/payments.csv")

# Load settlement data
settlements = pd.read_csv("data/settlements.csv")

clean_settlements = settlements.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

# Merge payments and settlements
reconciled = pd.merge(
    payments,
    clean_settlements,
    on="order_id",
    how="left"
)


# Calculate difference
reconciled["difference"] = (
    reconciled["amount"] -
    reconciled["settled_amount"]
)


# Determine reconciliation status
def determine_status(row):

    # Settlement does not exist
    if pd.isna(row["settled_amount"]):
        return "MISSING SETTLEMENT"

    # Payment and settlement amounts are equal
    elif row["difference"] == 0:
        return "MATCHED"

    # Payment and settlement amounts are different
    else:
        return "AMOUNT MISMATCH"


# Apply the function to every row
reconciled["reconciliation_status"] = reconciled.apply(
    determine_status,
    axis=1
)


# Save the result
reconciled.to_csv(
    "data/reconciliation_results.csv",
    index=False
)


# Display results
print("Reconciliation completed successfully!")
print()
print(reconciled["reconciliation_status"].value_counts())

# Check for settlements without matching payments
unmatched_settlements = settlements.merge(
    payments,
    on="order_id",
    how="left"
)

unmatched_settlements = unmatched_settlements[
    unmatched_settlements["amount"].isna()
]

print()
print("Unmatched settlements:")
print(unmatched_settlements)

# Check for duplicate settlements
duplicates = settlements[
    settlements.duplicated(
        subset=["order_id"],
        keep=False
    )
]

print()
print("Duplicate settlements:")
print(duplicates)

# Payment-side exceptions
exceptions = reconciled[
    reconciled["reconciliation_status"] != "MATCHED"
].copy()

payment_report = exceptions[
    [
        "order_id",
        "amount",
        "settled_amount",
        "difference",
        "reconciliation_status"
    ]
].copy()


# Unmatched settlements
unmatched_report = unmatched_settlements[
    [
        "order_id",
        "amount",
        "settled_amount"
    ]
].copy()

unmatched_report["reconciliation_status"] = "UNMATCHED SETTLEMENT"

unmatched_report["difference"] = None

# Duplicate settlements
duplicate_report = duplicates[
    [
        "order_id",
        "settled_amount"
    ]
].copy()

duplicate_report["amount"] = None
duplicate_report["difference"] = None
duplicate_report["reconciliation_status"] = "DUPLICATE SETTLEMENT"

# Combine both exception reports
final_exceptions = pd.concat(
    [
        payment_report,
        unmatched_report,
        duplicate_report
    ],
    ignore_index=True
)
# Give every exception record a unique ID
final_exceptions.insert(
    0,
    "exception_record_id",
    range(1, len(final_exceptions) + 1)
)


# Save final report
final_exceptions.to_csv(
    "data/reconciliation_report.csv",
    index=False
)

print()
print("Final reconciliation report created!")
print(final_exceptions)

# Reconciliation summary

total_payments = len(payments)

total_payment_amount = payments["amount"].sum()

matched_count = (
    reconciled["reconciliation_status"] == "MATCHED"
).sum()

amount_mismatch_count = (
    reconciled["reconciliation_status"] == "AMOUNT MISMATCH"
).sum()

missing_settlement_count = (
    reconciled["reconciliation_status"] == "MISSING SETTLEMENT"
).sum()

total_mismatch_amount = reconciled[
    reconciled["reconciliation_status"] == "AMOUNT MISMATCH"
]["difference"].sum()

unmatched_settlement_count = len(unmatched_settlements)

duplicate_settlement_records = len(duplicates)

duplicate_order_count = duplicates["order_id"].nunique()


summary = {
    "total_payments": total_payments,
    "total_payment_amount": total_payment_amount,
    "matched_transactions": matched_count,
    "amount_mismatches": amount_mismatch_count,
    "missing_settlements": missing_settlement_count,
    "total_mismatch_amount": total_mismatch_amount,
    "unmatched_settlements": unmatched_settlement_count,
    "duplicate_settlement_records": duplicate_settlement_records,
    "duplicate_orders": duplicate_order_count
}


summary_df = pd.DataFrame([summary])


summary_df.to_csv(
    "data/reconciliation_summary.csv",
    index=False
)


print()
print("Reconciliation summary:")
print(summary_df.to_string(index=False))

print()
print("Total reconciled rows:", len(reconciled))