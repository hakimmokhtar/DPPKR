import streamlit as st
import pandas as pd

# --- Logo ---
st.image("LOGO DPPM.png", width=500)

# --- Tajuk Aplikasi ---
st.title("Takwim Dewan Pemuda PAS Kawasan Rembau")

# --- Google Sheet URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

# --- Fungsi Baca Data dengan Debugging ---

def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
        
    # Tukar tarikh dengan errors='coerce' supaya tak valid jadi NaT
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True, errors='coerce')
    
    # Buang baris tanpa tarikh valid
    df = df.dropna(subset=['Tarikh'])
    
    # Teruskan buat kolum Tahun, Bulan dan BulanNum
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')
    df['BulanNum'] = df['Tarikh'].dt.month
    
    return df.sort_values('Tarikh')

df = load_data()

# --- Dropdown Tahun ---
tahun_list = sorted(set(df['Tahun'].unique()).union({2025, 2026, 2027}), reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

# --- Senarai Bulan Penuh ---
bulan_penuh = [
    ('Januari', 1), ('Februari', 2), ('Mac', 3), ('April', 4),
    ('Mei', 5), ('Jun', 6), ('Julai', 7), ('Ogos', 8),
    ('September', 9), ('Oktober', 10), ('November', 11), ('Disember', 12)
]

bulan_nama_list = [b[0] for b in bulan_penuh]
bulan_nombor_list = [b[1] for b in bulan_penuh]

# --- Dropdown Bulan ---
bulan_dipilih_nama = st.selectbox("Pilih Bulan", bulan_nama_list)
bulan_dipilih_index = bulan_nama_list.index(bulan_dipilih_nama)
bulan_dipilih_num = bulan_nombor_list[bulan_dipilih_index]

# --- Tapis Data ---
df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['BulanNum'] == bulan_dipilih_num)]

# --- Tajuk Seksyen ---
st.markdown(f"## 📌 Jadual Aktiviti Bulan {bulan_dipilih_nama} {tahun_dipilih}")

# --- Papar Data ---
if df_tapis.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    
    df_papar = df_tapis[['Tarikh', 'Aktiviti', 'Lajnah']].copy()
   # Peta nama hari dan bulan ke Bahasa Melayu
    nama_hari = {
    'Monday': 'Isnin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
    'Thursday': 'Khamis', 'Friday': 'Jumaat', 'Saturday': 'Sabtu', 'Sunday': 'Ahad'
    }

    nama_bulan = {
    'January': 'Januari', 'February': 'Februari', 'March': 'Mac', 'April': 'April',
    'May': 'Mei', 'June': 'Jun', 'July': 'Julai', 'August': 'Ogos',
    'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Disember'
    }

# Tukar ke format Bahasa Melayu
df_papar['Tarikh'] = df_papar['Tarikh'].dt.strftime('%A|%d|%B|%Y')
df_papar['Tarikh'] = df_papar['Tarikh'].apply(lambda x: f"{nama_hari[x.split('|')[0]]}, {x.split('|')[1]} {nama_bulan[x.split('|')[2]]} {x.split('|')[3]}")

    # Tambah kolum Bil bermula dari 1
    df_papar.reset_index(drop=True, inplace=True)
    df_papar.index += 1
    df_papar.index.name = 'Bil'

    st.dataframe(df_papar, use_container_width=True)
