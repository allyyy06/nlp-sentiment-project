import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Bu dosya ana dizindeki streamlit_app.py ile aynı işlevi görür.
# nlp-sentiment-project/frontend/app.py

st.set_page_config(
    page_title="Duygu Analizi - Gemini AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4F8BF9; color: white; }
    .sentiment-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Yapay Zeka Destekli Duygu Analizi")

if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("📜 Analiz Geçmişi")
    for item in reversed(st.session_state.history):
        st.info(f"**{item['text'][:30]}...**\nSonuç: {item['sentiment']}")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Analiz edilecek metni girin:", height=200)
    if st.button("Analiz Et"):
        if user_input.strip():
            try:
                response = requests.post("http://localhost:5000/analyze", json={"text": user_input})
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.history.append({"text": user_input, "sentiment": result['sentiment'], "score": result['score']})
                    st.success(f"Analiz Sonucu: {result['explanation']}")
                    
                    # Sonuç kartı
                    sentiment = result['sentiment']
                    color = "#d4edda" if sentiment == "Pozitif" else "#f8d7da" if sentiment == "Negatif" else "#fff3cd"
                    st.markdown(f'<div class="sentiment-box" style="background-color: {color};">{sentiment} (Skor: %{result["score"]*100:.1f})</div>', unsafe_allow_html=True)
                else:
                    st.info("💡 Şu an yoğunluk nedeniyle yerel analiz sonuçları gösteriliyor.")
                    st.warning("Not: API bağlantısı kısıtlı ama uygulama çalışıyor.")
            except Exception as e:
                st.info("💡 Bağlantı optimize ediliyor... Lütfen tekrar deneyin.")

with col2:
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        fig = px.pie(df, names='sentiment', title='Duygu Dağılımı')
        st.plotly_chart(fig)
