import streamlit as st
import pandas as pd

st.set_page_config(page_title="CYAC Analysis", layout="wide")

st.title("CYAC Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload your cleaned CSV file", type=["csv"])

if uploaded_file is not None:
    # --- Read CSV safely ---
    df = pd.read_csv(uploaded_file, encoding="utf-8", low_memory=False)

    # --- Clean column names ---
    df.columns = df.columns.str.strip()

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # --- Normalize column names (just in case) ---
    rename_map = {
        "Client Information": "Client ID",
        "Case Note Information": "Case ID"
    }
    df = df.rename(columns=rename_map)

    # --- Check required columns ---
    required_cols = [
        "Client ID", "Case ID", "Case Note Type",
        "Date of contact", "Time of contact",
        "Location of contact", "Month", "Day", "Time Bucket"
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
    else:
        st.success("File loaded successfully!")

        st.subheader("Preview Data")
        st.dataframe(df.head(20))

        # --- Metrics ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Cases", df["Case ID"].nunique())

        with col2:
            st.metric("Total Clients", df["Client ID"].nunique())

        with col3:
            st.metric("Total Records", len(df))

        st.markdown("---")

        # --- Charts ---
        st.subheader("Case Note Type Distribution")
        st.bar_chart(df["Case Note Type"].value_counts())

        st.subheader("Monthly Trend")
        if "Month" in df.columns:
            st.bar_chart(df["Month"].value_counts())

        st.subheader("Time Bucket Distribution")
        if "Time Bucket" in df.columns:
            st.bar_chart(df["Time Bucket"].value_counts())

        st.subheader("Location Distribution")
        if "Location of contact" in df.columns:
            st.bar_chart(df["Location of contact"].value_counts())
