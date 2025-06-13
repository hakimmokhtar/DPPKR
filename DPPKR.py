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

today = datetime.date.today()
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

    if len(aktiviti_list) == 1:
        st.toast(f"📢 Program Hari Ini: {aktiviti_list[0]}", icon="📌")
    else:
        st.toast(f"📢 {len(aktiviti_list)} Program Hari Ini!", icon="📌")
        for aktiviti in aktiviti_list:
            st.toast(f"📌 {aktiviti}")

    mesej_wa = f"*Program Hari Ini ({today.strftime('%A, %d %B %Y')})*\n"
    for aktiviti, tempat in zip(aktiviti_list, tempat_list):
        mesej_wa += f"📌 {aktiviti}\n📍 {tempat}\n\n"

    pautan_wa = f"https://wa.me/?text={quote(mesej_wa)}"
    st.markdown(f"[📤 Kongsi ke WhatsApp]({pautan_wa})", unsafe_allow_html=True)

jumlah_program = len(df)
jumlah_program_hari_ini = len(program_hari_ini)
jumlah_program_akan_datang = len(df[df['Tarikh'].dt.date > today])

tahun_list = sorted(
    [int(t) for t in df['Tahun'].dropna().unique() if 2025 <= t <= 2027],
    reverse=True
)
tahun_dipilih = st.selectbox("Pilih Tahun", tahun_list)

jumlah_program_tahun_ini = len(df[df['Tahun'] == tahun_dipilih])
jumlah_program_selesai = len(df[df['Tarikh'].dt.date < today])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Jumlah Program", jumlah_program)
col2.metric("Program Hari Ini", jumlah_program_hari_ini)
col3.metric("Akan Datang", jumlah_program_akan_datang)
col4.metric(f"Program {tahun_dipilih}", jumlah_program_tahun_ini)
col5.metric("Program Selesai", jumlah_program_selesai)

bulan_penuh = [
    ('Januari', 1), ('Februari', 2), ('Mac', 3), ('April', 4),
    ('Mei', 5), ('Jun', 6), ('Julai', 7), ('Ogos', 8),
    ('September', 9), ('Oktober', 10), ('November', 11), ('Disember', 12)
]

bulan_nama_list = [b[0] for b in bulan_penuh]
bulan_nombor_list = [b[1] for b in bulan_penuh]

bulan_dipilih_nama = st.selectbox("Pilih Bulan", bulan_nama_list)
bulan_dipilih_index = bulan_nama_list.index(bulan_dipilih_nama)
bulan_dipilih_num = bulan_nombor_list[bulan_dipilih_index]

df['BulanNum'] = df['Tarikh'].dt.month
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

st.markdown("## 📅 Program Yang Terdekat")
df_akan_datang = df[df['Tarikh'].dt.date >= today].sort_values('Tarikh').head(3)

if df_akan_datang.empty:
    st.info("❌ Tiada program akan datang setakat ini.")
else:
    df_prog_akan_datang = df_akan_datang[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_prog_akan_datang['Tarikh'] = df_prog_akan_datang['Tarikh'].dt.strftime('%A, %d %B %Y')
    df_prog_akan_datang.reset_index(drop=True, inplace=True)
    df_prog_akan_datang.index += 1
    df_prog_akan_datang.index.name = 'Bil'
    st.dataframe(df_prog_akan_datang, use_container_width=True)

tarikh_dicari = st.date_input("📆 Pilih Tarikh Untuk Lihat Program", today)
df_tarikh_dicari = df[df['Tarikh'].dt.date == tarikh_dicari]

st.markdown(f"## 🔍 Program Pada {tarikh_dicari.strftime('%A, %d %B %Y')}")

if df_tarikh_dicari.empty:
    st.info("❌ Tiada program pada tarikh ini.")
else:
    df_view = df_tarikh_dicari[['Tarikh', 'Aktiviti', 'Tempat']].copy()
    df_view['Tarikh'] = df_view['Tarikh'].dt.strftime('%d %b %Y')
    df_view.reset_index(drop=True, inplace=True)
    df_view.index += 1
    df_view.index.name = 'Bil'
    st.dataframe(df_view, use_container_width=True)

st.markdown("""
    <style>
    .stAlert {
        background-color: #006e3c !important;
        color: white !important;
        border-left: 0.5rem solid white !important;
    }
    .stAlert > div {
        color: white !important;
        font-weight: normal;
    }
    .stAlert svg {
        fill: white !important;
    }
    </style>
""", unsafe_allow_html=True)

footer_style = """
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
"""

footer_html = """
<div class="footer">
    <b>DIBANGUNKAN OLEH JABATAN SETIAUSAHA DPPKR </b><br>
    <span>&#128231;</span> <a href="mailto:dppkrembau@gmail.com">Email</a> |
    <span>&#128279;</span> <a href="https://facebook.com/pemudapasrembau" target="_blank">Facebook </a><br> 
    <span>&#128222;</span> SU : <a href="tel:+60136343231">HAKIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60136343231" target="_blank">WhatsApp</a><br>
    <span>&#128222;</span> PSU 1: <a href="tel:+60173607925">NAIM</a> |
    <span>&#128172;</span> <a href="https://wa.me/60173607925" target="_blank">WhatsApp</a>
</div>
"""

st.markdown(footer_style + footer_html, unsafe_allow_html=True)

st.markdown("""
    <style>
    .element-container .stMetric label, .element-container .stMetric div {
        color: white !important;
    }
    .stMetric {
        background-color: #004d2a;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
