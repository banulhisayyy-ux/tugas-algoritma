import streamlit as st # type: ignore
import pandas as pd # type: ignore
import random

# --- KONFIGURASI HALAMAN MODERN ---
st.set_page_config(
    page_title="MiniTube-Tok",
    page_icon="logo.png",
    layout="centered"
)

# --- CSS KUSTOM UNTUK TAMPILAN MODERN ---
# Kita gunakan CSS agar tampilan Card, Tombol, dan Judul terlihat lebih bersih.
# --- CSS KUSTOM UNTUK PERBAIKAN TAMPILAN SIDEBAR ---
st.markdown("""
<style>
    /* 1. Perbaikan Sidebar agar Teks Jelas Terbaca */
    /* Kita pastikan latar belakang sidebar putih, dan warna teks gelap */
    [data-testid="stSidebar"] {
        background-color: #ffffff; /* Latar belakang sidebar putih bersih */
        color: #1a1a1a !important; /* Paksa warna teks utama jadi hitam/gelap */
    }

    /* Memastikan teks label di atas menu juga gelap */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #1a1a1a !important;
    }

    /* Mengatur warna judul di sidebar (StreamFolio) agar tetap Merah */
    [data-testid="stSidebar"] h1 {
        color: #ff4b4b !important;
    }

    /* 2. Styling untuk Card Video (Agar tetap modern) */
    [data-testid="stVerticalBlock"] > div:has(div.stVideo) {
        border: 1px solid #e6e6e6;
        border-radius: 15px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)


# --- DATABASE LOKAL LENGKAP (VIDEO BARU) ---
# Di sini kita gunakan URL video dummy "Big Buck Bunny" dan "Elephant's Dream" yang stabil.
if 'video_db' not in st.session_state:
    st.session_state.video_db = [
        {
            "id": 1, 
            "judul": "🎬 Petualangan Kelinci Putih: Babak 1", 
            "kreator": "Blender Foundation", 
            "tag": "Animasi", 
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", 
            "likes": 1205
        },
        {
            "id": 2, 
            "judul": "🐘 Elephant's Dream: Sebuah Kisah Fantasi", 
            "kreator": "Studio Orange", 
            "tag": "Hiburan", 
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4", 
            "likes": 850
        },
        {
            "id": 3, 
            "judul": "👨‍💻 Tutorial Dasar Membuat UI Streamlit", 
            "kreator": "BudiTech", 
            "tag": "Pendidikan", 
            "url": "https://www.w3schools.com/html/mov_bbb.mp4", # Dummy lainnya
            "likes": 430
        },
        {
            "id": 4, 
            "judul": "Gaya Hidup Digital di Purbalingga", 
            "kreator": "LokalKonten", 
            "tag": "Gaya Hidup", 
            "url": "https://www.w3schools.com/html/movie.mp4", # Dummy lainnya
            "likes": 210
        },
    ]

# --- UI SIDEBAR (DENGAN LOGO) ---
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    st.sidebar.markdown("<h1 style='text-align: center; color: #ff4b4b;'>MiniTube-Tok</h1>", unsafe_allow_html=True)

st.sidebar.caption("<p style='text-align: center;'>Modern Video App Concept</p>", unsafe_allow_html=True)
st.sidebar.divider()
menu = st.sidebar.radio("Main Menu:", ["✨ For You Page", "🔍 Explore", "📤 Upload"])

# --- MODUL 1: TIKTOK MODE (FYP MODERN) ---
if menu == "✨ For You Page":
    st.header("✨ For You Page")
    st.caption("Nikmati feed video yang dipersonalisasi untukmu.")
    st.write("---")
    
    # Menampilkan video secara acak (simulasi algoritma FYP)
    videos = st.session_state.video_db.copy()
    random.shuffle(videos)
    
    for v in videos:
        with st.container():
            # Styling Judul dan Meta menggunakan CSS class yang dibuat di atas
            st.markdown(f"<div class='video-title'>{v['judul']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='video-meta'>Oleh: {v['kreator']} | Kategori: <b>{v['tag']}</b></div>", unsafe_allow_html=True)
            
            # Video Player (Lebar penuh di dalam card)
            st.video(v['url'])
            
            # Kolom Tombol Interaksi ala Modern
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                st.button(f"❤️ {v['likes']:,}", key=f"like_{v['id']}")
            with col2:
                st.button("💬 Komentar", key=f"com_{v['id']}")
            with col3:
                st.button("🔗 Bagikan", key=f"sh_{v['id']}")
            st.write(" ") # Jarak tambahan

# --- MODUL 2: YOUTUBE MODE (EXPLORE MODERN) ---
elif menu == "🔍 Explore":
    st.header("🔍 Explore")
    
    # Search & Filter dalam satu container agar rapi
    with st.expander("Filter & Pencarian", expanded=True):
        query = st.text_input("Cari video, kreator, atau tag...")
        available_tags = list(set([v['tag'] for v in st.session_state.video_db]))
        tags = st.multiselect("Pilih Kategori:", available_tags)
    
    st.divider()

    # Logic Filter
    filtered = st.session_state.video_db
    if query:
        filtered = [v for v in filtered if query.lower() in v['judul'].lower() or query.lower() in v['tag'].lower()]
    if tags:
        filtered = [v for v in filtered if v['tag'] in tags]
    
    # Tampilkan Grid (2 kolom)
    if not filtered:
        st.info("Tidak ada video yang ditemukan.")
    else:
        cols = st.columns(2)
        for i, v in enumerate(filtered):
            with cols[i % 2]:
                with st.container():
                    # Thumbnail (Palsu) - Gunakan LoremFlickr untuk gambar random
                    st.image(f"https://loremflickr.com/400/225/video,{v['tag']}/all", use_column_width=True, caption=f"Kategori: {v['tag']}")
                    st.subheader(v['judul'])
                    st.write(f"👤 {v['kreator']} | ❤️ {v['likes']:,}")
                    if st.button("Tonton", key=f"watch_{v['id']}"):
                        st.video(v['url'])
                    st.write("") # Jarak tambahan

# --- MODUL 3: UPLOAD VIDEO ---
elif menu == "📤 Upload":
    st.header("📤 Upload Konten Baru")
    st.caption("Dukung kreator lokal dengan mengupload video original kamu.")
    st.write("---")

    with st.form("form_upload", clear_on_submit=True):
        judul = st.text_input("Judul Video")
        kreator = st.text_input("Nama Kreator / Channel")
        kategori = st.selectbox("Kategori", ["Animasi", "Hiburan", "Pendidikan", "Gaya Hidup", "Teknologi"])
        
        # Di versi sederhana ini, kita hanya upload metadata. Video default dipasang.
        st.info("Catatan: Di demo ini, video yang diupload akan menggunakan video dummy secara otomatis.")
        
        uploaded_file = st.file_uploader("Pilih file video (MP4)", type=["mp4"])
        
        submit = st.form_submit_button("Publish Video")
        
        if submit and judul and kreator:
            new_id = len(st.session_state.video_db) + 1
            new_entry = {
                "id": new_id,
                "judul": judul,
                "kreator": kreator,
                "tag": kategori,
                # Gunakan URL yang stabil untuk demo upload
                "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "likes": 0
            }
            st.session_state.video_db.append(new_entry)
            st.success(f"Video '{judul}' berhasil di-upload ke sistem!")
            st.balloons()