# CYAC Data Analysis Dashboard

This project analyzes CYAC case data using Streamlit.

## Features
- Upload CSV file
- Clean and preview data
- Metrics:
  - Total Cases
  - Total Clients
  - Total Records
- Visualizations:
  - Case Note Type
  - Monthly Trends
  - Time Bucket Analysis
  - Location Distribution

## Required Columns in CSV

Client ID  
Case ID  
Case Note Type  
Date of contact  
Time of contact  
Location of contact  
Month  
Day  
Time Bucket  

## How to Use

1. Clean your Excel data
2. Export as:
   CSV UTF-8 (Comma delimited)
3. Upload file in app

## Notes

- Remove extra header rows
- Remove "Unnamed" columns
- Ensure column names are correct
- No personal/sensitive data

## Tech Stack

- Python
- Pandas
- Streamlit
