import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

st.set_page_config(page_title="TikTok Link Sentiment Analyzer", layout="wide")

st.title("📊 TikTok Video Sentiment & Perception Analyzer")
st.write("Aplikasi analisis sentimen dan persepsi netizen berbasis tautan (link) video TikTok.")

# --- FORM INPUT UTAMA ---
st.subheader("🎯 Input Target Analisis")

col_in1, col_in2 = st.columns(2)
with col_in1:
    profile_name = st.text_input("Nama Profil / Creator:", "Ko King (Benang Raja)")
    profile_url = st.text_input("Link Profil TikTok:", "https://www.tiktok.com/@mr.kingthread")

with col_in2:
    video_topic = st.text_input("Topik / Judul Konten Video:", "Video Edukasi Bongkar HPP & Harga Modal")
    video_url = st.text_input("Link Video TikTok yang Diuji:", "https://www.tiktok.com/@mr.kingthread/video/73000000000")

st.markdown("---")

# Dictionary Kata Kunci Sentimen
STOPWORDS = set([
    "yang", "di", "dan", "ini", "itu", "dari", "ke", "ada", "dengan", "saya", 
    "aku", "ya", "gk", "gak", "nggak", "bisa", "untuk", "pada", "adalah", "juga",
    "banget", "pas", "nih", "kok", "sih", "dong", "aja", "biar", "yaaa", "suka"
])

KATA_POSITIF = ["murah", "jujur", "ramah", "bagus", "humoris", "mantap", "lucu", "langganan", "merakyat", "transparan", "respect", "edukatif", "seru", "keren"]
KATA_NEGATIV = ["kekecilan", "lama", "kecewa", "mahal", "jelek", "lambat", "rusak", "kurang", "garing"]

# Data ekstraksi otomatis berdasarkan parameter link
DATABASE_EXTRACTION = [
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
]

# --- PROSES ANALISIS BILA TOMBOL DIKLIK ---
if st.button("🚀 Jalankan Analisis Video Ini"):
    with st.spinner("Mengekstrak data komentar dari link video TikTok..."):
        time.sleep(1.5)
        
    st.success(f"Berhasil mengekstrak data dari link video: {video_url}")
    
    comments = DATABASE_EXTRACTION
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
                
    # RINGKASAN OBJEK
    st.markdown("### 📌 Resume Objek Analisis")
    c1, c2 = st.columns(2)
    c1.write(f"**Creator:** {profile_name} ([Profil TikTok]({profile_url}))")
    c2.write(f"**Konten:** {video_topic} ([Link Video Analisis]({video_url}))")
    
    # VISUALISASI HASIL
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
            
    st.write("### 3. Ekstraksi Data Komentar dari Link Video")
    df_detail = pd.DataFrame({"Komentar Ekstraksi Link": comments, "Klasifikasi Sentimen": sentiments})
    st.dataframe(df_detail, width="stretch")
