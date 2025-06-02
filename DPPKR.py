import streamlit as st
import pandas as pd
import streamlit as st

# --- ✅ Logo ---
st.image("LOGO DPPKR.jpeg", width=100)  # Boleh tukar ke URL logo sendiri

# --- ✅ Tajuk Aplikasi ---
st.title("📅 Takwim Dewan Pemuda PAS Kawasan Rembau")

# --- ✅ Google Sheet URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

# --- ✅ Fungsi Baca Data ---
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()  # Bersih nama kolum
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')
    df['BulanNum'] = df['Tarikh'].dt.month
    return df.sort_values('Tarikh')

df = load_data()

# --- ✅ Dropdown Tahun ---
tahun_list = sorted(df['Tahun'].unique(), reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

# --- ✅ Senarai Bulan Penuh (Jan - Dec) ---
bulan_penuh = [
    ('Januari', 1), ('Februari', 2), ('Mac', 3), ('April', 4),
    ('Mei', 5), ('Jun', 6), ('Julai', 7), ('Ogos', 8),
    ('September', 9), ('Oktober', 10), ('November', 11), ('Disember', 12)
]

bulan_nama_list = [b[0] for b in bulan_penuh]
bulan_nombor_list = [b[1] for b in bulan_penuh]

# --- ✅ Dropdown Bulan ---
bulan_dipilih_nama = st.selectbox("Pilih Bulan", bulan_nama_list)
bulan_dipilih_index = bulan_nama_list.index(bulan_dipilih_nama)
bulan_dipilih_num = bulan_nombor_list[bulan_dipilih_index]

# --- ✅ Tapis Data Ikut Pilihan Tahun dan Bulan ---
df['BulanNum'] = df['Tarikh'].dt.month  # pastikan kolum BulanNum ada
df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['BulanNum'] == bulan_dipilih_num)]

# --- ✅ Papar Aktiviti ---
st.markdown(f"## 📌 Aktiviti Bulan {bulan_dipilih_nama} {tahun_dipilih}")

if df_tapis.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    for _, row in df_tapis.iterrows():
        st.write(f"🗓️ **{row['Tarikh'].strftime('%d %b %Y')}**: {row['Aktiviti']}")
