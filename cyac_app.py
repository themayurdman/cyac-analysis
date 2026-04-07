import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='CAC Analytics Dashboard', layout='wide', page_icon='CAC')

@st.cache_data
def load_data():
xl = pd.read_excel(‘cleaned_data.xlsx’, sheet_name=None)
clients        = xl[‘clients_dim’]
investigations = xl[‘investigations_dash’]
interviews     = xl[‘interviews_dash’]
case_notes     = xl[‘case_notes_fact’]
monthly        = xl[‘monthly_summary’]
alleged        = xl[‘alleged_offender’]
charges        = xl[‘charges_outcomes’]
case_support   = xl[‘case_support’]
monthly[‘month_start’] = pd.to_datetime(monthly[‘month_start’], errors=‘coerce’)
return clients, investigations, interviews, case_notes, monthly, alleged, charges, case_support

clients, investigations, interviews, case_notes, monthly, alleged, charges, case_support = load_data()

st.sidebar.title(‘Filters’)
fiscal_years = sorted(investigations[‘investigation_fiscal_year’].dropna().unique())
selected_fy = st.sidebar.multiselect(‘Fiscal Year’, fiscal_years, default=fiscal_years[-2:] if len(fiscal_years) >= 2 else fiscal_years)
age_bands = sorted(investigations[‘age_band’].dropna().unique())
selected_ages = st.sidebar.multiselect(‘Age Band’, age_bands, default=age_bands)

inv_f = investigations[investigations[‘investigation_fiscal_year’].isin(selected_fy) & investigations[‘age_band’].isin(selected_ages)] if (selected_fy and selected_ages) else investigations.copy()
int_f = interviews[interviews[‘interview_fiscal_year’].isin(selected_fy)] if selected_fy else interviews.copy()

tab1, tab2, tab3, tab4, tab5 = st.tabs([‘Overview’, ‘Client Demographics’, ‘Investigations’, ‘Interviews’, ‘Case Activity’])

# OVERVIEW

with tab1:
st.title(‘Child Advocacy Centre - Analytics Dashboard’)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(‘Total Clients’, f”{clients[‘client_id’].nunique():,}”)
c2.metric(‘Investigations’, f”{inv_f[‘occurrence_id’].nunique():,}”)
c3.metric(‘Interviews’, f”{int_f[‘occurrence_id’].nunique():,}”)
c4.metric(‘Case Notes’, f”{case_notes[‘case_id’].nunique():,}”)
c5.metric(‘Avg Interview Duration’, f”{interviews[‘interview_duration_minutes’].mean():.0f} min”)
st.divider()
mon_f = monthly[monthly[‘fiscal_year’].isin(selected_fy)] if selected_fy else monthly.copy()
st.subheader(‘Monthly Volume Trend’)
if not mon_f.empty:
fig = go.Figure()
fig.add_trace(go.Scatter(x=mon_f[‘month_start’], y=mon_f[‘investigations_reported’], name=‘Investigations’, line=dict(color=’#1f77b4’, width=2)))
fig.add_trace(go.Scatter(x=mon_f[‘month_start’], y=mon_f[‘interviews_reported’], name=‘Interviews’, line=dict(color=’#ff7f0e’, width=2)))
fig.update_layout(height=360, xaxis_title=‘Month’, yaxis_title=‘Count’)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Consent Rate Over Time’)
if not mon_f.empty:
fig2 = px.bar(mon_f, x=‘month_start’, y=‘consent_rate_pct’, color=‘fiscal_year’)
fig2.update_layout(height=300)
st.plotly_chart(fig2, use_container_width=True)

# DEMOGRAPHICS

with tab2:
st.header(‘Client Demographics’)
col1, col2 = st.columns(2)
with col1:
st.subheader(‘Age Band Distribution’)
d = clients[‘age_band’].value_counts().reset_index()
d.columns = [‘Age Band’, ‘Count’]
fig = px.bar(d, x=‘Age Band’, y=‘Count’, color=‘Age Band’, color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(showlegend=False, height=320)
st.plotly_chart(fig, use_container_width=True)
with col2:
st.subheader(‘Biological Sex’)
d = clients[‘biological_sex_clean’].value_counts().reset_index()
d.columns = [‘Sex’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Sex’, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
st.subheader(‘Ethnicity (Top 10)’)
d = clients[‘ethnicity’].value_counts().head(10).reset_index()
d.columns = [‘Ethnicity’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Ethnicity’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Blues’)
fig.update_layout(height=350, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col4:
st.subheader(‘Indigenous Identity’)
d = clients[‘is_indigenous’].value_counts().reset_index()
d.columns = [‘Indigenous’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Indigenous’, hole=0.35)
fig.update_layout(height=350)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Primary Language’)
d = clients[‘primary_language’].value_counts().head(12).reset_index()
d.columns = [‘Language’, ‘Count’]
fig = px.bar(d, x=‘Language’, y=‘Count’, color=‘Count’, color_continuous_scale=‘Teal’, text_auto=True)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘File Closure Reasons’)
d = clients[‘reason_for_file_closure’].value_counts().reset_index()
d.columns = [‘Reason’, ‘Count’]
fig = px.bar(d, x=‘Reason’, y=‘Count’, color=‘Reason’, color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_layout(showlegend=False, height=320)
st.plotly_chart(fig, use_container_width=True)

# INVESTIGATIONS

with tab3:
st.header(‘Investigations’)
col1, col2 = st.columns(2)
with col1:
st.subheader(‘By Fiscal Year’)
d = inv_f.groupby(‘investigation_fiscal_year’)[‘occurrence_id’].nunique().reset_index()
d.columns = [‘Fiscal Year’, ‘Count’]
fig = px.bar(d, x=‘Fiscal Year’, y=‘Count’, color=‘Count’, color_continuous_scale=‘Blues’, text_auto=True)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)
with col2:
st.subheader(‘File Status’)
d = inv_f[‘file_status_clean’].value_counts().reset_index()
d.columns = [‘Status’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Status’, hole=0.35, color_discrete_sequence=px.colors.qualitative.Set1)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
st.subheader(‘Referral Source’)
d = inv_f[‘referral_source_clean’].value_counts().head(10).reset_index()
d.columns = [‘Source’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Source’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Oranges’)
fig.update_layout(height=350, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col4:
st.subheader(‘Detachment (Top 10)’)
d = inv_f[‘detachment_clean’].value_counts().head(10).reset_index()
d.columns = [‘Detachment’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Detachment’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Greens’)
fig.update_layout(height=350, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Investigations by Quarter and Fiscal Year’)
d = inv_f.groupby([‘investigation_fiscal_year’, ‘investigation_quarter’])[‘occurrence_id’].nunique().reset_index()
d.columns = [‘Fiscal Year’, ‘Quarter’, ‘Count’]
fig = px.bar(d, x=‘Quarter’, y=‘Count’, color=‘Fiscal Year’, barmode=‘group’, color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(height=340)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Alleged Offenders’)
col5, col6 = st.columns(2)
with col5:
d = alleged[‘primary_abuse_type’].value_counts().reset_index()
d.columns = [‘Abuse Type’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Abuse Type’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Reds’)
fig.update_layout(height=340, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col6:
d = alleged[‘relationship_to_client’].value_counts().head(10).reset_index()
d.columns = [‘Relationship’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Relationship’, hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(height=340)
st.plotly_chart(fig, use_container_width=True)
if not charges.empty:
st.subheader(‘Charge Outcomes’)
d = charges[‘outcome’].value_counts().reset_index()
d.columns = [‘Outcome’, ‘Count’]
fig = px.bar(d, x=‘Outcome’, y=‘Count’, color=‘Outcome’, text_auto=True)
fig.update_layout(showlegend=False, height=300)
st.plotly_chart(fig, use_container_width=True)

# INTERVIEWS

with tab4:
st.header(‘Interviews’)
col1, col2 = st.columns(2)
with col1:
st.subheader(‘Interview Type’)
d = int_f[‘interview_type’].value_counts().reset_index()
d.columns = [‘Type’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Type’, hole=0.35, color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)
with col2:
st.subheader(‘Disclosure Made’)
d = int_f[‘disclosure_made_clean’].value_counts().reset_index()
d.columns = [‘Disclosure’, ‘Count’]
fig = px.bar(d, x=‘Disclosure’, y=‘Count’, color=‘Disclosure’, text_auto=True)
fig.update_layout(showlegend=False, height=320)
st.plotly_chart(fig, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
st.subheader(‘Type of Abuse’)
d = int_f[‘type_of_abuse_clean’].value_counts().reset_index()
d.columns = [‘Abuse Type’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Abuse Type’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Purples’)
fig.update_layout(height=350, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col4:
st.subheader(‘Interview Duration Distribution’)
dur = int_f[‘interview_duration_minutes’].dropna()
fig = px.histogram(dur, nbins=30, color_discrete_sequence=[’#2196F3’], labels={‘value’: ‘Duration (min)’})
fig.update_layout(height=350)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Person Interviewed’)
d = int_f[‘person_interviewed’].value_counts().head(8).reset_index()
d.columns = [‘Person’, ‘Count’]
fig = px.bar(d, x=‘Person’, y=‘Count’, color=‘Count’, color_continuous_scale=‘Teal’, text_auto=True)
fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

# CASE ACTIVITY

with tab5:
st.header(‘Case Activity’)
col1, col2 = st.columns(2)
with col1:
st.subheader(‘Case Note Types’)
d = case_notes[‘case_note_type_clean’].value_counts().head(12).reset_index()
d.columns = [‘Note Type’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Note Type’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Blues’)
fig.update_layout(height=380, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col2:
st.subheader(‘Contact Method’)
d = case_notes[‘contact_method_clean’].value_counts().reset_index()
d.columns = [‘Method’, ‘Count’]
fig = px.pie(d, values=‘Count’, names=‘Method’, hole=0.35, color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(height=380)
st.plotly_chart(fig, use_container_width=True)
col3, col4 = st.columns(2)
with col3:
st.subheader(‘Contact Location’)
d = case_notes[‘contact_location_clean’].value_counts().head(10).reset_index()
d.columns = [‘Location’, ‘Count’]
fig = px.bar(d, x=‘Count’, y=‘Location’, orientation=‘h’, color=‘Count’, color_continuous_scale=‘Oranges’)
fig.update_layout(height=350, yaxis=dict(autorange=‘reversed’))
st.plotly_chart(fig, use_container_width=True)
with col4:
st.subheader(‘Support Type’)
d = case_support.groupby(‘support_type’)[‘support_count’].sum().reset_index()
d.columns = [‘Support Type’, ‘Total’]
fig = px.bar(d, x=‘Support Type’, y=‘Total’, color=‘Support Type’, text_auto=True)
fig.update_layout(showlegend=False, height=350)
st.plotly_chart(fig, use_container_width=True)
st.subheader(‘Case Notes Volume by Fiscal Year’)
case_notes[‘note_fiscal_year’] = case_notes[‘note_fiscal_year’].astype(str)
d = case_notes.groupby(‘note_fiscal_year’)[‘case_id’].count().reset_index()
d.columns = [‘Fiscal Year’, ‘Note Count’]
d = d[d[‘Fiscal Year’] != ‘nan’]
fig = px.bar(d, x=‘Fiscal Year’, y=‘Note Count’, color=‘Note Count’, color_continuous_scale=‘Teal’, text_auto=True)
fig.update_layout(height=320)
st.plotly_chart(fig, use_container_width=True)

st.sidebar.divider()
st.sidebar.caption(‘Dashboard built with Streamlit’)