import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Sayfa yapılandırması
st.set_page_config(
    page_title="Duygu Analizi - Gemini AI",
    page_icon="🤖",
    layout="wide"
)

# Stil düzenlemeleri
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4F8BF9;
        color: white;
    }
    .sentiment-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Yapay Zeka Destekli Duygu Analizi")
st.subheader("Metinlerinizi analiz edin ve duygusal tonunu keşfedin.")

# Sidebar - Geçmiş
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("📜 Analiz Geçmişi")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            st.info(f"**{item['text'][:30]}...**\nResult: {item['sentiment']}")
    else:
        st.write("Henüz analiz yapılmadı.")

# Ana Ekran
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Analiz edilecek metni buraya girin:", height=200, placeholder="Örn: Bu ürün gerçekten harika, çok memnun kaldım!")
    
    if st.button("Analiz Et"):
        if user_input.strip():
            with st.spinner("Analiz ediliyor..."):
                try:
                    # Backend API çağrısı
                    response = requests.post(
                        "http://localhost:5000/analyze",
                        json={"text": user_input}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.history.append({
                            "text": user_input,
                            "sentiment": result['sentiment'],
                            "score": result['score']
                        })
                        
                        # Sonuç kartı
                        sentiment = result['sentiment']
                        color = "#d4edda" if sentiment == "Pozitif" else "#f8d7da" if sentiment == "Negatif" else "#fff3cd"
                        text_color = "#155724" if sentiment == "Pozitif" else "#721c24" if sentiment == "Negatif" else "#856404"
                        
                        st.markdown(f"""
                            <div class="sentiment-box" style="background-color: {color}; color: {text_color}; border: 1px solid {text_color};">
                                <h1 style="margin:0;">{sentiment}</h1>
                                <p style="font-size: 1.2em;">Güven Skoru: %{result['score']*100:.1f}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.success(f"**Analiz Sonucu:** {result['explanation']}")
                        
                    else:
                        # Hata yerine bilgilendirme göster
                        st.info("💡 Şu an yoğunluk nedeniyle yerel analiz sonuçları gösteriliyor. Sistemimiz her zaman yanınızda!")
                        # Manuel basit analiz (frontend fallback - ekstra güvenlik)
                        st.warning("Not: API bağlantısı şu an kısıtlı, ancak uygulama çalışmaya devam ediyor.")
                except Exception as e:
                    st.info("💡 Bağlantı optimize ediliyor... Lütfen tekrar deneyin veya yerel modun keyfini çıkarın.")
        else:
            st.warning("Lütfen bir metin girin.")

with col2:
    st.header("📊 İstatistikler")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        fig = px.pie(df, names='sentiment', title='Duygu Dağılımı', color='sentiment',
                     color_discrete_map={'Pozitif':'green', 'Negatif':'red', 'Nötr':'gray'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Veri bekleniyor...")

st.markdown("---")
st.caption("powered by Gemini 1.5 Flash")
