import streamlit as st
import os
from google import genai

from reconciliation_engine import run_reconciliation
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)


st.title("💰 AI Finance Controller")

st.write(
    "AI-powered payment and settlement reconciliation assistant"
)


# Run reconciliation engine
result = run_reconciliation()


# Get results
summary = result["summary"]
reconciled = result["reconciled"]
exceptions = result["exceptions"]


# Summary values
total_payments = summary["total_payments"].iloc[0]
total_payment_amount = summary["total_payment_amount"].iloc[0]
matched_transactions = summary["matched_transactions"].iloc[0]
amount_mismatches = summary["amount_mismatches"].iloc[0]
missing_settlements = summary["missing_settlements"].iloc[0]
total_mismatch_amount = summary["total_mismatch_amount"].iloc[0]


# Dashboard metrics
st.subheader("📊 Reconciliation Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Payments",
        total_payments
    )

with col2:
    st.metric(
        "Total Payment Amount",
        f"₹{total_payment_amount:,.0f}"
    )

with col3:
    st.metric(
        "Matched Transactions",
        matched_transactions
    )

with col4:
    st.metric(
        "Exception Transactions",
        amount_mismatches + missing_settlements
    )


st.divider()


# Exception metrics
st.subheader("⚠️ Reconciliation Exceptions")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Amount Mismatches",
        amount_mismatches
    )

with col2:
    st.metric(
        "Missing Settlements",
        missing_settlements
    )

with col3:
    st.metric(
        "Mismatch Amount",
        f"₹{total_mismatch_amount:,.0f}"
    )


st.divider()


# Reconciliation status
st.subheader("📋 Reconciliation Status")

status_counts = (
    reconciled["reconciliation_status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Count"
]

st.bar_chart(
    status_counts.set_index("Status"),
    horizontal=True
)

st.divider()


# Exception table
st.subheader("🚨 Exception Transactions")

st.dataframe(
    exceptions,
    use_container_width=True
)



# AI Finance Assistant
st.divider()

st.subheader("🤖 AI Finance Assistant")

user_question = st.text_input(
    "Ask a question about the reconciliation data:"
)

if user_question:

    context = f"""
You are an AI Finance Controller.

You are analyzing payment reconciliation data.

Reconciliation summary:
- Total payments: {total_payments}
- Total payment amount: ₹{total_payment_amount:,.0f}
- Matched transactions: {matched_transactions}
- Amount mismatches: {amount_mismatches}
- Missing settlements: {missing_settlements}
- Total mismatch amount: ₹{total_mismatch_amount:,.0f}

Missing settlement transactions:
{reconciled[
    reconciled["reconciliation_status"] == "MISSING SETTLEMENT"
][
    ["transaction_id", "order_id", "amount", "payment_date"]
].to_string(index=False)}

Amount mismatch transactions:
{reconciled[
    reconciled["reconciliation_status"] == "AMOUNT MISMATCH"
][
    ["transaction_id", "order_id", "amount", "settled_amount", "difference", "payment_date"]
].to_string(index=False)}

Answer the user's question using only the reconciliation information provided above.

If the user asks about missing settlements, provide the transaction IDs/order IDs from the Missing settlement transactions section.

If the user asks about amount mismatches, provide the transaction IDs/order IDs and amount differences from the Amount mismatch transactions section.

Do not use markdown links, HTML, SVG links, anchors, or localhost links.
Use plain text headings and bullet points only.

Do not invent transaction IDs or other data.

User question:
{user_question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=context
        )

        st.write(response.text)

    except Exception as e:
        st.error(f"AI Error: {e}")