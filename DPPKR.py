import streamlit as st
import pandas as pd

# URL Google Sheet CSV
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

# Baca dan proses data
@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()  # Bersih nama kolum
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')  # Contoh: "January"
    df['BulanNum'] = df['Tarikh'].dt.month        # Untuk sort bulan
    return df

df = load_data()

# Tajuk Aplikasi
st.title("📅 Takwim PASTI Rembau")

# Pilih Tahun
tahun_list = sorted(df['Tahun'].unique(), reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

# Pilih Bulan (ikut tahun dipilih)
bulan_list = df[df['Tahun'] == tahun_dipilih].sort_values('BulanNum')['Bulan'].unique()
bulan_dipilih = st.selectbox("Pilih Bulan", bulan_list)

# Tapis ikut pilihan
df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['Bulan'] == bulan_dipilih)]

# Papar hasil
st.markdown(f"### 📌 Aktiviti Bulan {bulan_dipilih} {tahun_dipilih}")
if df_tapis.empty:
    st.info("Tiada aktiviti pada bulan ini.")
else:
    for _, row in df_tapis.iterrows():
        st.write(f"🗓️ **{row['Tarikh'].strftime('%d %b %Y')}**: {row['Aktiviti']}")
