import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CYAC Analytics Dashboard", layout="wide")

st.title("CYAC Analytics Dashboard")
st.markdown(
    "Upload an **anonymized CSV file** for CYAC analysis. "
    "This app is designed for cleaned data only — do not upload raw personal identifiers."
)

with st.expander("Recommended safe structure"):
    st.markdown(
        """
        **Use anonymized data only**, such as:
        - `PT_ID` instead of full names
        - `Interview_Date` or `Month`
        - `Fiscal_Year`
        - `Agency`
        - `Meeting_Count`
        - `Interview_Count`
        - `Case_Type` (if safe and approved)

        You can upload either:
        1. **Record-level data** (one row per activity/interview), or
        2. **Summary data** (monthly counts by agency / fiscal year)
        """
    )

uploaded_file = st.file_uploader("Upload anonymized CSV file", type=["csv"])

if uploaded_file is None:
    st.info("Please upload your cleaned CYAC CSV file to begin.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

st.subheader("Raw Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

st.divider()
st.subheader("Column Mapping")
st.caption("Select the columns that match your file. Leave blank if a field is not available.")

all_columns = [""] + df.columns.tolist()

col1, col2, col3 = st.columns(3)
with col1:
    date_col = st.selectbox("Date column", all_columns, index=all_columns.index("Interview_Date") if "Interview_Date" in all_columns else 0)
    month_col = st.selectbox("Month column", all_columns, index=all_columns.index("Month") if "Month" in all_columns else 0)
    fy_col = st.selectbox("Fiscal year column", all_columns, index=all_columns.index("Fiscal_Year") if "Fiscal_Year" in all_columns else 0)
with col2:
    agency_col = st.selectbox("Agency column", all_columns, index=all_columns.index("Agency") if "Agency" in all_columns else 0)
    ptid_col = st.selectbox("PT_ID column", all_columns, index=all_columns.index("PT_ID") if "PT_ID" in all_columns else 0)
    category_col = st.selectbox("Category column", all_columns, index=all_columns.index("Case_Type") if "Case_Type" in all_columns else 0)
with col3:
    count_col = st.selectbox("Count column", all_columns, index=all_columns.index("Meeting_Count") if "Meeting_Count" in all_columns else 0)

clean_df = df.copy()

# Normalize optional date column
if date_col:
    clean_df[date_col] = pd.to_datetime(clean_df[date_col], errors="coerce")
    clean_df = clean_df.dropna(subset=[date_col]).copy()
    clean_df["Year"] = clean_df[date_col].dt.year
    clean_df["Month_Name"] = clean_df[date_col].dt.strftime("%B")

# Normalize count column
if count_col:
    clean_df[count_col] = pd.to_numeric(clean_df[count_col], errors="coerce")

# Sidebar filters
st.sidebar.header("Filters")
filtered_df = clean_df.copy()

if fy_col:
    fy_values = sorted(filtered_df[fy_col].dropna().astype(str).unique().tolist())
    selected_fy = st.sidebar.multiselect("Fiscal Year", fy_values, default=fy_values)
    if selected_fy:
        filtered_df = filtered_df[filtered_df[fy_col].astype(str).isin(selected_fy)]

if agency_col:
    agency_values = sorted(filtered_df[agency_col].dropna().astype(str).unique().tolist())
    selected_agency = st.sidebar.multiselect("Agency", agency_values, default=agency_values)
    if selected_agency:
        filtered_df = filtered_df[filtered_df[agency_col].astype(str).isin(selected_agency)]

if month_col:
    month_values = filtered_df[month_col].dropna().astype(str).unique().tolist()
    selected_months = st.sidebar.multiselect("Month", month_values, default=month_values)
    if selected_months:
        filtered_df = filtered_df[filtered_df[month_col].astype(str).isin(selected_months)]
elif "Month_Name" in filtered_df.columns:
    month_values = filtered_df["Month_Name"].dropna().astype(str).unique().tolist()
    selected_months = st.sidebar.multiselect("Month", month_values, default=month_values)
    if selected_months:
        filtered_df = filtered_df[filtered_df["Month_Name"].astype(str).isin(selected_months)]

if category_col:
    category_values = sorted(filtered_df[category_col].dropna().astype(str).unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", category_values, default=category_values)
    if selected_categories:
        filtered_df = filtered_df[filtered_df[category_col].astype(str).isin(selected_categories)]

if filtered_df.empty:
    st.warning("No records available for the selected filters.")
    st.stop()

st.subheader("Project Summary")
st.write(
    "This dashboard helps review anonymized CYAC activity data, monitor trends across time, "
    "summarize records by agency or fiscal year, and create safe visuals for presentations."
)

# Metrics
rows_count = len(filtered_df)
unique_people = filtered_df[ptid_col].nunique() if ptid_col else None
unique_agencies = filtered_df[agency_col].nunique() if agency_col else None

if count_col:
    total_activity = filtered_df[count_col].fillna(0).sum()
else:
    total_activity = rows_count

m1, m2, m3, m4 = st.columns(4)
m1.metric("Rows", f"{rows_count:,}")
m2.metric("Total Activity", f"{int(total_activity):,}" if pd.notna(total_activity) else "N/A")
m3.metric("Unique PT_IDs", f"{unique_people:,}" if unique_people is not None else "N/A")
m4.metric("Agencies", f"{unique_agencies:,}" if unique_agencies is not None else "N/A")

st.divider()
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(50), use_container_width=True)

# Summary tables
left, right = st.columns(2)

with left:
    st.subheader("Summary Table")
    if agency_col and count_col:
        agency_summary = (
            filtered_df.groupby(agency_col, as_index=False)[count_col]
            .sum()
            .sort_values(count_col, ascending=False)
        )
        st.dataframe(agency_summary, use_container_width=True)
    elif agency_col:
        agency_summary = (
            filtered_df.groupby(agency_col)
            .size()
            .reset_index(name="Record_Count")
            .sort_values("Record_Count", ascending=False)
        )
        st.dataframe(agency_summary, use_container_width=True)
    else:
        st.info("Select an Agency column to see agency summary.")

with right:
    st.subheader("Fiscal Year / Month Summary")
    if fy_col and count_col:
        fy_summary = (
            filtered_df.groupby(fy_col, as_index=False)[count_col]
            .sum()
            .sort_values(fy_col)
        )
        st.dataframe(fy_summary, use_container_width=True)
    elif fy_col:
        fy_summary = (
            filtered_df.groupby(fy_col)
            .size()
            .reset_index(name="Record_Count")
            .sort_values(fy_col)
        )
        st.dataframe(fy_summary, use_container_width=True)
    else:
        st.info("Select a Fiscal Year column to see year summary.")

st.divider()
st.subheader("Visualizations")

# Chart 1: Agency distribution
if agency_col:
    if count_col:
        chart_df = filtered_df.groupby(agency_col)[count_col].sum().sort_values(ascending=False)
        ylabel = count_col
    else:
        chart_df = filtered_df.groupby(agency_col).size().sort_values(ascending=False)
        ylabel = "Record Count"

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    chart_df.plot(kind="bar", ax=ax1)
    ax1.set_title("Activity by Agency")
    ax1.set_xlabel("Agency")
    ax1.set_ylabel(ylabel)
    ax1.tick_params(axis="x", rotation=45)
    st.pyplot(fig1)
else:
    st.info("Add an Agency column to generate the agency chart.")

# Chart 2: Trend over time
trend_source = None
if month_col:
    trend_source = month_col
elif "Month_Name" in filtered_df.columns:
    trend_source = "Month_Name"
elif fy_col:
    trend_source = fy_col

if trend_source:
    if count_col:
        trend_df = filtered_df.groupby(trend_source)[count_col].sum()
        ylabel = count_col
    else:
        trend_df = filtered_df.groupby(trend_source).size()
        ylabel = "Record Count"

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    trend_df.plot(kind="line", marker="o", ax=ax2)
    ax2.set_title("Trend Overview")
    ax2.set_xlabel(trend_source)
    ax2.set_ylabel(ylabel)
    ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2)

# Chart 3: Category breakdown
if category_col:
    if count_col:
        cat_df = filtered_df.groupby(category_col)[count_col].sum().sort_values(ascending=False)
        ylabel = count_col
    else:
        cat_df = filtered_df.groupby(category_col).size().sort_values(ascending=False)
        ylabel = "Record Count"

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    cat_df.plot(kind="bar", ax=ax3)
    ax3.set_title("Category Breakdown")
    ax3.set_xlabel(category_col)
    ax3.set_ylabel(ylabel)
    ax3.tick_params(axis="x", rotation=45)
    st.pyplot(fig3)

st.divider()
st.subheader("Download Filtered Data")
output_csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=output_csv,
    file_name="cyac_filtered_data.csv",
    mime="text/csv"
)
