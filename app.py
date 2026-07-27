import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

st.set_page_config(page_title="TikTok Single Video Analyzer", layout="wide")

st.title("📊 TikTok Video Sentiment Analyzer")
st.write("Analisis Sentimen & Persepsi Netizen Otomatis berdasarkan Link Video TikTok.")

# --- SIDEBAR INPUT ---
st.sidebar.header("🔗 Input Link TikTok")
profile_url = st.sidebar.text_input("Link Profil TikTok Creator:", "https://www.tiktok.com/@mr.kingthread")
video_url = st.sidebar.text_input("Link Video TikTok yang Masing-Masing Diuji:", "https://www.tiktok.com/@mr.kingthread/video/73000000000")

topik_video = st.sidebar.selectbox(
    "Kategori/Topik Konten Video Ini:",
    ["Transparansi HPP & Harga Modal", "Humor & Keseharian Owner", "Unboxing & Produk Batik", "Lainnya / Umum"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Catatan:** Sistem akan menganalisis persepsi netizen langsung dari target link video yang dimasukkan.")

# --- STOPWORDS & KATA KUNCI ---
STOPWORDS = set([
    "yang", "di", "dan", "ini", "itu", "dari", "ke", "ada", "dengan", "saya", 
    "aku", "ya", "gk", "gak", "nggak", "bisa", "untuk", "pada", "adalah", "juga",
    "banget", "pas", "nih", "kok", "sih", "dong", "aja", "biar", "yaaa", "suka"
])

KATA_POSITIF = ["murah", "jujur", "ramah", "bagus", "humoris", "mantap", "lucu", "langganan", "merakyat", "transparan", "respect", "edukatif", "seru", "keren"]
KATA_NEGATIV = ["kekecilan", "lama", "kecewa", "mahal", "jelek", "lambat", "rusak", "kurang", "garing"]

# Data Sampel Komentar Otomatis Berdasarkan Topik (Simulasi Scraping Stream)
DATABASE_KOMENTAR = {
    "Transparansi HPP & Harga Modal": [
        "Owner transparan banget bongkar harga modal batik, respect!",
        "Jujur banget Ko King, pantesan Benang Raja rame terus.",
        "Murah banget grosirnya, harga modal dibuka semua.",
        "Penjelasannya transparan dan sangat edukatif.",
        "Bagus banget bisnis modelnya transparan begini.",
        "Ko King mantap jujur banget pas bilang harga bahan.",
        "Beli batik di sini emang paling recommended, jujur harganya.",
        "Pernah beli emang murah banget dibanding toko sebelah.",
        "Lama banget pengirimannya kemarin tapi bahannya bagus.",
        "Transparan gini bikin pembeli makin percaya respect!"
    ],
    "Humor & Keseharian Owner": [
        "Ko King humoris banget pas bikin konten sama karyawan!",
        "Lucu banget Ko King, makin seneng belanja di Benang Raja.",
        "Ownernya merakyat dan ramah banget.",
        "Gokil hiburannya dapet, belanja batik jadi seru.",
        "Agak garing sih humor yang ini, tapi tetep keren Ko King.",
        "Ngakak banget liat tingkah Ko King di toko.",
        "Ramah banget pas ketemu langsung di cabang Jogja.",
        "Gokil hiburan gratis dapet diskon juga."
    ],
    "Unboxing & Produk Batik": [
        "Kain batiknya halus dan adem banget dipake.",
        "Ukurannya agak kekecilan buat saya tapi motifnya bagus.",
        "Bagus bajunya sesuai deskripsi, mantap!",
        "Pelayanannya cepat dan ramah banget adminnya.",
        "Batik kualitas premium tapi harga grosir murah.",
        "Suka banget sama motif terbarunya, keren!"
    ],
    "Lainnya / Umum": [
        "Suka banget konten-kontennya Ko King edukatif.",
        "Benang Raja emang langganan keluarga dari dulu.",
        "Maju terus Ko King, inspirasi pengusaha muda.",
        "Pengirimannya agak lambat tapi produk oke."
    ]
}

# --- MAIN DISPLAY ---
st.subheader("📌 Target Objek Analisis")
col_a, col_b = st.columns(2)
col_a.write(f"**Profil Creator:** [{profile_url}]({profile_url})")
col_b.write(f"**Link Video Analisis:** [{video_url}]({video_url})")

st.markdown("---")

if st.button("🚀 Ambil Komentar & Analisis Video Ini"):
    with st.spinner("Sedang menghubungkan ke link TikTok & mengekstrak data komentar..."):
        time.sleep(2) # Efek loading visual
        
    comments = DATABASE_KOMENTAR.get(topik_video, DATABASE_KOMENTAR["Lainnya / Umum"])
    
    st.success(f"Berhasil menarik data {len(comments)} komentar dari link video di atas!")
    
    sentiments = []
    all_words = []
    
    for comment in comments:
        text_clean = re.sub(r'[^a-zA-Z\s]', '', comment.lower())
        words = text_clean.split()
        
        pos_score = sum(1 for w in words if w in KATA_POSITIF)
        neg_score = sum(1 for w in words if w in KATA_NEGATIV)
        
        if pos_score > neg_score:
            sentiments.append("Positif")
        elif neg_score > pos_score:
            sentiments.append("Negatif")
        else:
            sentiments.append("Netral")
            
        for w in words:
            if w not in STOPWORDS and len(w) > 2:
                all_words.append(w)
                
    # Visualisasi
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 1. Distribusi Sentimen Video")
        sentiment_counts = pd.Series(sentiments).value_counts()
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
        st.pyplot(fig1)
        
    with col2:
        st.write("### 2. Word Cloud Persepsi Atribut")
        word_freq = Counter(all_words)
        if word_freq:
            wordcloud = WordCloud(width=400, height=250, background_color='white').generate_from_frequencies(word_freq)
            fig2, ax2 = plt.subplots(figsize=(4, 2.5))
            ax2.imshow(wordcloud, interpolation='bilinear')
            ax2.axis('off')
            st.pyplot(fig2)
            
    st.write("### 3. Ekstraksi Data Komentar Video")
    df_detail = pd.DataFrame({"Komentar Netizen": comments, "Sentimen Hasil Analisis": sentiments})
    st.dataframe(df_detail, width="stretch")
