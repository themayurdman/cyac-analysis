# CAC Analytics Dashboard 📊

An interactive Streamlit dashboard for analyzing Child Advocacy Centre (CAC) data across clients, investigations, interviews, and case activity.

-----

## 🚀 Live App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> Replace the link above with your deployed Streamlit Cloud URL after deployment.

-----

## 📁 Repository Structure

```
├── app.py                # Main Streamlit application
├── cleaned_data.xlsx     # Source data file (add manually — see note below)
├── requirements.txt      # Python dependencies
└── README.md
```

> ⚠️ **Important:** `cleaned_data.xlsx` is **not** included in this repo (sensitive data). Upload it manually to the root of the repo, or configure Streamlit Secrets / cloud storage to provide it.

-----

## 📊 Dashboard Tabs

|Tab                    |Contents                                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------------------------------------|
|**Overview**           |KPI metrics, monthly investigation & interview trends, consent rate                                                 |
|**Client Demographics**|Age bands, biological sex, ethnicity, indigenous identity, language, closure reasons                                |
|**Investigations**     |Volume by fiscal year/quarter, file status, referral sources, detachments, alleged offender details, charge outcomes|
|**Interviews**         |Interview types, disclosure rates, abuse types, duration distribution, person interviewed                           |
|**Case Activity**      |Case note types, contact methods & locations, support types, notes volume by year                                   |

-----

## 🔍 Sidebar Filters

- **Fiscal Year** — multi-select to compare across years
- **Age Band** — filter all investigation views by client age group

-----

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place cleaned_data.xlsx in the project root

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

-----

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub (ensure `cleaned_data.xlsx` is included).
1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
1. Select your repo, branch (`main`), and set **Main file path** to `app.py`.
1. Click **Deploy** — done!

-----

## 📦 Dependencies

|Package    |Purpose                      |
|-----------|-----------------------------|
|`streamlit`|Web app framework            |
|`pandas`   |Data loading and manipulation|
|`openpyxl` |Reading `.xlsx` files        |
|`plotly`   |Interactive charts           |

-----

## 📝 Data Sheets Used

|Sheet                |Description                           |
|---------------------|--------------------------------------|
|`clients_dim`        |Client demographics and file info     |
|`investigations_dash`|Investigations joined with client data|
|`interviews_dash`    |Interviews joined with client data    |
|`case_notes_fact`    |Case note records                     |
|`monthly_summary`    |Aggregated monthly metrics            |
|`alleged_offender`   |Alleged offender details              |
|`charges_outcomes`   |Criminal charge outcomes              |
|`case_support`       |Support services provided             |

-----

## 🔒 Data Privacy

This dashboard is intended for internal organizational use only. Ensure all data is handled in accordance with applicable privacy legislation (e.g., PIPEDA, PHIPA).