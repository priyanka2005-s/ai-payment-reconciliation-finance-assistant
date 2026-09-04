import pandas as pd


def run_reconciliation(
    payments_file="Data/payments.csv",
    settlements_file="Data/settlements.csv"
):
    # Load payment data
    payments = pd.read_csv(payments_file)

    # Load settlement data
    settlements = pd.read_csv(settlements_file)

    # Remove duplicate settlement records for reconciliation
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

        if pd.isna(row["settled_amount"]):
            return "MISSING SETTLEMENT"

        elif row["difference"] == 0:
            return "MATCHED"

        else:
            return "AMOUNT MISMATCH"

    # Apply status
    reconciled["reconciliation_status"] = reconciled.apply(
        determine_status,
        axis=1
    )

    # Find unmatched settlements
    unmatched_settlements = settlements.merge(
        payments,
        on="order_id",
        how="left"
    )

    unmatched_settlements = unmatched_settlements[
        unmatched_settlements["amount"].isna()
    ]

    # Find duplicate settlements
    duplicates = settlements[
        settlements.duplicated(
            subset=["order_id"],
            keep=False
        )
    ]

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

    # Unmatched settlement report
    unmatched_report = unmatched_settlements[
        [
            "order_id",
            "amount",
            "settled_amount"
        ]
    ].copy()

    unmatched_report["reconciliation_status"] = (
        "UNMATCHED SETTLEMENT"
    )

    unmatched_report["difference"] = None

    # Duplicate settlement report
    duplicate_report = duplicates[
        [
            "order_id",
            "settled_amount"
        ]
    ].copy()

    duplicate_report["amount"] = None
    duplicate_report["difference"] = None
    duplicate_report["reconciliation_status"] = (
        "DUPLICATE SETTLEMENT"
    )

    # Combine exception reports
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

    # Return results to other parts of the application
    return {
        "reconciled": reconciled,
        "exceptions": final_exceptions,
        "summary": summary_df,
        "unmatched_settlements": unmatched_settlements,
        "duplicates": duplicates
    }