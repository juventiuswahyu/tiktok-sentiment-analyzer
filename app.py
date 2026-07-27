import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="TikTok Multi-Content Analyzer", layout="wide")

st.title("📊 TikTok Multi-Content Sentiment & Perception Analyzer")
st.write("Aplikasi komparatif analisis sentimen dan persepsi netizen untuk berbagai profil dan konten TikTok.")

# --- SIDEBAR: PROFIL CREATOR ---
st.sidebar.header("👤 Profil Target Analisis")
profile_name = st.sidebar.text_input("Nama Akun / Creator:", "Ko King (Benang Raja)")
profile_url = st.sidebar.text_input("Link Profil TikTok:", "https://www.tiktok.com/@mr.kingthread")

st.sidebar.markdown("---")
num_videos = st.sidebar.number_input("Jumlah Konten yang Ingin Dibandingkan:", min_value=1, max_value=5, value=3)

# Kata Buangan & Sentimen Dictionary
STOPWORDS = set([
    "yang", "di", "dan", "ini", "itu", "dari", "ke", "ada", "dengan", "saya", 
    "aku", "ya", "gk", "gak", "nggak", "bisa", "untuk", "pada", "adalah", "juga",
    "banget", "pas", "nih", "kok", "sih", "dong", "aja", "biar", "yaaa", "suka"
])

KATA_POSITIF = ["murah", "jujur", "ramah", "bagus", "humoris", "mantap", "lucu", "langganan", "merakyat", "transparan", "respect", "edukatif", "seru", "keren"]
KATA_NEGATIV = ["kekecilan", "lama", "kecewa", "mahal", "jelek", "lambat", "rusak", "kurang", "garing"]

# --- FORM INPUT DINAMIS ---
st.subheader(f"📌 Profil Objek: **{profile_name}**")
st.caption(f"URL Profil: [{profile_url}]({profile_url})")

video_data = []

for i in range(num_videos):
    with st.expander(f"🎬 Input Data Video #{i+1}", expanded=(i == 0)):
        col_link, col_label = st.columns([2, 1])
        v_link = col_link.text_input(f"Link Video TikTok #{i+1}:", key=f"link_{i}", value=f"https://www.tiktok.com/@mr.kingthread/video/sample{i+1}")
        v_label = col_label.text_input(f"Topik/Label Video #{i+1}:", key=f"label_{i}", value=f"Konten Tema {i+1}")
        
        v_comments = st.text_area(f"Tempel Komentar Video #{i+1} (pisahkan baris baru):", height=120, key=f"comments_{i}")
        
        video_data.append({
            "index": i + 1,
            "link": v_link,
            "label": v_label,
            "raw_comments": [line.strip() for line in v_comments.split("\n") if line.strip()]
        })

# --- PROSES ANALISIS ---
if st.button("🚀 Jalankan Analisis Komparatif"):
    st.markdown("---")
    st.header("📈 Hasil Analisis Sentimen & Persepsi")
    
    summary_list = []
    tab_names = [f"Video #{v['index']}: {v['label']}" for v in video_data]
    tabs = st.tabs(tab_names)
    
    for idx, tab in enumerate(tabs):
        v = video_data[idx]
        comments = v["raw_comments"]
        
        with tab:
            st.write(f"**Link Video:** [{v['link']}]({v['link']})")
            
            if not comments:
                st.warning("Belum ada komentar yang dimasukkan untuk video ini.")
            else:
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
                
                s_series = pd.Series(sentiments).value_counts(normalize=True) * 100
                pos_pct = round(s_series.get("Positif", 0), 1)
                neu_pct = round(s_series.get("Netral", 0), 1)
                neg_pct = round(s_series.get("Negatif", 0), 1)
                
                summary_list.append({
                    "Video / Konten": f"#{v['index']} - {v['label']}",
                    "Total Komentar": len(comments),
                    "Positif (%)": f"{pos_pct}%",
                    "Netral (%)": f"{neu_pct}%",
                    "Negatif (%)": f"{neg_pct}%"
                })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("##### 1. Distribusi Sentimen")
                    fig1, ax1 = plt.subplots(figsize=(4, 3))
                    sentiment_counts = pd.Series(sentiments).value_counts()
                    ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
                    st.pyplot(fig1)
                    
                with col2:
                    st.write("##### 2. Word Cloud (Asosiasi Kata)")
                    word_freq = Counter(all_words)
                    if word_freq:
                        wordcloud = WordCloud(width=400, height=250, background_color='white').generate_from_frequencies(word_freq)
                        fig2, ax2 = plt.subplots(figsize=(4, 2.5))
                        ax2.imshow(wordcloud, interpolation='bilinear')
                        ax2.axis('off')
                        st.pyplot(fig2)
                        
                st.write("##### 3. Detail Hasil Per Komentar")
                df_detail = pd.DataFrame({"Komentar Netizen": comments, "Klasifikasi Sentimen": sentiments})
                st.dataframe(df_detail, width="stretch")

    if summary_list:
        st.markdown("---")
        st.subheader("📊 Matriks Ringkasan Komparasi Antar Konten")
        df_summary = pd.DataFrame(summary_list)
        st.dataframe(df_summary, width="stretch")
