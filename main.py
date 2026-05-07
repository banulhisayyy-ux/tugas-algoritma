import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="MiniTube-Tok",
    page_icon="logo.png", # Menggunakan file logo kamu
    layout="centered"
)

# --- CSS KUSTOM UNTUK WARNA & TAMPILAN SIDEBAR ---
st.markdown("""
<style>
    /* Mengatasi teks sidebar yang tidak kelihatan */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] h1 {
        color: #ff4b4b !important;
    }
    
    /* Styling Card Video */
    [data-testid="stVerticalBlock"] > div:has(div.stVideo) {
        border: 1px solid #e6e6e6;
        border-radius: 15px;
        padding: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .video-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    .video-meta {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 15px;
    }
    .comment-box {
        background-color: #f8f9fa;
        padding: 10px 15px;
        border-radius: 8px;
        margin-top: 5px;
        margin-bottom: 5px;
        border-left: 3px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE VIDEO ASLI (YOUTUBE) ---
# Menggunakan video YouTube asli agar judul dan isi videonya sama persis!
if 'video_db' not in st.session_state:
    st.session_state.video_db = [
        {
            "id": 1, 
            "judul": "🎬 Trailer Animasi Big Buck Bunny Resmi", 
            "kreator": "Blender Foundation", 
            "tag": "Animasi", 
            "url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ", 
            "likes": 1205,
            "komentar": ["Bagus banget animasinya!", "Kelincinya lucu pol!"]
        },
        {
            "id": 2, 
            "judul": "JAPAN | Sony FX30 | Cinematic Travel Film | Tamron 17-70mm f/2.8", 
            "kreator": "Jun Chew", 
            "tag": "Hiburan", 
            "url": "https://www.youtube.com/watch?v=ChxDEAN8EtY", 
            "likes": 16200,
            "komentar": ["Truly beautiful", "Awesome video bro!"]
        },
        {
            "id": 3, 
            "judul": "👨‍💻 Belajar Python Dasar dalam 10 Menit", 
            "kreator": "Suka Koding", 
            "tag": "Pendidikan", 
            "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", 
            "likes": 430,
            "komentar": ["Sangat membantu buat pemula!", "Penjelasannya gampang dimengerti."]
        },
        {
            "id": 4, 
            "judul": "4K Cinematic | BMW M4 Competition", 
            "kreator": "Ark Cinematics ", 
            "tag": "Cinematic", 
            "url": "https://www.youtube.com/watch?v=MktCSJmpTI4", 
            "likes": 5721,
            "komentar": ["Thanks for the edit❤", "this is perfect for edit"]
        }
    ]

# --- UI SIDEBAR DENGAN LOGO ---
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    st.sidebar.markdown("<h1 style='text-align: center; color: #ff4b4b;'>MiniTube-Tok</h1>", unsafe_allow_html=True)

st.sidebar.caption("<p style='text-align: center;'>Aplikasi Video Modern</p>", unsafe_allow_html=True)
st.sidebar.divider()
menu = st.sidebar.radio("Main Menu:", ["✨ For You Page", "🔍 Explore", "📤 Upload"])

# --- MENU 1: FOR YOU PAGE ---
if menu == "✨ For You Page":
    st.header("✨ For You Page")
    st.caption("Video pilihan terbaik untuk menemani harimu.")
    st.write("---")
    
    for v in st.session_state.video_db:
        # Inisialisasi state interaksi jika belum ada
        if f"likes_{v['id']}" not in st.session_state:
            st.session_state[f"likes_{v['id']}"] = v['likes']
        if f"show_comm_{v['id']}" not in st.session_state:
            st.session_state[f"show_comm_{v['id']}"] = False
            
        with st.container():
            st.markdown(f"<div class='video-title'>{v['judul']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='video-meta'>Kreator: <b>{v['kreator']}</b> | Kategori: <span style='color:#ff4b4b;'>{v['tag']}</span></div>", unsafe_allow_html=True)
            
            # Putar video YouTube
            st.video(v['url'])
            
            # Tombol Interaksi (Like, Komen, Share)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Logika Like Bertambah saat diklik
                if st.button(f"❤️ {st.session_state[f'likes_{v['id']}']} Likes", key=f"btn_like_{v['id']}"):
                    st.session_state[f"likes_{v['id']}"] += 1
                    st.rerun()
                    
            with col2:
                # Logika Tampilkan/Sembunyikan Kolom Komentar
                if st.button(f"💬 Komentar ({len(v['komentar'])})", key=f"btn_comm_{v['id']}"):
                    st.session_state[f"show_comm_{v['id']}"] = not st.session_state[f"show_comm_{v['id']}"]
                    st.rerun()
                    
            with col3:
                if st.button("🔗 Bagikan", key=f"btn_share_{v['id']}"):
                    st.toast("Link berhasil disalin!")
            
            # Bagian Kolom Komentar (Hanya muncul jika tombol komentar diklik)
            if st.session_state[f"show_comm_{v['id']}"]:
                st.write("---")
                st.write("**Komentar Netizen:**")
                
                # Tampilkan list komentar yang sudah ada
                for k in v['komentar']:
                    st.markdown(f"<div class='comment-box'>💬 {k}</div>", unsafe_allow_html=True)
                
                # Input komentar baru
                new_comm = st.text_input("Tulis komentar kamu...", key=f"input_comm_{v['id']}", placeholder="Tulis di sini...")
                if st.button("Kirim", key=f"btn_send_{v['id']}"):
                    if new_comm:
                        v['komentar'].append(new_comm)
                        st.success("Komentar berhasil ditambahkan!")
                        st.rerun()

# --- MENU 2: EXPLORE ---
elif menu == "🔍 Explore":
    st.header("🔍 Explore")
    query = st.text_input("Cari video berdasarkan judul atau kategori...")
    
    filtered = [v for v in st.session_state.video_db if query.lower() in v['judul'].lower() or query.lower() in v['tag'].lower()]
    
    st.divider()
    if not filtered:
        st.info("Video tidak ditemukan.")
    else:
        for v in filtered:
            with st.container():
                st.subheader(v['judul'])
                st.video(v['url'])

# --- MENU 3: UPLOAD ---
elif menu == "📤 Upload":
    st.header("📤 Upload Konten")
    with st.form("form_upload", clear_on_submit=True):
        judul = st.text_input("Judul Video")
        kreator = st.text_input("Nama Kreator")
        kategori = st.selectbox("Kategori", ["Animasi", "Hiburan", "Pendidikan"])
        url = st.text_input("Link Video YouTube", placeholder="https://www.youtube.com/watch?v=...")
        
        submit = st.form_submit_button("Publish Video")
        if submit and judul and url:
            new_id = len(st.session_state.video_db) + 1
            st.session_state.video_db.append({
                "id": new_id,
                "judul": judul,
                "kreator": kreator,
                "tag": kategori,
                "url": url,
                "likes": 0,
                "komentar": []
            })
            st.success("Video baru berhasil dipublikasikan!")
            st.balloons()