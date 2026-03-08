# NLP Duygu Analizi Projesi (Gemini AI)

Bu proje, Google Gemini 1.5 Flash modelini kullanarak metinlerin duygu analizini (Pozitif, Negatif, Nötr) gerçekleştiren bir full-stack web uygulamasıdır.

## 🚀 Özellikler
- **Flask Backend:** Gemini API ile entegre RESTful API.
- **Streamlit Frontend:** Modern ve etkileşimli kullanıcı arayüzü.
- **Duygu Dağılımı:** Plotly ile görselleştirilmiş analiz geçmişi.
- **Detaylı Açıklama:** Yapay zeka tarafından sağlanan duygu gerekçesi.

## 🛠️ Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/nlp-sentiment-project.git
   cd nlp-sentiment-project
   ```

2. `.env` dosyasını oluşturun ve API anahtarınızı ekleyin:
   ```env
   GEMINI_API_KEY=Sizin_API_Anahtariniz
   ```

3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```

## 🏃 Uygulamayı Çalıştırma

1. **Backend'i Başlatın:**
   ```bash
   cd backend
   python app.py
   ```

2. **Frontend'i Başlatın:**
   (Yeni bir terminalde)
   ```bash
   streamlit run streamlit_app.py
   ```

Uygulama varsayılan olarak `http://localhost:8501` adresinde çalışacaktır.
