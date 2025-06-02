import streamlit as st
import pandas as pd

# Google Sheet URL
sheet_id = "1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck"
sheet_url = f"https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

df = pd.read_csv(sheet_url)

# 👇 Ini debug penting
st.write("📋 Kolum yang dibaca dari Google Sheet:", df.columns)
st.write("🔍 Data awal yang dibaca:", df.head())
