import streamlit as st
import pandas as pd

# URL Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

# Fungsi Baca Data
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()  # Bersih ruang kosong nama kolum
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')
    df['BulanNum'] = df['Tarikh'].dt.month  # Untuk susun bulan ikut urutan
    return df.sort_values('Tarikh')

df = load_data()

# Tajuk Aplikasi
st.title("📅 Takwim Tahunan")

# Dropdown Tahun
tahun_list = sorted(df['Tahun'].unique(), reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

# Dropdown Bulan ikut Tahun yang dipilih
bulan_list = df[df['Tahun'] == tahun_dipilih].sort_values('BulanNum')['Bulan'].unique()
bulan_dipilih = st.selectbox("Pilih Bulan", bulan_list)

# Tapis data ikut pilihan
df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['Bulan'] == bulan_dipilih)]

# Tajuk seksyen aktiviti
st.markdown(f"## 📌 Aktiviti Bulan {bulan_dipilih} {tahun_dipilih}")

# Papar aktiviti
if df_tapis.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    for _, row in df_tapis.iterrows():
        st.write(f"🗓️ **{row['Tarikh'].strftime('%d %b %Y')}**: {row['Aktiviti']}")
