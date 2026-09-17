from src.reconciliation_engine import run_reconciliation


result = run_reconciliation()

summary = result["summary"]

print("TEST RESULTS")
print("--------------------")

print("Total Payments:", summary["total_payments"].iloc[0])
print("Matched Transactions:", summary["matched_transactions"].iloc[0])
print("Amount Mismatches:", summary["amount_mismatches"].iloc[0])
print("Missing Settlements:", summary["missing_settlements"].iloc[0])
print("Total Mismatch Amount:", summary["total_mismatch_amount"].iloc[0])

print()
print("Engine test completed successfully!")