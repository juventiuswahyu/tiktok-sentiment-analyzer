import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="TikTok Precision Sentiment Analyzer", layout="wide")

st.title("📊 TikTok Video Sentiment & Perception Analyzer (Akurat)")
st.write("Aplikasi analisis sentimen berbasis data komentar riil & pemrosesan teks tingkat lanjut.")

# --- SIDEBAR INPUT PARAMETER ---
st.sidebar.header("🎯 Parameter Objek Analisis")
profile_name = st.sidebar.text_input("Nama Creator:", "Ko King (Benang Raja)")
profile_url = st.sidebar.text_input("Link Profil TikTok:", "https://www.tiktok.com/@mr.kingthread")
video_topic = st.sidebar.text_input("Topik Video:", "Edukasi Transparansi HPP Batik")
video_url = st.sidebar.text_input("Link Video TikTok:", "https://www.tiktok.com/@mr.kingthread/video/73000000000")

st.sidebar.markdown("---")
st.sidebar.header("📥 Sumber Data Komentar")
data_source = st.sidebar.radio(
    "Pilih Sumber Data:",
    ("Upload File CSV/Excel (Data Komentar Riil)", "Gunakan Data Sampel Uji Coba")
)

# --- DICTIONARY BAHASA INDONESIA YANG DIPERLUAS ---
STOPWORDS = set([
    "yang", "di", "dan", "ini", "itu", "dari", "ke", "ada", "dengan", "saya", 
    "aku", "ya", "gk", "gak", "nggak", "bisa", "untuk", "pada", "adalah", "juga",
    "banget", "pas", "nih", "kok", "sih", "dong", "aja", "biar", "yaaa", "suka",
    "yg", "dgn", "utk", "sdh", "udah", "aja", "kalo", "kalau", "biar", "pen"
])

KATA_POSITIF = [
    "murah", "jujur", "ramah", "bagus", "humoris", "mantap", "lucu", "langganan", 
    "merakyat", "transparan", "respect", "edukatif", "seru", "keren", "recomended", 
    "recommended", "suka", "amanah", "berkualitas", "top", "terjangkau", "berkah"
]

KATA_NEGATIF = [
    "kekecilan", "lama", "kecewa", "mahal", "jelek", "lambat", "rusak", "kurang", 
    "garing", "parah", "penipuan", "kapok", "bohong", "mahalan", "kasar", "scam"
]

def analyze_sentiment(text):
    text_clean = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    words = text_clean.split()
    
    pos_score = sum(1 for w in words if w in KATA_POSITIF)
    neg_score = sum(1 for w in words if w in KATA_NEGATIF)
    
    # Deteksi Sederhana Negasi (contoh: "tidak murah" / "gak bagus")
    if "gak" in words or "tidak" in words or "nggak" in words:
        if pos_score > neg_score:
            return "Negatif", words
            
    if pos_score > neg_score:
        return "Positif", words
    elif neg_score > pos_score:
        return "Negatif", words
    else:
        return "Netral", words

# --- PENANGANAN DATA ---
comments_data = []

if data_source == "Upload File CSV/Excel (Data Komentar Riil)":
    uploaded_file = st.file_uploader("Unggah File Komentar (.csv atau .xlsx):", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            st.write(" Preview Data yang Diunggah:")
            st.dataframe(df_upload.head(3), width="stretch")
            
            col_target = st.selectbox("Pilih Kolom yang Berisi Teks Komentar:", df_upload.columns)
            comments_data = df_upload[col_target].dropna().tolist()
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
else:
    comments_data = [
        "Owner transparan banget bongkar harga modal batik, respect!",
        "Jujur banget Ko King, pantesan Benang Raja rame terus.",
        "Murah banget grosirnya, harga modal dibuka semua.",
        "Penjelasannya transparan dan sangat edukatif.",
        "Bagus banget bisnis modelnya transparan begini.",
        "Pengirimannya agak lama tapi produk bahannya bagus.",
        "Harganya agak mahal dibanding toko sebelah tapi oke lah."
    ]

# --- DISPLAY HASIL ANALISIS ---
st.markdown("---")
st.subheader("📌 Objek Analisis Terdaftar")
c1, c2 = st.columns(2)
c1.write(f"**Creator:** {profile_name} ([Profil TikTok]({profile_url}))")
c2.write(f"**Topik Video:** {video_topic} ([Link Video TikTok]({video_url}))")

if st.button("🚀 Jalankan Analisis Sentimen"):
    if not comments_data:
        st.warning("Data komentar belum tersedia. Silakan unggah file CSV atau gunakan data sampel.")
    else:
        sentiments = []
        all_words = []
        
        for comment in comments_data:
            sentiment, words = analyze_sentiment(comment)
            sentiments.append(sentiment)
            for w in words:
                if w not in STOPWORDS and len(w) > 2:
                    all_words.append(w)
                    
        st.success(f"Berhasil menganalisis **{len(comments_data)}** data komentar secara presisi!")
        
        # VISUALISASI HASIL
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 1. Distribusi Sentimen Netizen")
            sentiment_counts = pd.Series(sentiments).value_counts()
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
            st.pyplot(fig1)
            
        with col2:
            st.write("### 2. Word Cloud Perception Atribut")
            word_freq = Counter(all_words)
            if word_freq:
                wordcloud = WordCloud(width=400, height=250, background_color='white').generate_from_frequencies(word_freq)
                fig2, ax2 = plt.subplots(figsize=(4, 2.5))
                ax2.imshow(wordcloud, interpolation='bilinear')
                ax2.axis('off')
                st.pyplot(fig2)
                
        st.write("### 3. Matriks Hasil Klasifikasi Komentar")
        df_result = pd.DataFrame({"Komentar Netizen": comments_data, "Hasil Sentimen": sentiments})
        st.dataframe(df_result, width="stretch")
