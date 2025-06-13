import streamlit as st
import pandas as pd
import datetime
from urllib.parse import quote

# --- ✅ CSS Custom ---
st.markdown("""
    <style>
    .stApp {
        background-color: #006e3c;
        color: white;
    }
    h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stSelectbox label, .stDateInput label, .stNumberInput label,
    .stTextInput, .stButton {
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"],
    .stDateInput input {
        background-color: #004d2a !important;
        color: white !important;
    }
    .dataframe th {
        background-color: #cce5cc !important;
        color: black !important;
    }
    .dataframe td {
        background-color: #e6f2e6 !important;
        color: black !important;
    }
    .box-container {
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-size: 24px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
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
    </style>
""", unsafe_allow_html=True)

# --- ✅ Header & Logo ---
cols = st.columns(5)
icons = ["📊", "📌", "📅", "🗓️", "✅"]
labels = ["Statistik", "Program Akan Datang", "Takwim", "Senarai Program", "Selesai"]

for col, icon, label in zip(cols, icons, labels):
    with col:
        st.markdown(f'<div class="box-container">{icon}<br><span>{label}</span></div>', unsafe_allow_html=True)

st.image("LOGO DPPM.png", width=700)
st.title("DEWAN PEMUDA PAS KAWASAN REMBAU 2025-2027")

# --- ✅ Load Data ---
sheet_url = "https://docs.google.com/spreadsheets/d/1qJmyiXVzcmzcfreSdDC1cV0Hr4iVsQcA99On-0NPOck/export?format=csv"
@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    df['Tarikh'] = pd.to_datetime(df['Tarikh'], dayfirst=True)
    df['Tahun'] = df['Tarikh'].dt.year
    df['Bulan'] = df['Tarikh'].dt.strftime('%B')
    df['BulanNum'] = df['Tarikh'].dt.month
    return df.sort_values('Tarikh')

df = load_data()
today = datetime.date.today()
program_hari_ini = df[df['Tarikh'].dt.date == today]

# --- ✅ Paparan Program Hari Ini ---
if not program_hari_ini.empty:
    aktiviti_list = program_hari_ini['Aktiviti'].tolist()
    tempat_list = program_hari_ini['Tempat'].tolist()
    senarai_program = "<ul>" + "".join(f"<li>{a} - {t}</li>" for a, t in zip(aktiviti_list, tempat_list)) + "</ul>"

    st.markdown(f"""
        <div style="background-color:#004d2a; padding:20px; border-radius:10px; border-left:8px solid #ffffff">
            <h4 style="color:white;">📢 <u>Program Hari Ini ({today.strftime('%A, %d %B %Y')}):</u></h4>
            {senarai_program}
        </div>
    """, unsafe_allow_html=True)

    for aktiviti in aktiviti_list:
        st.toast(f"📌 {aktiviti}")

    mesej_wa = f"*Program Hari Ini ({today.strftime('%A, %d %B %Y')})*\n" + "".join(
        f"📌 {a}\n📍 {t}\n\n" for a, t in zip(aktiviti_list, tempat_list))
    pautan_wa = f"https://wa.me/?text={quote(mesej_wa)}"
    st.markdown(f"[📤 Kongsi ke WhatsApp]({pautan_wa})", unsafe_allow_html=True)

# --- ✅ Statistik Kiraan Program ---
jumlah_program = len(df)
jumlah_program_hari_ini = len(program_hari_ini)
jumlah_program_akan_datang = len(df[df['Tarikh'].dt.date > today])
jumlah_program_selesai = len(df[df['Tarikh'].dt.date < today])
tahun_list = sorted([int(t) for t in df['Tahun'].unique() if 2025 <= t <= 2027], reverse=True)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)
jumlah_program_tahun_ini = len(df[df['Tahun'] == tahun_dipilih])

# --- ✅ Butang-Butang Senarai ---
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button(f"📊 Jumlah Program\n({jumlah_program})"):
        with st.expander("📋 Semua Program", expanded=True):
            df_view = df[['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
            df_view.index = range(1, len(df_view) + 1)
            st.dataframe(df_view, use_container_width=True)

    if col2.button(f"📌 Hari Ini\n({jumlah_program_hari_ini})"):
        with st.expander("📋 Program Hari Ini", expanded=True):
            df_view = program_hari_ini[['Tarikh', 'Aktiviti', 'Tempat']].copy()
            df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
            df_view.index = range(1, len(df_view) + 1)
            st.dataframe(df_view, use_container_width=True)

    if col3.button(f"📅 Akan Datang\n({jumlah_program_akan_datang})"):
        with st.expander("📋 Program Akan Datang", expanded=True):
            df_view = df[df['Tarikh'].dt.date > today][['Tarikh', 'Aktiviti', 'Tempat']]
            df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
            df_view.index = range(1, len(df_view) + 1)
            st.dataframe(df_view, use_container_width=True)

    if col4.button(f"📆 Program {tahun_dipilih}\n({jumlah_program_tahun_ini})"):
        with st.expander(f"📋 Program Tahun {tahun_dipilih}", expanded=True):
            df_view = df[df['Tahun'] == tahun_dipilih][['Tarikh', 'Aktiviti', 'Tempat']]
            df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
            df_view.index = range(1, len(df_view) + 1)
            st.dataframe(df_view, use_container_width=True)

    if col5.button(f"✅ Selesai\n({jumlah_program_selesai})"):
        with st.expander("📋 Program Telah Selesai", expanded=True):
            df_view = df[df['Tarikh'].dt.date < today][['Tarikh', 'Aktiviti', 'Tempat']]
            df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
            df_view.index = range(1, len(df_view) + 1)
            st.dataframe(df_view, use_container_width=True)

# --- ✅ Paparan Bulan Dipilih ---
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
    df_view = df_tapis[['Tarikh', 'Aktiviti', 'Tempat']]
    df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
    df_view.index = range(1, len(df_view) + 1)
    st.dataframe(df_view, use_container_width=True)

# --- ✅ Program Terdekat ---
st.markdown("## 📅 Program Yang Terdekat")
df_terdekat = df[df['Tarikh'].dt.date >= today].sort_values('Tarikh').head(3)
if df_terdekat.empty:
    st.info("❌ Tiada program akan datang setakat ini.")
else:
    df_view = df_terdekat[['Tarikh', 'Aktiviti', 'Tempat']]
    df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%A, %d %B %Y')
    df_view.index = range(1, len(df_view) + 1)
    st.dataframe(df_view, use_container_width=True)

# --- ✅ Cari Program Ikut Tarikh ---
tarikh_dicari = st.date_input("📆 Pilih Tarikh Untuk Lihat Program", today)
df_dicari = df[df['Tarikh'].dt.date == tarikh_dicari]
st.markdown(f"## 🔍 Program Pada {tarikh_dicari.strftime('%A, %d %B %Y')}")

if df_dicari.empty:
    st.info("❌ Tiada program pada tarikh ini.")
else:
    df_view = df_dicari[['Tarikh', 'Aktiviti', 'Tempat']]
    df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
    df_view.index = range(1, len(df_view) + 1)
    st.dataframe(df_view, use_container_width=True)

# --- ✅ Footer ---
footer_html = """
<div class="footer">
    <b>DIBANGUNKAN OLEH JABATAN SETIAUSAHA DPPKR</b><br>
    <span>&#128231;</span> <a href="mailto:dppkrembau@gmail.com">Email</a> |
    <span>&#128279;</span> <a href="https://facebook.com/pemudapasrembau" target="_blank">Facebook</a><br> 
    <span>&#128222;</span> SU: <a href="tel:+60136343231">HAKIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60136343231" target="_blank">WhatsApp</a><br>
    <span>&#128222;</span> PSU 1: <a href="tel:+60173607925">NAIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60173607925" target="_blank">WhatsApp</a>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
