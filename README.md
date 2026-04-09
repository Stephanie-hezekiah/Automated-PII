# DKIPPI PII Scanner — Setup Guide

## What This App Does
A web-based tool for DKIPPI and TYIMS to automatically scan files for Nigerian PII
(NIN, BVN, Phone Numbers) and generate compliance reports under NDPA 2023.

---

## How to Run Locally (Your Own Computer)

### Step 1 — Install Python
Download Python 3.10 or newer from https://python.org if you don't have it.

### Step 2 — Install dependencies
Open your terminal (Command Prompt on Windows) and run:
```
pip install -r requirements.txt
```

### Step 3 — Run the app
```
streamlit run dkippi_app.py
```

The app will open automatically in your browser at http://localhost:8501

---

## How to Deploy Online (Free — Streamlit Cloud)

1. Create a free account at https://streamlit.io/cloud
2. Upload both files (`dkippi_app.py` and `requirements.txt`) to a GitHub repository
3. In Streamlit Cloud, click "New App" → connect your GitHub repo → select `dkippi_app.py`
4. Click Deploy — your app will be live at a public URL within 2 minutes

---

## How to Use the App

### Single File Mode (Row-by-Row)
- Upload one CSV or Excel file
- The app scans every row for NIN, BVN, and phone number patterns
- View risk levels per row, filter by risk, search by name
- Download findings as CSV or PDF

### Multiple Files Mode (Directory)
- Upload several files at once
- The app scans each file's full text for labelled PII (e.g. "NIN: 12345678901")
- See which files contain the most PII and their risk levels
- Download a summary report

### Custom Column Names
If your file uses different column headers (e.g. "Mobile" instead of "PHONE NUMBER"),
enter your column names in the sidebar before scanning.

---

## Files Included
- `dkippi_app.py`     — The full Streamlit web application
- `requirements.txt` — Python package dependencies
- `README.md`        — This setup guide
