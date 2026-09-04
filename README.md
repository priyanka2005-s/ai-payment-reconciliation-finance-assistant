# AI Payment Reconciliation & Finance Controller

An AI-powered payment and settlement reconciliation system that automatically compares payment records with settlement records, identifies financial exceptions, and provides an AI Finance Assistant for answering reconciliation questions.

##  Project Overview

Payment reconciliation is an important finance operation where payment transactions need to be matched against settlement records.

This project automates that workflow using **Python and Pandas** and adds an **AI Finance Assistant powered by Gemini** to help users understand reconciliation results through natural-language questions.

### Workflow

```text
Payments CSV + Settlements CSV
            ↓
     Python / Pandas
            ↓
   Reconciliation Engine
            ↓
   Exception Identification
            ↓
   Reconciliation Results
            ↓
      AI Finance Assistant
            ↓
       Streamlit Dashboard
```

##  Key Features

* Automated payment and settlement reconciliation
* Payment-to-settlement matching using `order_id`
* Detection of amount mismatches
* Detection of missing settlements
* Detection of unmatched settlements
* Detection of duplicate settlement records
* Automatic calculation of mismatch amounts
* Reconciliation summary and exception reporting
* Interactive Streamlit dashboard
* Gemini-powered AI Finance Assistant
* Natural-language questions about reconciliation results
* Power BI dashboard for financial analysis

##  Reconciliation Results

The project uses a synthetic dataset containing **120 payment transactions**.

| Metric                       |   Result |
| ---------------------------- | -------: |
| Total Payments               |      120 |
| Total Payment Amount         | ₹226,400 |
| Matched Transactions         |      108 |
| Amount Mismatches            |        6 |
| Missing Settlements          |        6 |
| Total Exceptions             |       12 |
| Total Mismatch Amount        |     ₹600 |
| Unmatched Settlements        |        5 |
| Duplicate Settlement Records |        2 |

The reconciliation engine intentionally contains exceptions so that the system can demonstrate real-world finance reconciliation scenarios.

##  AI Finance Assistant

The AI assistant uses Gemini to answer questions based on the reconciliation results.

Example questions:

* How many transactions failed reconciliation?
* What is the total mismatch amount?
* Which transactions have missing settlements?
* Which transactions have amount mismatches?
* What are the main reconciliation issues?

The AI is provided with the reconciliation results as context and is instructed to answer using only the available reconciliation information.

##  Technology Stack

* **Python**
* **Pandas**
* **Google Gemini API**
* **Streamlit**
* **Power BI**
* **Excel**
* **Git & GitHub**

##  Project Structure

```text
ai-payment-reconciliation-finance-controller/
│
├── Data/
│   ├── payments.csv
│   ├── settlements.csv
│   ├── reconciliation_results.csv
│   ├── reconciliation_report.csv
│   └── reconciliation_summary.csv
│
├── src/
│   ├── app.py
│   ├── generate_data.py
│   ├── reconciliation.py
│   ├── reconciliation_engine.py
│   └── test_engine.py
│
├── Payment_Reconciliation_Analysis.xlsx
├── PBI.pbix
├── requirements.txt
├── .gitignore
└── README.md
```

##  How It Works

### 1. Load Payment Data

The system reads payment transaction data from `payments.csv`.

### 2. Load Settlement Data

Settlement information is loaded from `settlements.csv`.

### 3. Clean Settlement Records

Duplicate settlement records are identified and handled before reconciliation.

### 4. Match Transactions

Payment and settlement records are matched using the `order_id`.

### 5. Calculate Differences

The system calculates:

```text
Difference = Payment Amount - Settled Amount
```

### 6. Determine Reconciliation Status

Each transaction receives a reconciliation status:

* `MATCHED`
* `AMOUNT MISMATCH`
* `MISSING SETTLEMENT`

Additional settlement-side exceptions are also reported:

* `UNMATCHED SETTLEMENT`
* `DUPLICATE SETTLEMENT`

### 7. Generate Reports

The reconciliation engine produces:

* Reconciliation results
* Exception report
* Reconciliation summary

### 8. Ask Questions Using AI

The Streamlit application sends the relevant reconciliation context to Gemini so users can ask questions using natural language.

##  Streamlit Application

The Streamlit dashboard provides:

* Reconciliation overview
* Total payment amount
* Matched transactions
* Exception transactions
* Amount mismatches
* Missing settlements
* Mismatch amount
* Reconciliation status chart
* Exception transaction table
* AI Finance Assistant

##  Power BI Dashboard

A Power BI dashboard was created to analyze the reconciliation data visually.

Key dashboard metrics include:

* Total Payments
* Total Payment Amount
* Total Settled Amount
* Reconciliation Rate
* Exception Rate
* Matched Transactions
* Exception Transactions
* Total Mismatch Amount
* Average Settlement Delay

The dashboard also includes reconciliation status and settlement analysis visuals.

##  Testing

The reconciliation engine was tested using the synthetic payment and settlement dataset.

Expected results:

```text
Total Payments: 120
Matched Transactions: 108
Amount Mismatches: 6
Missing Settlements: 6
Total Mismatch Amount: 600.0
```

The engine test completed successfully.

##  Security

The Gemini API key is **not stored in the source code**.

It is accessed through the environment variable:

```text
GEMINI_API_KEY
```

Sensitive files and environment secrets are excluded through `.gitignore`.

## ▶️ Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/priyanka2005-s/ai-payment-reconciliation-finance-controller.git
cd ai-payment-reconciliation-finance-controller
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set the Gemini API key

Set the `GEMINI_API_KEY` environment variable on your system.

### 4. Run the Streamlit application

```bash
streamlit run src/app.py
```

The application will open in your browser.

##  Business Value

This project demonstrates how automation and AI can support finance operations by:

* Reducing manual reconciliation effort
* Identifying financial exceptions quickly
* Providing structured exception reports
* Making reconciliation data easier to understand
* Allowing finance users to ask questions in natural language
* Combining traditional data processing with generative AI

## Future Improvements

Potential future improvements include:

* Upload payment and settlement files directly through the UI
* Automated reconciliation scheduling
* Database integration
* Role-based access control
* Automated exception alerts
* Larger datasets and performance benchmarking
* More advanced AI-based financial analysis
* Deployment to a cloud platform

##  Author

**Priyanka**

Built as a practical AI + Finance automation project demonstrating Python, data analysis, reconciliation logic, generative AI, Streamlit, and Power BI.
