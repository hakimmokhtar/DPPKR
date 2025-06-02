import streamlit as st
import pandas as pd

# Google Sheet URL
sheet_id = "1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck"
sheet_url = f"https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"


# Baca data
@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df['Tarikh'] = pd.to_datetime(df['Tarikh'])
    return df.sort_values('Tarikh')

@st.cache_data
def load_data():
    # ✅ header=1 sebab baris pertama kosong atau bukan tajuk
    df = pd.read_csv(sheet_url, header=1)

    # ✅ Ubah ke format datetime & pastikan day dulu (dd/mm/yyyy)
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)

    # ✅ Susun ikut tarikh naik
    return df.sort_values('Tarikh')

# Tajuk Aplikasi
st.title("📅 Takwim Tahunan")

# Papar jadual
st.dataframe(df, use_container_width=True)

# Papar kalendar ringkas
st.markdown("## Aktiviti Tahun Ini")
for index, row in df.iterrows():
    st.write(f"📌 **{row['Tarikh'].strftime('%d %b %Y')}**: {row['Aktiviti']}")



