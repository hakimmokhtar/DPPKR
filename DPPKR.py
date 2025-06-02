import streamlit as st
import pandas as pd

# Google Sheet URL
sheet_id = "1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck"
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

# Baca data
@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df['Tarikh'] = pd.to_datetime(df['Tarikh'])
    return df.sort_values('Tarikh')

df = load_data()

# Tajuk Aplikasi
st.title("📅 Takwim Tahunan")

# Papar jadual
st.dataframe(df, use_container_width=True)

# Papar kalendar ringkas
st.markdown("## Aktiviti Tahun Ini")
for index, row in df.iterrows():
    st.write(f"📌 **{row['Tarikh'].strftime('%d %b %Y')}**: {row['Aktiviti']}")
