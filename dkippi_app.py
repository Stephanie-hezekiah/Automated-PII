# =============================================================================
# DKIPPI PII DISCOVERY & AUDIT TOOL — Streamlit Web App
# NDPA 2023 Compliance Scanner
# Authors: Hezekiah Stephanie & Adeoye Rachael
# Run with: streamlit run dkippi_app.py
# =============================================================================

import streamlit as st
import pandas as pd
import re
import os
import io
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors as rl_colors
from reportlab.lib.pagesizes import A4
from datetime import datetime

# =============================================================================
# PAGE CONFIG & STYLING
# =============================================================================

st.set_page_config(
    page_title="DKIPPI PII Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

/* Main background */
.stApp {
    background-color: #0a0f1e;
    color: #e2e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1424;
    border-right: 1px solid #1e3a5f;
}

/* Header */
.dkippi-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2f4a 50%, #0d1b2a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.dkippi-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(30, 58, 95, 0.15) 2px,
        rgba(30, 58, 95, 0.15) 4px
    );
    pointer-events: none;
}
.dkippi-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0;
}
.dkippi-title span {
    color: #38bdf8;
}
.dkippi-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #64748b;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.ndpa-badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 3px;
    margin-top: 0.6rem;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-card {
    background: #0d1424;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 8px 0 0 8px;
}
.metric-card.blue::after  { background: #38bdf8; }
.metric-card.red::after   { background: #ef4444; }
.metric-card.amber::after { background: #f59e0b; }
.metric-card.green::after { background: #22c55e; }

.metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.metric-sub {
    font-size: 0.65rem;
    color: #475569;
    margin-top: 0.3rem;
}

/* Risk badges */
.risk-high   { background:#ef444420; color:#ef4444; border:1px solid #ef444440; padding:2px 8px; border-radius:3px; font-size:0.7rem; font-weight:600; letter-spacing:0.08em; }
.risk-medium { background:#f59e0b20; color:#f59e0b; border:1px solid #f59e0b40; padding:2px 8px; border-radius:3px; font-size:0.7rem; font-weight:600; letter-spacing:0.08em; }
.risk-low    { background:#22c55e20; color:#22c55e; border:1px solid #22c55e40; padding:2px 8px; border-radius:3px; font-size:0.7rem; font-weight:600; letter-spacing:0.08em; }
.risk-none   { background:#64748b20; color:#64748b; border:1px solid #64748b40; padding:2px 8px; border-radius:3px; font-size:0.7rem; font-weight:600; letter-spacing:0.08em; }

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
}

/* Upload zone */
.uploadedFile { background: #0d1424 !important; border: 1px dashed #1e3a5f !important; }

/* Streamlit overrides */
div[data-testid="stMetric"] { background: #0d1424; border: 1px solid #1e3a5f; border-radius: 8px; padding: 1rem; }
.stDataFrame { border: 1px solid #1e3a5f; border-radius: 8px; }
div[data-testid="stAlert"] { border-radius: 8px; }

button[kind="primary"] {
    background: #38bdf8 !important;
    color: #0a0f1e !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 6px !important;
}

.stSelectbox > div > div { background: #0d1424 !important; border-color: #1e3a5f !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# PII PATTERNS & RISK LOGIC
# =============================================================================

COLUMN_PATTERNS = {
    "NIN":          r'^\d{11}$',
    "BVN":          r'^\d{11}$',
    "PHONE NUMBER": r'^(070|080|081|090|091)\d{8}$',
}

LABELED_PATTERNS = {
    "NIN":   r'NIN[:\s\-]*(\d{11})',
    "BVN":   r'BVN[:\s\-]*(\d{11})',
    "Phone": r'\b(070|080|081|090|091)\d{8}\b',
}

COLUMN_MAP = {
    "NIN": "NIN", "Nin": "NIN", "nin": "NIN", "National_ID": "NIN",
    "BVN": "BVN", "Bvn": "BVN", "bvn": "BVN", "Bank_Verification": "BVN",
    "PHONE NUMBER": "PHONE NUMBER", "Phone": "PHONE NUMBER",
    "PhoneNumber": "PHONE NUMBER", "Mobile": "PHONE NUMBER",
    "phone_number": "PHONE NUMBER", "PHONE": "PHONE NUMBER",
}

RISK_COLORS = {
    "HIGH": "#ef4444",
    "MEDIUM": "#f59e0b",
    "LOW": "#22c55e",
    "NO RISK": "#64748b",
}


def calculate_weighted_risk(nin, bvn, phone):
    score = (nin * 5) + (bvn * 5) + (phone * 2)
    if score == 0:   level = "NO RISK"
    elif score <= 10: level = "LOW"
    elif score <= 30: level = "MEDIUM"
    else:             level = "HIGH"
    return score, level


def risk_badge_html(level):
    cls = {"HIGH": "risk-high", "MEDIUM": "risk-medium",
           "LOW": "risk-low"}.get(level, "risk-none")
    return f'<span class="{cls}">{level}</span>'


# =============================================================================
# SCANNING FUNCTIONS
# =============================================================================

def preprocess_df(df):
    df = df.rename(columns=COLUMN_MAP)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
    return df


def scan_structured(df, source_name="uploaded file"):
    df = preprocess_df(df)
    available = [c for c in COLUMN_PATTERNS if c in df.columns]
    findings = []

    for index, row in df.iterrows():
        detected = []
        for col in available:
            val = str(row.get(col, "")).strip()
            if val and val.lower() not in ("nan", "none", ""):
                if re.match(COLUMN_PATTERNS[col], val):
                    detected.append(col)

        if detected:
            nin_f  = 1 if "NIN" in detected else 0
            bvn_f  = 1 if "BVN" in detected else 0
            ph_f   = 1 if "PHONE NUMBER" in detected else 0
            score, level = calculate_weighted_risk(nin_f, bvn_f, ph_f)
            findings.append({
                "Row":          index + 2,
                "Name":         row.get("NAME", row.get("Name", row.get("name", "—"))),
                "Detected PII": ", ".join(detected),
                "NIN":          "✓" if nin_f else "—",
                "BVN":          "✓" if bvn_f else "—",
                "Phone":        "✓" if ph_f  else "—",
                "Risk Score":   score,
                "Risk Level":   level,
            })

    return pd.DataFrame(findings), available


def scan_freetext(file_bytes, filename):
    ext = os.path.splitext(filename)[1].lower()
    try:
        if ext == ".csv":
            text = pd.read_csv(io.BytesIO(file_bytes), dtype=str).to_string()
        elif ext in (".xlsx", ".xlsm"):
            text = pd.read_excel(io.BytesIO(file_bytes), dtype=str).to_string()
        elif ext == ".txt":
            text = file_bytes.decode("utf-8", errors="ignore")
        else:
            return None
    except Exception:
        return None

    counts = {}
    for pii_type, pattern in LABELED_PATTERNS.items():
        counts[pii_type] = len(re.findall(pattern, text, re.IGNORECASE))
    return counts


# =============================================================================
# CHART FUNCTIONS
# =============================================================================

def make_risk_pie(df):
    counts = df["Risk Level"].value_counts()
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="#0d1424")
    ax.set_facecolor("#0d1424")
    wedge_colors = [RISK_COLORS.get(l, "#64748b") for l in counts.index]
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=None,
        colors=wedge_colors, autopct="%1.0f%%",
        startangle=140, pctdistance=0.75,
        wedgeprops=dict(linewidth=2, edgecolor="#0a0f1e")
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(10)
    ax.legend(counts.index, loc="lower center", ncol=2,
              frameon=False, labelcolor="white", fontsize=8)
    ax.set_title("Risk Distribution", color="white", fontsize=11, pad=10)
    plt.tight_layout()
    return fig


def make_bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#0d1424")
    ax.set_facecolor("#0a0f1e")
    bar_colors = [RISK_COLORS.get(str(r), "#38bdf8")
                  for r in df.get("Risk Level", df.get("Risk_Level", ["NO RISK"] * len(df)))]
    ax.bar(df[x_col].astype(str), df[y_col], color=bar_colors,
           edgecolor="#0a0f1e", linewidth=1.5, width=0.6)
    ax.set_title(title, color="white", fontsize=11, pad=10)
    ax.set_xlabel(x_col, color="#64748b", fontsize=8)
    ax.set_ylabel(y_col, color="#64748b", fontsize=8)
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.spines[:].set_color("#1e3a5f")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    return fig


def make_pii_breakdown(df):
    """Stacked bar: NIN / BVN / Phone per file."""
    fig, ax = plt.subplots(figsize=(8, 4), facecolor="#0d1424")
    ax.set_facecolor("#0a0f1e")
    x = df["File_Name"] if "File_Name" in df.columns else df.index.astype(str)
    nin   = df.get("NIN_Count",   [0]*len(df))
    bvn   = df.get("BVN_Count",   [0]*len(df))
    phone = df.get("Phone_Count", [0]*len(df))
    ax.bar(x, nin,   color="#38bdf8", label="NIN",   width=0.5)
    ax.bar(x, bvn,   color="#818cf8", label="BVN",   bottom=nin, width=0.5)
    ax.bar(x, phone, color="#f472b6", label="Phone", bottom=[i+j for i,j in zip(nin,bvn)], width=0.5)
    ax.legend(frameon=False, labelcolor="white", fontsize=8)
    ax.set_title("PII Type Breakdown per File", color="white", fontsize=11, pad=10)
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.spines[:].set_color("#1e3a5f")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    return fig


# =============================================================================
# PDF REPORT GENERATOR
# =============================================================================

def generate_pdf(findings_df, summary_df, scan_mode, target_name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=50, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("t", parent=styles["Title"], fontSize=16, spaceAfter=4)
    h2_style    = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, spaceAfter=6, textColor=rl_colors.HexColor("#003366"))
    body_style  = styles["Normal"]
    content     = []
    ts          = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content.append(Paragraph("DKIPPI PII Compliance Audit Report", title_style))
    content.append(Paragraph(f"Generated: {ts}  |  Scan Target: {target_name}", body_style))
    content.append(Spacer(1, 14))

    # Summary stats
    content.append(Paragraph("Executive Summary", h2_style))
    if scan_mode == "structured" and not findings_df.empty:
        high = len(findings_df[findings_df["Risk Level"] == "HIGH"])
        med  = len(findings_df[findings_df["Risk Level"] == "MEDIUM"])
        content.append(Paragraph(f"Total rows with PII detected: {len(findings_df)}", body_style))
        content.append(Paragraph(f"HIGH risk rows: {high}", body_style))
        content.append(Paragraph(f"MEDIUM risk rows: {med}", body_style))
    elif scan_mode == "directory" and not summary_df.empty:
        high = len(summary_df[summary_df["Risk_Level"] == "HIGH"])
        content.append(Paragraph(f"Total files scanned: {len(summary_df)}", body_style))
        content.append(Paragraph(f"HIGH risk files: {high}", body_style))
        content.append(Paragraph(f"Total PII instances: {summary_df['Total_PII'].sum()}", body_style))

    content.append(Spacer(1, 12))

    # Table
    ref_df = findings_df if scan_mode == "structured" else summary_df
    if not ref_df.empty:
        content.append(Paragraph("Detailed Findings", h2_style))
        safe_cols = [c for c in ref_df.columns if c != "File_Path"]
        tdata = [safe_cols] + ref_df[safe_cols].astype(str).values.tolist()
        tbl = Table(tdata, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0),  rl_colors.HexColor("#003366")),
            ("TEXTCOLOR",     (0,0), (-1,0),  rl_colors.white),
            ("FONTSIZE",      (0,0), (-1,0),  8),
            ("FONTSIZE",      (0,1), (-1,-1), 7),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [rl_colors.white, rl_colors.HexColor("#f0f4f8")]),
            ("GRID",          (0,0), (-1,-1), 0.4, rl_colors.grey),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ]))
        content.append(tbl)

    content.append(Spacer(1, 20))
    content.append(Paragraph(
        "This report was automatically generated by the DKIPPI PII Discovery Tool "
        "in support of NDPA 2023 compliance obligations. Handle this report as confidential.",
        styles["Italic"]
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem 0'>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff'>
            DKIPPI
        </div>
        <div style='font-size:0.6rem;letter-spacing:0.15em;color:#475569;text-transform:uppercase'>
            PII Audit Tool v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    scan_mode = st.radio(
        "Scan Mode",
        ["Single File (Row-by-Row)", "Multiple Files (Directory)"],
        help="Row-by-Row: deep scan of one structured file. Directory: broad scan across many files."
    )

    st.divider()
    st.markdown("<div style='font-size:0.65rem;color:#475569;letter-spacing:0.1em;text-transform:uppercase'>Column Mapping</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#64748b;margin-top:0.3rem'>If your file uses non-standard column names, map them below.</div>", unsafe_allow_html=True)

    custom_nin   = st.text_input("NIN column name in your file",   value="NIN",          key="cn")
    custom_bvn   = st.text_input("BVN column name in your file",   value="BVN",          key="cb")
    custom_phone = st.text_input("Phone column name in your file", value="PHONE NUMBER",  key="cp")

    if custom_nin:   COLUMN_MAP[custom_nin]   = "NIN"
    if custom_bvn:   COLUMN_MAP[custom_bvn]   = "BVN"
    if custom_phone: COLUMN_MAP[custom_phone] = "PHONE NUMBER"

    st.divider()
    st.markdown("""
    <div style='font-size:0.65rem;color:#334155;line-height:1.6'>
        Supported formats: <span style='color:#38bdf8'>.csv  .xlsx  .txt</span><br>
        Detects: NIN · BVN · Nigerian Phone Numbers<br>
        Compliant with: <span style='color:#38bdf8'>NDPA 2023</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN CONTENT
# =============================================================================

st.markdown("""
<div class="dkippi-header">
    <div class="dkippi-title">DKIPPI <span>PII</span> Scanner</div>
    <div class="dkippi-subtitle">Automated PII Discovery & Audit Tool · TYIMS / DKIPPI</div>
    <div class="ndpa-badge">NDPA 2023 Compliant</div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# MODE A: SINGLE FILE
# =============================================================================

if scan_mode == "Single File (Row-by-Row)":

    st.markdown("<div class='section-header'>Upload File</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload a CSV or Excel file containing Nigerian records",
        type=["csv", "xlsx", "xlsm"],
        help="Your file should contain columns like NIN, BVN, PHONE NUMBER (or configure custom names in the sidebar)"
    )

    if uploaded:
        # Load file
        try:
            ext = os.path.splitext(uploaded.name)[1].lower()
            if ext == ".csv":
                raw_df = pd.read_csv(uploaded, dtype=str)
            else:
                raw_df = pd.read_excel(uploaded, dtype=str)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

        st.success(f"✓ Loaded **{uploaded.name}** — {len(raw_df):,} rows × {len(raw_df.columns)} columns")

        with st.expander("Preview raw data (first 5 rows)"):
            st.dataframe(raw_df.head(), use_container_width=True)

        # Run scan
        with st.spinner("Scanning for PII..."):
            findings, detected_cols = scan_structured(raw_df.copy(), uploaded.name)

        if detected_cols:
            st.info(f"PII columns detected in your file: **{', '.join(detected_cols)}**")
        else:
            st.warning("No recognised PII columns found. Check your column names match the sidebar settings.")
            st.stop()

        # ---- METRICS ----
        total_rows  = len(raw_df)
        pii_rows    = len(findings)
        high_count  = len(findings[findings["Risk Level"] == "HIGH"])  if not findings.empty else 0
        med_count   = len(findings[findings["Risk Level"] == "MEDIUM"]) if not findings.empty else 0

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card blue">
                <div class="metric-label">Total Rows Scanned</div>
                <div class="metric-value">{total_rows:,}</div>
                <div class="metric-sub">records processed</div>
            </div>
            <div class="metric-card red">
                <div class="metric-label">PII Rows Found</div>
                <div class="metric-value">{pii_rows:,}</div>
                <div class="metric-sub">{pii_rows/total_rows*100:.1f}% of total</div>
            </div>
            <div class="metric-card red">
                <div class="metric-label">HIGH Risk Rows</div>
                <div class="metric-value">{high_count:,}</div>
                <div class="metric-sub">immediate attention required</div>
            </div>
            <div class="metric-card amber">
                <div class="metric-label">MEDIUM Risk Rows</div>
                <div class="metric-value">{med_count:,}</div>
                <div class="metric-sub">review recommended</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if findings.empty:
            st.success("✓ No PII detected in this file.")
        else:
            # ---- CHARTS ----
            st.markdown("<div class='section-header'>Risk Analysis</div>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])

            with col1:
                st.pyplot(make_risk_pie(findings), use_container_width=True)

            with col2:
                risk_counts = findings.groupby("Risk Level").size().reset_index(name="Count")
                risk_counts["Risk Level_sort"] = risk_counts["Risk Level"].map(
                    {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "NO RISK": 3}
                )
                risk_counts = risk_counts.sort_values("Risk Level_sort")
                fig = make_bar_chart(risk_counts, "Risk Level", "Count", "Rows by Risk Level")
                st.pyplot(fig, use_container_width=True)

            # ---- FINDINGS TABLE ----
            st.markdown("<div class='section-header'>Detailed Findings</div>", unsafe_allow_html=True)

            filter_col1, filter_col2 = st.columns([2, 1])
            with filter_col1:
                risk_filter = st.multiselect(
                    "Filter by Risk Level",
                    options=findings["Risk Level"].unique().tolist(),
                    default=findings["Risk Level"].unique().tolist()
                )
            with filter_col2:
                search = st.text_input("Search by name", placeholder="e.g. Adeyemi")

            filtered = findings[findings["Risk Level"].isin(risk_filter)]
            if search:
                filtered = filtered[filtered["Name"].str.contains(search, case=False, na=False)]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Risk Level": st.column_config.TextColumn("Risk Level"),
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score", min_value=0, max_value=20, format="%d"
                    ),
                }
            )

            # ---- DOWNLOADS ----
            st.markdown("<div class='section-header'>Export Reports</div>", unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)

            with dl1:
                csv_data = findings.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇ Download CSV Report",
                    data=csv_data,
                    file_name=f"DKIPPI_PII_Findings_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with dl2:
                pdf_buffer = generate_pdf(findings, pd.DataFrame(), "structured", uploaded.name)
                st.download_button(
                    "⬇ Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"DKIPPI_Compliance_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )


# =============================================================================
# MODE B: MULTIPLE FILES
# =============================================================================

else:
    st.markdown("<div class='section-header'>Upload Multiple Files</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload all files you want to scan (CSV, Excel, TXT)",
        type=["csv", "xlsx", "xlsm", "txt"],
        accept_multiple_files=True,
        help="Upload multiple files at once to scan an entire directory of records"
    )

    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} file(s) uploaded — ready to scan")

        if st.button("▶ Run Directory Scan", type="primary", use_container_width=False):
            summary_rows = []
            progress = st.progress(0, text="Scanning files...")

            for i, f in enumerate(uploaded_files):
                file_bytes = f.read()
                counts = scan_freetext(file_bytes, f.name)
                progress.progress((i + 1) / len(uploaded_files),
                                   text=f"Scanning {f.name}...")

                if counts is not None:
                    total = sum(counts.values())
                    score, level = calculate_weighted_risk(
                        counts.get("NIN", 0), counts.get("BVN", 0), counts.get("Phone", 0)
                    )
                    summary_rows.append({
                        "File_Name":   f.name,
                        "NIN_Count":   counts.get("NIN", 0),
                        "BVN_Count":   counts.get("BVN", 0),
                        "Phone_Count": counts.get("Phone", 0),
                        "Total_PII":   total,
                        "Risk_Score":  score,
                        "Risk_Level":  level,
                    })

            progress.empty()
            summary = pd.DataFrame(summary_rows)
            st.session_state["dir_summary"] = summary

        # Show results if available
        if "dir_summary" in st.session_state:
            summary = st.session_state["dir_summary"]

            if summary.empty:
                st.info("No PII detected across the uploaded files.")
            else:
                # ---- METRICS ----
                total_files  = len(summary)
                high_files   = len(summary[summary["Risk_Level"] == "HIGH"])
                total_pii    = int(summary["Total_PII"].sum())
                top_risk_file = summary.loc[summary["Risk_Score"].idxmax(), "File_Name"]

                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card blue">
                        <div class="metric-label">Files Scanned</div>
                        <div class="metric-value">{total_files}</div>
                        <div class="metric-sub">total files processed</div>
                    </div>
                    <div class="metric-card red">
                        <div class="metric-label">HIGH Risk Files</div>
                        <div class="metric-value">{high_files}</div>
                        <div class="metric-sub">require immediate action</div>
                    </div>
                    <div class="metric-card amber">
                        <div class="metric-label">Total PII Instances</div>
                        <div class="metric-value">{total_pii:,}</div>
                        <div class="metric-sub">across all files</div>
                    </div>
                    <div class="metric-card red">
                        <div class="metric-label">Highest Risk File</div>
                        <div class="metric-value" style="font-size:0.9rem;margin-top:4px">{top_risk_file}</div>
                        <div class="metric-sub">most PII detected</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ---- CHARTS ----
                st.markdown("<div class='section-header'>Visual Analysis</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)

                with c1:
                    fig1 = make_bar_chart(summary, "File_Name", "Total_PII",
                                          "Total PII per File")
                    st.pyplot(fig1, use_container_width=True)

                with c2:
                    fig2 = make_pii_breakdown(summary)
                    st.pyplot(fig2, use_container_width=True)

                # ---- SUMMARY TABLE ----
                st.markdown("<div class='section-header'>File Summary</div>", unsafe_allow_html=True)
                st.dataframe(
                    summary,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Risk_Score": st.column_config.ProgressColumn(
                            "Risk Score", min_value=0, max_value=100, format="%d"
                        ),
                    }
                )

                # ---- DOWNLOADS ----
                st.markdown("<div class='section-header'>Export Reports</div>", unsafe_allow_html=True)
                dl1, dl2 = st.columns(2)

                with dl1:
                    csv_data = summary.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇ Download CSV Report",
                        data=csv_data,
                        file_name=f"DKIPPI_Directory_Scan_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

                with dl2:
                    pdf_buf = generate_pdf(
                        pd.DataFrame(), summary, "directory",
                        f"{len(uploaded_files)} uploaded files"
                    )
                    st.download_button(
                        "⬇ Download PDF Report",
                        data=pdf_buf,
                        file_name=f"DKIPPI_Compliance_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top:1px solid #1e3a5f;padding-top:1rem;display:flex;justify-content:space-between;align-items:center'>
    <div style='font-size:0.65rem;color:#334155'>
        DKIPPI PII Discovery Tool · Built for NDPA 2023 Compliance · TYIMS / DKIPPI
    </div>
    <div style='font-size:0.65rem;color:#334155'>
        Detects: NIN · BVN · Nigerian Phone Numbers
    </div>
</div>
""", unsafe_allow_html=True)
