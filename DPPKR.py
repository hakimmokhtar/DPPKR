import streamlit as st
import pandas as pd
import datetime
from urllib.parse import quote

# --- ✅ Background Hijau PAS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #006e3c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    .stApp, .stMarkdown, .stSelectbox label, .stDateInput label,
    .stDataFrame, .stMetric, .stTextInput, .stButton, .stNumberInput label {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    .css-1d391kg { color: white !important; }
    .stSelectbox div[data-baseweb="select"],
    .stDateInput input {
        background-color: #004d2a !important;
        color: white !important;
    }
    .dataframe th {
        background-color: #004d2a !important;
        color: white !important;
    }
    .dataframe td {
        color: white !important;
        background-color: #006e3c !important;
    }
    </style>
""", unsafe_allow_html=True)

st.image("LOGO DPPM.png", width=700)

st.title("DEWAN PEMUDA PAS KAWASAN REMBAU 2025-2027")

sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"

def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')
    df['BulanNum'] = df['Tarikh'].dt.month
    return df.sort_values('Tarikh')

df = load_data()

# Tarikh hari ini
today = datetime.date.today()

# Program hari ini
program_hari_ini = df[df['Tarikh'].dt.date == today]

if not program_hari_ini.empty:
    aktiviti_list = program_hari_ini['Aktiviti'].tolist()
    tempat_list = program_hari_ini['Tempat'].tolist()

    senarai_program = "<ul>" + "".join(
        f"<li>{aktiviti} - {tempat}</li>" for aktiviti, tempat in zip(aktiviti_list, tempat_list)
    ) + "</ul>"

    st.markdown(
        f"""
        <div style="background-color:#004d2a; padding:20px; border-radius:10px; border-left:8px solid #ffffff">
            <h4 style="color:white;">📢 <u>Program Hari Ini ({today.strftime('%A, %d %B %Y')}):</u></h4>
            {senarai_program}
        </div>
        """,
        unsafe_allow_html=True
    )

    mesej_wa_hari_ini = f"*Program Hari Ini ({today.strftime('%A, %d %B %Y')})*\n"
    for aktiviti, tempat in zip(aktiviti_list, tempat_list):
        mesej_wa_hari_ini += f"📌 {aktiviti}\n📍 {tempat}\n\n"

    pautan_wa_hari_ini = f"https://wa.me/?text={quote(mesej_wa_hari_ini)}"
    st.markdown(f"[📤 Kongsi Program Hari Ini ke WhatsApp]({pautan_wa_hari_ini})", unsafe_allow_html=True)

# Butang metrik dan fungsi klik
jumlah_program = len(df)
jumlah_program_hari_ini = len(program_hari_ini)
jumlah_program_akan_datang = len(df[df['Tarikh'].dt.date > today])
jumlah_program_selesai = len(df[df['Tarikh'].dt.date < today])

# Pilihan tahun
tahun_list = sorted(
    [int(t) for t in df['Tahun'].dropna().unique() if 2025 <= t <= 2027],
    reverse=True
)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

jumlah_program_tahun_ini = len(df[df['Tahun'] == tahun_dipilih])

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button(f"📊 Jumlah Program\n({jumlah_program})"):
        with st.expander("📋 Senarai Semua Program", expanded=True):
            df_all = df[['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_all['Tarikh'] = df_all['Tarikh'].dt.strftime('%d %b %Y')
            df_all.reset_index(drop=True, inplace=True)
            df_all.index += 1
            df_all.index.name = 'Bil'
            st.dataframe(df_all, use_container_width=True)

    if col2.button(f"📌 Program Hari Ini\n({jumlah_program_hari_ini})"):
        with st.expander("📋 Senarai Program Hari Ini", expanded=True):
            st.dataframe(df_papar, use_container_width=True)

    if col3.button(f"📅 Akan Datang\n({jumlah_program_akan_datang})"):
        with st.expander("📋 Program Akan Datang", expanded=True):
            df_future = df[df['Tarikh'].dt.date > today][['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_future['Tarikh'] = df_future['Tarikh'].dt.strftime('%d %b %Y')
            df_future.reset_index(drop=True, inplace=True)
            df_future.index += 1
            df_future.index.name = 'Bil'
            st.dataframe(df_future, use_container_width=True)

    if col4.button(f"📆 Program {tahun_dipilih}\n({jumlah_program_tahun_ini})"):
        with st.expander(f"📋 Senarai Program Tahun {tahun_dipilih}", expanded=True):
            df_year = df[df['Tahun'] == tahun_dipilih][['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_year['Tarikh'] = df_year['Tarikh'].dt.strftime('%d %b %Y')
            df_year.reset_index(drop=True, inplace=True)
            df_year.index += 1
            df_year.index.name = 'Bil'
            st.dataframe(df_year, use_container_width=True)

    if col5.button(f"✅ Program Selesai\n({jumlah_program_selesai})"):
        with st.expander("📋 Program Telah Selesai", expanded=True):
            df_done = df[df['Tarikh'].dt.date < today][['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_done['Tarikh'] = df_done['Tarikh'].dt.strftime('%d %b %Y')
            df_done.reset_index(drop=True, inplace=True)
            df_done.index += 1
            df_done.index.name = 'Bil'
            st.dataframe(df_done, use_container_width=True)


# Butang kongsi semua program ke WhatsApp
mesej_semua_program = "*📋 Senarai Semua Program DPPKR 2025–2027*\n"
for _, row in df.iterrows():
    mesej_semua_program += f"📅 {row['Tarikh'].strftime('%d/%m/%Y')}\n📌 {row['Aktiviti']}\n📍 {row['Tempat']}\n\n"

pautan_wa_semua = f"https://wa.me/?text={quote(mesej_semua_program)}"
st.markdown(f"[📤 Kongsi Semua Program ke WhatsApp]({pautan_wa_semua})", unsafe_allow_html=True)

# Penapis ikut bulan
bulan_penuh = [
    ('Januari', 1), ('Februari', 2), ('Mac', 3), ('April', 4),
    ('Mei', 5), ('Jun', 6), ('Julai', 7), ('Ogos', 8),
    ('September', 9), ('Oktober', 10), ('November', 11), ('Disember', 12)
]

bulan_nama_list = [b[0] for b in bulan_penuh]
bulan_nombor_list = [b[1] for b in bulan_penuh]

bulan_dipilih_nama = st.selectbox("Pilih Bulan", bulan_nama_list)
bulan_dipilih_num = bulan_nombor_list[bulan_nama_list.index(bulan_dipilih_nama)]

df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['BulanNum'] == bulan_dipilih_num)]

st.markdown(f"## 📌 Jadual Aktiviti Bulan {bulan_dipilih_nama} {tahun_dipilih}")

if df_tapis.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    df_papar = df_tapis[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_papar['Tarikh'] = df_papar['Tarikh'].dt.strftime('%d %b %Y')
    df_papar.reset_index(drop=True, inplace=True)
    df_papar.index += 1
    df_papar.index.name = 'Bil'
    st.dataframe(df_papar, use_container_width=True)

# Carian ikut tarikh
st.markdown("## 🔍 Program Mengikut Tarikh")
tarikh_dicari = st.date_input("📆 Pilih Tarikh", today)
df_dicari = df[df['Tarikh'].dt.date == tarikh_dicari]
if df_dicari.empty:
    st.info("❌ Tiada program pada tarikh ini.")
else:
    df_carian = df_dicari[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_carian['Tarikh'] = df_carian['Tarikh'].dt.strftime('%d %b %Y')
    df_carian.reset_index(drop=True, inplace=True)
    df_carian.index += 1
    df_carian.index.name = 'Bil'
    st.dataframe(df_carian, use_container_width=True)

# Footer
st.markdown("""
    <style>
    .footer {
        background-color: #006e3c;
        color: white;
        padding: 15px 10px;
        text-align: center;
        font-size: 0.9rem;
        margin-top: 30px;
        border-radius: 5px;
    }
    .footer a {
        color: #90ee90;
        text-decoration: none;
        margin: 0 8px;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
""" + """
<div class="footer">
    <b>DIBANGUNKAN OLEH JABATAN SETIAUSAHA DPPKR </b><br>
    <span>&#128231;</span> <a href="mailto:dppkrembau@gmail.com">Email</a> |
    <span>&#128279;</span> <a href="https://facebook.com/pemudapasrembau" target="_blank">Facebook </a><br> 
    <span>&#128222;</span> SU : <a href="tel:+60136343231">HAKIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60136343231" target="_blank">WhatsApp</a><br>
    <span>&#128222;</span> PSU 1: <a href="tel:+60173607925">NAIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60173607925" target="_blank">WhatsApp</a>
</div>
""", unsafe_allow_html=True)
