import streamlit as st
import pandas as pd
import datetime

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
    h1, h2, h3, h4, h5, h6 { color: white !important; }
    .css-1d391kg { color: white !important; }
    .stSelectbox div[data-baseweb="select"], .stDateInput input {
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

# --- ✅ Notifikasi Program Hari Ini ---
today = datetime.date.today()
program_hari_ini = df[df['Tarikh'].dt.date == today]

if not program_hari_ini.empty:
    aktiviti_list = program_hari_ini['Aktiviti'].tolist()
    tempat_list = program_hari_ini['Tempat'].tolist()
    maklumat_list = [f"{a} @ {t}" for a, t in zip(aktiviti_list, tempat_list)]
    senarai_program = "<ul>" + "".join(f"<li>{m}</li>" for m in maklumat_list) + "</ul>"
    st.markdown(f"""
        <div style="background-color:#004d2a; padding:20px; border-radius:10px; border-left:8px solid #ffffff">
            <h4 style="color:white;">📢 <u>Program Hari Ini ({today.strftime('%A, %d %B %Y')}):</u></h4>
            {senarai_program}
        </div>
    """, unsafe_allow_html=True)
    for m in maklumat_list:
        st.toast(f"📌 {m}")

# --- ✅ Statistik Ringkas ---
jumlah_program = len(df)
jumlah_program_hari_ini = len(program_hari_ini)
jumlah_program_akan_datang = len(df[df['Tarikh'].dt.date > today])

# --- ✅ Dropdown Tahun ---
tahun_list = sorted([int(t) for t in df['Tahun'].dropna().unique() if 2025 <= t <= 2027], reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

jumlah_program_tahun_ini = len(df[df['Tahun'] == tahun_dipilih])
jumlah_program_selesai = len(df[df['Tarikh'].dt.date < today])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Jumlah Program", jumlah_program)
col2.metric("Program Hari Ini", jumlah_program_hari_ini)
col3.metric("Akan Datang", jumlah_program_akan_datang)
col4.metric(f"Program {tahun_dipilih}", jumlah_program_tahun_ini)
col5.metric("Program Selesai", jumlah_program_selesai)

# --- ✅ Pilih Bulan ---
bulan_penuh = [('Januari', 1), ('Februari', 2), ('Mac', 3), ('April', 4), ('Mei', 5), ('Jun', 6), ('Julai', 7),
               ('Ogos', 8), ('September', 9), ('Oktober', 10), ('November', 11), ('Disember', 12)]
bulan_nama_list = [b[0] for b in bulan_penuh]
bulan_nombor_list = [b[1] for b in bulan_penuh]

bulan_dipilih_nama = st.selectbox("Pilih Bulan", bulan_nama_list)
bulan_dipilih_num = bulan_nombor_list[bulan_nama_list.index(bulan_dipilih_nama)]

# --- ✅ Jadual Bulan Dipilih ---
df_tapis = df[(df['Tahun'] == tahun_dipilih) & (df['BulanNum'] == bulan_dipilih_num)]
st.markdown(f"## 📌 Jadual Aktiviti Bulan {bulan_dipilih_nama} {tahun_dipilih}")

if df_tapis.empty:
    st.info("❌ Tiada aktiviti pada bulan ini.")
else:
    df_papar = df_tapis[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_papar['Tarikh'] = df_papar['Tarikh'].dt.strftime('%d %b %Y')
    df_papar['Maklumat'] = df_papar['Aktiviti'] + " @ " + df_papar['Tempat']
    df_papar = df_papar[['Tarikh', 'Maklumat', 'Tempat']]
    df_papar.reset_index(drop=True, inplace=True)
    df_papar.index += 1
    df_papar.index.name = 'Bil'
    st.dataframe(df_papar, use_container_width=True)

# --- ✅ Program Akan Datang ---
st.markdown("## 📅 Program Yang Terdekat")
df_akan_datang = df[df['Tarikh'].dt.date >= today].sort_values('Tarikh').head(3)

if df_akan_datang.empty:
    st.info("❌ Tiada program akan datang setakat ini.")
else:
    df_prog = df_akan_datang[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_prog['Tarikh'] = df_prog['Tarikh'].dt.strftime('%A, %d %B %Y')
    df_prog['Maklumat'] = df_prog['Aktiviti'] + " @ " + df_prog['Tempat']
    df_prog = df_prog[['Tarikh', 'Maklumat', 'Tempat']]
    df_prog.reset_index(drop=True, inplace=True)
    df_prog.index += 1
    df_prog.index.name = 'Bil'
    st.dataframe(df_prog, use_container_width=True)

# --- ✅ Carian Tarikh ---
tarikh_dicari = st.date_input("📆 Pilih Tarikh Untuk Lihat Program", today)
df_carian = df[df['Tarikh'].dt.date == tarikh_dicari]

st.markdown(f"## 🔍 Program Pada {tarikh_dicari.strftime('%A, %d %B %Y')}")
if df_carian.empty:
    st.info("❌ Tiada program pada tarikh ini.")
else:
    df_view = df_carian[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
    df_view['Maklumat'] = df_view['Aktiviti'] + " @ " + df_view['Tempat']
    df_view = df_view[['Tarikh', 'Maklumat', 'Tempat']]
    df_view.reset_index(drop=True, inplace=True)
    df_view.index += 1
    df_view.index.name = 'Bil'
    st.dataframe(df_view, use_container_width=True)

# --- ✅ Footer & Gaya Tambahan ---
st.markdown("""
    <style>
    .stAlert {
        background-color: #006e3c !important;
        color: white !important;
        border-left: 0.5rem solid white !important;
    }
    .stAlert > div, .stAlert svg {
        color: white !important;
        fill: white !important;
    }
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
    .stMetric {
        background-color: #004d2a;
        padding: 10px;
        border-radius: 10px;
    }
    .element-container .stMetric label, .element-container .stMetric div {
        color: white !important;
    }
    </style>
    <div class="footer">
        <b>DISEDIAKAN OLEH JABATAN SETIAUSAHA DPPKR 25-27</b><br>
        <span>&#128231;</span> <a href="mailto:dppkrembau@gmail.com">Email</a> |
        <span>&#128279;</span> <a href="https://facebook.com/pemudapasrembau" target="_blank">Facebook </a><br>
        <span>&#128222;</span> SU : <a href="tel:+60136343231">HAKIM</a> |
        <span>&#128172;</span> <a href="https://wa.me/60136343231" target="_blank">WhatsApp</a><br>
        <span>&#128222;</span> PSU 1: <a href="tel:+60173607925">NAIM</a> |
        <span>&#128172;</span> <a href="https://wa.me/60173607925" target="_blank">WhatsApp</a>
    </div>
""", unsafe_allow_html=True)
