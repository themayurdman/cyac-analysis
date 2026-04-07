# CYAC Analytics Dashboard

This project is a Streamlit web app for analyzing **anonymized CYAC data**.

## Important privacy note
Use **cleaned and anonymized data only**.
Do not upload raw names, direct personal identifiers, or confidential case information to a public app or public repository.

## Features
- Upload anonymized CSV file
- Map your own dataset columns
- Filter by fiscal year, agency, month, and category
- Show key metrics
- Display summary tables
- Visualize:
  - Activity by agency
  - Trend over time
  - Category breakdown
- Download filtered data

## Recommended dataset columns
The app is flexible, but these columns are helpful:
- PT_ID
- Interview_Date or Month
- Fiscal_Year
- Agency
- Meeting_Count or Interview_Count
- Case_Type (optional)

## Safe workflow recommendation
- Keep the real working data in a **private repo or local folder**
- Use **PT_ID** instead of full names
- Remove or hide direct identifiers before upload
- If you want to publish a portfolio version, use **sample or aggregated data only**

## Run locally
```bash
pip install -r requirements.txt
streamlit run cyac_app.py
```
