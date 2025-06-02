import streamlit as st
import pandas as pd

st.set_page_config(page_title="Takwim PASTI", layout="centered")

# ✅ Gantikan dengan ID sebenar Google Sheet anda
sheet_id = "1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck"
sheet_url = f"https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

@st.cache_data
def load_data():
    # ✅ header=1 sebab baris pertama kosong atau bukan tajuk
    df = pd.read_csv(sheet_url, header=1)

    # ✅ Ubah ke format datetime & pastikan day dulu (dd/mm/yyyy)
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)

    # ✅ Susun ikut tarikh naik
    return df.sort_values('Tarikh')

# ✅ Paparkan header app
st.title("📅 Takwim PASTI Rembau")
st.markdown("Senarai aktiviti sepanjang tahun yang diambil dari Google Sheet.")

# ✅ Load dan papar data
try:
    df = load_data()
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error("❌ Gagal memuatkan data. Sila semak ID Google Sheet dan struktur fail.")
    st.exception(e)
