import streamlit as st
import pandas as pd
from datetime import datetime


def get_txn_type(text: str) -> str:
    if not isinstance(text, str):
        return "unknown"
    t = text.lower()
    if "debited" in t or "spent" in t or "paid" in t or "purchase" in t:
        return "debit"
    if "credited" in t or "received" in t:
        return "credit"
    return "unknown"

def parse_date(s):
    if not isinstance(s, str) or not s.strip():
        return None
    for fmt in (
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
        "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M",
        "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"
    ):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None



st.set_page_config(page_title="Analyzer", layout="wide")
st.title("Spend Analyzer")

uploaded_file = st.file_uploader("Upload transactions.csv / transactions_cleaned.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)


    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])


    required_cols = ["amount", "raw_message"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    if "txn_type" not in df.columns:
        st.warning("Column 'txn_type' not found. Inferring debit/credit from raw_message.")
        df["txn_type"] = df["raw_message"].apply(get_txn_type)
    else:
        df["txn_type"] = df["txn_type"].fillna(df["raw_message"].apply(get_txn_type))

    if "merchant" not in df.columns:
        st.warning("Column 'merchant' not found. Using 'sender' if available, else leaving blank.")
        if "sender" in df.columns:
            df["merchant"] = df["sender"]
        else:
            df["merchant"] = ""

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"].notnull()]

    if "date" in df.columns:
        df["date_parsed"] = df["date"].apply(parse_date)
        if df["date_parsed"].notnull().any():
            df["date_only"] = df["date_parsed"].dt.date
        else:
            df["date_parsed"] = None
    else:
        df["date_parsed"] = None

    if "Bank" in df.columns:
        st.sidebar.header("Bank Filter")
        banks = sorted(df["Bank"].dropna().unique())
        selected_banks = st.sidebar.multiselect(
            "Select bank accounts to include:",
            options=banks,
            default=banks
        )
        if selected_banks:
            df = df[df["Bank"].isin(selected_banks)]
        else:
            st.warning("No bank selected; showing no transactions.")

    total_debit = df[df["txn_type"] == "debit"]["amount"].sum()
    total_credit = df[df["txn_type"] == "credit"]["amount"].sum()

    st.header("Overall Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Debited (Spent)", f"₹ {total_debit:,.2f}")
    col2.metric("Total Credited (Received)", f"₹ {total_credit:,.2f}")

    if "Bank" in df.columns:
        st.subheader("🏦 Bank-wise Summary")
        bank_summary = (
            df.pivot_table(
                index="Bank",
                columns="txn_type",
                values="amount",
                aggfunc="sum"
            )
            .fillna(0)
        )

        if "debit" not in bank_summary.columns:
            bank_summary["debit"] = 0
        if "credit" not in bank_summary.columns:
            bank_summary["credit"] = 0

        st.dataframe(
            bank_summary.reset_index().rename(
                columns={"debit": "total_debited", "credit": "total_credited"}
            ),
            use_container_width=True
        )

    st.header("Debit Analysis")

    debit_df = df[df["txn_type"] == "debit"].copy()

    if debit_df.empty:
        st.info("No debit transactions found.")
    else:
        st.subheader("Amount debited to each name (merchant)")
        debit_by_merchant = (
            debit_df.groupby("merchant")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(
            debit_by_merchant.reset_index().rename(columns={"amount": "total_debited"}),
            use_container_width=True
        )

        st.subheader("Debit by name (bar chart)")
        st.bar_chart(debit_by_merchant)

        if debit_df["date_parsed"].notnull().any():
            st.subheader("Debit over time")
            debit_by_date = (
                debit_df[debit_df["date_parsed"].notnull()]
                .groupby("date_only")["amount"]
                .sum()
                .sort_index()
            )
            st.line_chart(debit_by_date)
        else:
            st.info("No valid dates to show debit over time.")

    st.header("Credit Analysis")

    credit_df = df[df["txn_type"] == "credit"].copy()

    if credit_df.empty:
        st.info("No credit transactions found.")
    else:
        st.subheader("👤 Amount credited from each name")
        credit_by_merchant = (
            credit_df.groupby("merchant")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(
            credit_by_merchant.reset_index().rename(columns={"amount": "total_credited"}),
            use_container_width=True
        )

        st.subheader("Credit by name (bar chart)")
        st.bar_chart(credit_by_merchant)

        # Credit over time
        if credit_df["date_parsed"].notnull().any():
            st.subheader("Credit over time")
            credit_by_date = (
                credit_df[credit_df["date_parsed"].notnull()]
                .groupby("date_only")["amount"]
                .sum()
                .sort_index()
            )
            st.line_chart(credit_by_date)
        else:
            st.info("No valid dates to show credit over time.")

else:
    st.info("👆 Upload your transactions.csv to start.")
