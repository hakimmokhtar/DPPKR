import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Takwim DPPKR", page_icon="📅", layout="wide")

# CSS untuk gaya tersuai
st.markdown("""
    <style>
    /* Gaya Metric Box */
    .stMetric {
        background-color: #004d2a;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stMetric > div {
        color: white !important;
        font-weight: bold;
        font-size: 15px;
    }

    /* Notifikasi tiada aktiviti */
    .stAlert[data-testid="stNotificationContentWarning"] {
        background-color: #ffe6e6 !important;
        color: red !important;
        font-weight: bold !important;
        border-left: 6px solid red !important;
    }

    /* Ubah saiz teks metric label */
    div[data-testid="metric-container"] label {
        font-size: 15px;
        font-weight: bold;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Data sampel
program_data = pd.DataFrame({
    'Tarikh': pd.to_datetime([
        '2025-05-04', '2025-05-11', '2025-05-14', '2025-05-17',
        '2025-05-24', '2025-05-28', '2025-05-29', '2025-06-05'
    ]),
    'Aktiviti': [
        'Muktamar DPPKR 2025',
        'Mesyuarat Exco DPPKR kali 1',
        'Mesyuarat Exco DPPKR kali 2',
        'Majlis Hari Guru PASTI Kawasan Rembau',
        'Himpunan Kedaulatan Ummah',
        'Serahan Memorandum Bantahan URA',
        'Smash Pemuda',
        'Mesyuarat Exco DPPKR kali 3'
    ],
    'Tempat': [
        'Dewan Al Qamar',
        'Google Meet',
        'Pusat Khidmat Masyarakat Dun Paroi',
        'Raden Hall Senawang',
        'Sogo KL',
        'Pusat Khidmat Ahli Parlimen Rembau',
        'Court Seremban Jaya',
        'Pusat Khidmat Masyarakat Dun Paroi'
    ]
})

# Dropdown pilih tahun
st.selectbox("Pilih Tahun", [2025], index=0)

# Paparan kotak metrik
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Jumlah Program", f"{len(program_data)} 📅")
with col2:
    st.metric("Mesyuarat", f"{program_data['Aktiviti'].str.contains('Mesyuarat').sum()} 📌")
with col3:
    st.metric("Aktiviti Luar", f"{program_data['Aktiviti'].str.contains('Himpunan|Smash').sum()} 🏃")
with col4:
    st.metric("Tempat Berbeza", f"{program_data['Tempat'].nunique()} 🗺️")
with col5:
    st.metric("Program Selesai", f"✅ {len(program_data)}")

# Senarai program selesai
with st.expander("📗 Program Telah Selesai", expanded=True):
    st.dataframe(program_data.reset_index(drop=True).rename(columns={
        'Tarikh': 'Tarikh',
        'Aktiviti': 'Aktiviti',
        'Tempat': 'Tempat'
    }), use_container_width=True)
    st.markdown("📎 [Kongsi Semua Program ke WhatsApp](https://wa.me/?text=Senarai%20Program%20DPPKR%202025)")

# Pilihan bulan
bulan_dict = {
    "Januari": 1, "Februari": 2, "Mac": 3, "April": 4,
    "Mei": 5, "Jun": 6, "Julai": 7, "Ogos": 8,
    "September": 9, "Oktober": 10, "November": 11, "Disember": 12
}
pilih_bulan = st.selectbox("Pilih Bulan", list(bulan_dict.keys()))
bulan_num = bulan_dict[pilih_bulan]

# Tapisan program untuk bulan dipilih
program_bulan_ini = program_data[program_data['Tarikh'].dt.month == bulan_num]

# Paparan senarai program bulan dipilih
st.subheader(f"📌 Jadual Aktiviti Bulan {pilih_bulan} 2025")
if program_bulan_ini.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    st.write(program_bulan_ini[['Tarikh', 'Aktiviti', 'Tempat']].reset_index(drop=True))
