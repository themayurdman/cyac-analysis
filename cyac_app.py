import streamlit as st
import pandas as pd

st.set_page_config(page_title="CYAC Analysis", layout="wide")

st.title("CYAC Data Analysis Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your cleaned CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip()

    st.subheader("Raw Data")
    st.dataframe(df)

    # Convert date columns
    if 'Date of contact' in df.columns:
        df['Date of contact'] = pd.to_datetime(df['Date of contact'], errors='coerce')

    if 'Next Contact Date' in df.columns:
        df['Next Contact Date'] = pd.to_datetime(df['Next Contact Date'], errors='coerce')

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Cases", df['Case ID'].nunique())

    with col2:
        st.metric("Total Records", len(df))

    # Case Type Chart
    if 'Case Note Type' in df.columns:
        st.subheader("Case Type Distribution")
        st.bar_chart(df['Case Note Type'].value_counts())

    # Location Chart
    if 'Location of contact' in df.columns:
        st.subheader("Location Distribution")
        st.bar_chart(df['Location of contact'].value_counts())

    # Time Trend
    if 'Date of contact' in df.columns:
        st.subheader("Contacts Over Time")
        trend = df.groupby('Date of contact').size()
        st.line_chart(trend)

else:
    st.info("Please upload a CSV file to begin analysis.")
