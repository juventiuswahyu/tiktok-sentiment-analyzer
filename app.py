import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="TikTok Sentiment Analyzer", layout="wide")

st.title("📊 TikTok Video Sentiment & Perception Analyzer")
st.write("Analisis sentimen dan persepsi netizen berdasarkan link video TikTok.")

# --- SIDEBAR INPUT ---
st.sidebar.header("🔗 Parameter Analisis")
profile_name = st.sidebar.text_input("Nama Profil / Creator:", "Ko King (Benang Raja)")
profile_url = st.sidebar.text_input("Link Profil TikTok:", "https://www.tiktok.com/@mr.kingthread")
video_url = st.sidebar.text_input("Link Video TikTok yang Diuji:", "https://www.tiktok.com/@mr.kingthread/video/73000000000")
video_topic = st.sidebar.text_input("Judul / Topik Video Spesifik:", "Video Edukasi Bongkar HPP & Harga Modal")

st.sidebar.markdown("---")
st.sidebar.header("📥 Sumber Data Komentar")
mode_input = st.sidebar.radio(
    "Pilih Metode Input Komentar:",
    ("Copas Manual Komentar Riil", "Gunakan Simulasi Data Otomatis")
)

# STOPWORDS & DICTIONARY
STOPWORDS = set([
    "yang", "di", "dan", "ini", "itu", "dari", "ke", "ada", "dengan", "saya", 
    "aku", "ya", "gk", "gak", "nggak", "bisa", "untuk", "pada", "adalah", "juga",
    "banget", "pas", "nih", "kok", "sih", "dong", "aja", "biar", "yaaa", "suka"
])

KATA_POSITIF = ["murah", "jujur", "ramah", "bagus", "humoris", "mantap", "lucu", "langganan", "merakyat", "transparan", "respect", "edukatif", "seru", "keren"]
KATA_NEGATIV = ["kekecilan", "lama", "kecewa", "mahal", "jelek", "lambat", "rusak", "kurang", "garing"]

DEMO_COMMENTS = """
Owner transparan banget bongkar harga modal batik, respect!
Jujur banget Ko King, pantesan Benang Raja rame terus.
Murah banget grosirnya, harga modal dibuka semua.
Penjelasannya transparan dan sangat edukatif.
Bagus banget bisnis modelnya transparan begini.
Ko King mantap jujur banget pas bilang harga bahan.
Beli batik di sini emang paling recommended, jujur harganya.
Pernah beli emang murah banget dibanding toko sebelah.
Lama banget pengirimannya kemarin tapi bahannya bagus.
Transparan gini bikin pembeli makin percaya respect!
"""

# --- DISPLAY OBJEK ANALISIS ---
st.subheader("📌 Informasi Objek Analisis")
col_a, col_b = st.columns(2)
with col_a:
    st.write(f"**Creator:** {profile_name}")
    st.write(f"**Link Profil:** [{profile_url}]({profile_url})")
with col_b:
    st.write(f"**Topik Video:** {video_topic}")
    st.write(f"**Link Video Analisis:** [{video_url}]({video_url})")

st.markdown("---")

# Area Input Komentar
if mode_input == "Copas Manual Komentar Riil":
    st.subheader("📝 Tempelkan (Copas) Komentar Riil dari TikTok")
    raw_input = st.text_area(
        "Salin komentar-komentar dari video TikTok di atas, lalu tempel di sini (pisahkan per baris):", 
        height=180,
        placeholder="Contoh:\nBagus banget kontennya!\nHarganya murah dan jujur.\nPengirimannya agak lama."
    )
    comments = [line.strip() for line in raw_input.split("\n") if line.strip()]
else:
    st.subheader("⚡ Mode Simulasi Data Otomatis")
    st.info("Menggunakan dataset sampel komentar bawaan sistem untuk pengujian cepat.")
    comments = [line.strip() for line in DEMO_COMMENTS.strip().split("\n") if line.strip()]

# --- PROSES ANALISIS ---
if st.button("🚀 Jalankan Analisis Video Ini"):
    if not comments:
        st.error("Silakan tempelkan komentar terlebih dahulu di kotak teks di atas!")
    else:
        st.success(f"Berhasil menganalisis {len(comments)} data komentar untuk video ini!")
        
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
                    
        # VISUALISASI
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 1. Distribusi Sentimen Netizen")
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
                
        st.write("### 3. Detail Hasil Ekstraksi Per Komentar")
        df_detail = pd.DataFrame({"Komentar Netizen": comments, "Klasifikasi Sentimen": sentiments})
        st.dataframe(df_detail, width="stretch")
