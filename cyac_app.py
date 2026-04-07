import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title=“CAC Analytics Dashboard”, layout=“wide”, page_icon=“📊”)

# ── Custom CSS ──────────────────────────────────────────────────────────────

st.markdown(”””

<style>
    .metric-card {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f3c6e;
        margin-bottom: 8px;
    }
</style>

“””, unsafe_allow_html=True)

# ── Data loading ─────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
xl = pd.read_excel(“cleaned_data.xlsx”, sheet_name=None)
clients        = xl[“clients_dim”]
investigations = xl[“investigations_dash”]
interviews     = xl[“interviews_dash”]
case_notes     = xl[“case_notes_fact”]
monthly        = xl[“monthly_summary”]
alleged        = xl[“alleged_offender”]
charges        = xl[“charges_outcomes”]
case_support   = xl[“case_support”]

```
# Parse dates
for df in [investigations, interviews, monthly, case_notes]:
    for col in df.select_dtypes(include="object").columns:
        if "date" in col.lower() or "month" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

monthly["month_start"] = pd.to_datetime(monthly["month_start"], errors="coerce")
return clients, investigations, interviews, case_notes, monthly, alleged, charges, case_support
```

clients, investigations, interviews, case_notes, monthly, alleged, charges, case_support = load_data()

# ── Sidebar filters ──────────────────────────────────────────────────────────

st.sidebar.title(“🔍 Filters”)

fiscal_years = sorted(investigations[“investigation_fiscal_year”].dropna().unique())
selected_fy = st.sidebar.multiselect(“Fiscal Year”, fiscal_years, default=fiscal_years[-2:] if len(fiscal_years) >= 2 else fiscal_years)

age_bands = sorted(investigations[“age_band”].dropna().unique())
selected_ages = st.sidebar.multiselect(“Age Band”, age_bands, default=age_bands)

# Apply filters

inv_f = investigations[
investigations[“investigation_fiscal_year”].isin(selected_fy) &
investigations[“age_band”].isin(selected_ages)
] if selected_fy and selected_ages else investigations.copy()

int_f = interviews[
interviews[“interview_fiscal_year”].isin(selected_fy)
] if selected_fy else interviews.copy()

# ── Page tabs ────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
“📋 Overview”, “👤 Client Demographics”, “🔎 Investigations”, “🎙️ Interviews”, “📂 Case Activity”
])

# ════════════════════════════════════════════════════════════════════════════

# TAB 1 – OVERVIEW

# ════════════════════════════════════════════════════════════════════════════

with tab1:
st.title(“Child Advocacy Centre — Analytics Dashboard”)
st.markdown(“Use the sidebar to filter by **Fiscal Year** and **Age Band**.”)

```
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Clients",        f"{clients['client_id'].nunique():,}")
c2.metric("Investigations",        f"{inv_f['occurrence_id'].nunique():,}")
c3.metric("Interviews",            f"{int_f['occurrence_id'].nunique():,}")
c4.metric("Case Notes",            f"{case_notes['case_id'].nunique():,}")
c5.metric("Avg Interview Duration",f"{interviews['interview_duration_minutes'].mean():.0f} min")

st.divider()

# Monthly trend
st.markdown('<div class="section-header">Monthly Volume Trend</div>', unsafe_allow_html=True)
mon_f = monthly[monthly["fiscal_year"].isin(selected_fy)] if selected_fy else monthly.copy()
if not mon_f.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mon_f["month_start"], y=mon_f["investigations_reported"],
                             name="Investigations", line=dict(color="#1f77b4", width=2)))
    fig.add_trace(go.Scatter(x=mon_f["month_start"], y=mon_f["interviews_reported"],
                             name="Interviews", line=dict(color="#ff7f0e", width=2)))
    fig.update_layout(height=360, margin=dict(t=20, b=20),
                      xaxis_title="Month", yaxis_title="Count", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

# Consent rate
st.markdown('<div class="section-header">Consent Rate Over Time (%)</div>', unsafe_allow_html=True)
fig2 = px.bar(mon_f, x="month_start", y="consent_rate_pct",
              color="fiscal_year", labels={"consent_rate_pct": "Consent %", "month_start": "Month"})
fig2.update_layout(height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig2, use_container_width=True)
```

# ════════════════════════════════════════════════════════════════════════════

# TAB 2 – CLIENT DEMOGRAPHICS

# ════════════════════════════════════════════════════════════════════════════

with tab2:
st.header(“Client Demographics”)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Age Band Distribution</div>', unsafe_allow_html=True)
    age_counts = clients["age_band"].value_counts().reset_index()
    age_counts.columns = ["Age Band", "Count"]
    fig = px.bar(age_counts, x="Age Band", y="Count", color="Age Band",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False, height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Biological Sex</div>', unsafe_allow_html=True)
    sex_counts = clients["biological_sex_clean"].value_counts().reset_index()
    sex_counts.columns = ["Sex", "Count"]
    fig = px.pie(sex_counts, values="Count", names="Sex", hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Ethnicity Breakdown</div>', unsafe_allow_html=True)
    eth = clients["ethnicity"].value_counts().head(10).reset_index()
    eth.columns = ["Ethnicity", "Count"]
    fig = px.bar(eth, x="Count", y="Ethnicity", orientation="h",
                 color="Count", color_continuous_scale="Blues")
    fig.update_layout(height=350, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Indigenous Identity</div>', unsafe_allow_html=True)
    ind = clients["is_indigenous"].value_counts().reset_index()
    ind.columns = ["Indigenous", "Count"]
    fig = px.pie(ind, values="Count", names="Indigenous", hole=0.35,
                 color_discrete_sequence=["#2196F3", "#FFC107", "#9E9E9E"])
    fig.update_layout(height=350, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">Primary Language</div>', unsafe_allow_html=True)
lang = clients["primary_language"].value_counts().head(12).reset_index()
lang.columns = ["Language", "Count"]
fig = px.bar(lang, x="Language", y="Count", color="Count",
             color_continuous_scale="Teal", text_auto=True)
fig.update_layout(height=320, margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">File Closure Reasons</div>', unsafe_allow_html=True)
closure = clients["reason_for_file_closure"].value_counts().reset_index()
closure.columns = ["Reason", "Count"]
fig = px.bar(closure, x="Reason", y="Count", color="Reason",
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_layout(showlegend=False, height=320, margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
```

# ════════════════════════════════════════════════════════════════════════════

# TAB 3 – INVESTIGATIONS

# ════════════════════════════════════════════════════════════════════════════

with tab3:
st.header(“Investigations”)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Investigations by Fiscal Year</div>', unsafe_allow_html=True)
    fy_inv = inv_f.groupby("investigation_fiscal_year")["occurrence_id"].nunique().reset_index()
    fy_inv.columns = ["Fiscal Year", "Count"]
    fig = px.bar(fy_inv, x="Fiscal Year", y="Count", color="Count",
                 color_continuous_scale="Blues", text_auto=True)
    fig.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">File Status</div>', unsafe_allow_html=True)
    status = inv_f["file_status_clean"].value_counts().reset_index()
    status.columns = ["Status", "Count"]
    fig = px.pie(status, values="Count", names="Status", hole=0.35,
                 color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Referral Source</div>', unsafe_allow_html=True)
    ref = inv_f["referral_source_clean"].value_counts().head(10).reset_index()
    ref.columns = ["Source", "Count"]
    fig = px.bar(ref, x="Count", y="Source", orientation="h",
                 color="Count", color_continuous_scale="Oranges")
    fig.update_layout(height=350, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Detachment (Top 10)</div>', unsafe_allow_html=True)
    det = inv_f["detachment_clean"].value_counts().head(10).reset_index()
    det.columns = ["Detachment", "Count"]
    fig = px.bar(det, x="Count", y="Detachment", orientation="h",
                 color="Count", color_continuous_scale="Greens")
    fig.update_layout(height=350, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">Investigations by Quarter × Fiscal Year</div>', unsafe_allow_html=True)
qtr = inv_f.groupby(["investigation_fiscal_year", "investigation_quarter"])["occurrence_id"].nunique().reset_index()
qtr.columns = ["Fiscal Year", "Quarter", "Count"]
fig = px.bar(qtr, x="Quarter", y="Count", color="Fiscal Year", barmode="group",
             color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(height=340, margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)

# Alleged offender section
st.subheader("Alleged Offenders")
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="section-header">Primary Abuse Type</div>', unsafe_allow_html=True)
    abuse = alleged["primary_abuse_type"].value_counts().reset_index()
    abuse.columns = ["Abuse Type", "Count"]
    fig = px.bar(abuse, x="Count", y="Abuse Type", orientation="h",
                 color="Count", color_continuous_scale="Reds")
    fig.update_layout(height=340, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">Relationship to Client</div>', unsafe_allow_html=True)
    rel = alleged["relationship_to_client"].value_counts().head(10).reset_index()
    rel.columns = ["Relationship", "Count"]
    fig = px.pie(rel, values="Count", names="Relationship", hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(height=340, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

if not charges.empty:
    st.markdown('<div class="section-header">Charge Outcomes</div>', unsafe_allow_html=True)
    out = charges["outcome"].value_counts().reset_index()
    out.columns = ["Outcome", "Count"]
    fig = px.bar(out, x="Outcome", y="Count", color="Outcome",
                 color_discrete_sequence=px.colors.qualitative.Safe, text_auto=True)
    fig.update_layout(showlegend=False, height=300, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)
```

# ════════════════════════════════════════════════════════════════════════════

# TAB 4 – INTERVIEWS

# ════════════════════════════════════════════════════════════════════════════

with tab4:
st.header(“Interviews”)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Interview Type</div>', unsafe_allow_html=True)
    itype = int_f["interview_type"].value_counts().reset_index()
    itype.columns = ["Type", "Count"]
    fig = px.pie(itype, values="Count", names="Type", hole=0.35,
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Disclosure Made</div>', unsafe_allow_html=True)
    disc = int_f["disclosure_made_clean"].value_counts().reset_index()
    disc.columns = ["Disclosure", "Count"]
    fig = px.bar(disc, x="Disclosure", y="Count", color="Disclosure",
                 color_discrete_sequence=["#4CAF50", "#F44336", "#9E9E9E"], text_auto=True)
    fig.update_layout(showlegend=False, height=320, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Type of Abuse (Interviews)</div>', unsafe_allow_html=True)
    ab_int = int_f["type_of_abuse_clean"].value_counts().reset_index()
    ab_int.columns = ["Abuse Type", "Count"]
    fig = px.bar(ab_int, x="Count", y="Abuse Type", orientation="h",
                 color="Count", color_continuous_scale="Purples")
    fig.update_layout(height=350, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Interview Duration Distribution</div>', unsafe_allow_html=True)
    dur = int_f["interview_duration_minutes"].dropna()
    fig = px.histogram(dur, nbins=30, color_discrete_sequence=["#2196F3"],
                       labels={"value": "Duration (min)", "count": "Count"})
    fig.update_layout(height=350, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">Interviews by Person Interviewed</div>', unsafe_allow_html=True)
pi = int_f["person_interviewed"].value_counts().head(8).reset_index()
pi.columns = ["Person", "Count"]
fig = px.bar(pi, x="Person", y="Count", color="Count",
             color_continuous_scale="Teal", text_auto=True)
fig.update_layout(height=300, margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
```

# ════════════════════════════════════════════════════════════════════════════

# TAB 5 – CASE ACTIVITY

# ════════════════════════════════════════════════════════════════════════════

with tab5:
st.header(“Case Activity”)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Case Note Types</div>', unsafe_allow_html=True)
    note_type = case_notes["case_note_type_clean"].value_counts().head(12).reset_index()
    note_type.columns = ["Note Type", "Count"]
    fig = px.bar(note_type, x="Count", y="Note Type", orientation="h",
                 color="Count", color_continuous_scale="Blues")
    fig.update_layout(height=380, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Contact Method</div>', unsafe_allow_html=True)
    cm = case_notes["contact_method_clean"].value_counts().reset_index()
    cm.columns = ["Method", "Count"]
    fig = px.pie(cm, values="Count", names="Method", hole=0.35,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=380, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Contact Location</div>', unsafe_allow_html=True)
    loc = case_notes["contact_location_clean"].value_counts().head(10).reset_index()
    loc.columns = ["Location", "Count"]
    fig = px.bar(loc, x="Count", y="Location", orientation="h",
                 color="Count", color_continuous_scale="Oranges")
    fig.update_layout(height=350, margin=dict(t=10), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Support Type Distribution</div>', unsafe_allow_html=True)
    sup = case_support.groupby("support_type")["support_count"].sum().reset_index()
    sup.columns = ["Support Type", "Total"]
    fig = px.bar(sup, x="Support Type", y="Total", color="Support Type",
                 color_discrete_sequence=px.colors.qualitative.Pastel, text_auto=True)
    fig.update_layout(showlegend=False, height=350, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-header">Case Notes Volume by Fiscal Year</div>', unsafe_allow_html=True)
case_notes["note_fiscal_year"] = case_notes["note_fiscal_year"].astype(str)
cn_fy = case_notes.groupby("note_fiscal_year")["case_id"].count().reset_index()
cn_fy.columns = ["Fiscal Year", "Note Count"]
cn_fy = cn_fy[cn_fy["Fiscal Year"] != "nan"]
fig = px.bar(cn_fy, x="Fiscal Year", y="Note Count", color="Note Count",
             color_continuous_scale="Teal", text_auto=True)
fig.update_layout(height=320, margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
```

st.sidebar.divider()
st.sidebar.caption(“Dashboard built with Streamlit · Data: cleaned_data.xlsx”)