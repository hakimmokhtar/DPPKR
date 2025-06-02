import streamlit as st
import pandas as pd

# Google Sheet URL
sheet_id = "1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck"
sheet_url = f"https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

@st.cache_data
def load_data():
    sheet_id = "GANTI_DENGAN_ID_SHEET"
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(sheet_url, header=1)
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    return df.sort_values('Tarikh')


