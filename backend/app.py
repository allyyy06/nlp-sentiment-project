import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini API Yapılandırması
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Eğer .env'de yoksa direkt streamlit_app.py'dan veya sistemden gelebilir
    # Ama biz .env'den okumasını bekliyoruz.
    pass

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "Metin girilmedi"}), 400
        
        prompt = f"""
        Aşağıdaki metnin duygu analizini yap. 
        Sonucu mutlaka şu JSON formatında döndür:
        {{
            "sentiment": "Pozitif" | "Negatif" | "Nötr",
            "score": 0.0-1.0 arası güven skoru,
            "explanation": "Kısa Türkçe açıklama"
        }}
        
        Metin: {text}
        """
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # JSON temizleme (Gemini bazen markdown içinde döndürür)
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        return result_text, 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        error_msg = str(e)
        
        # Local Fallback (API Kotası dolduğunda veya hata aldığında çalışır)
        positive_words = ['iyi', 'güzel', 'harika', 'muhteşem', 'memnun', 'başarılı', 'seviyorum', 'teşekkür']
        negative_words = ['kötü', 'berbat', 'rezelat', 'memnun değilim', 'hayal kırıklığı', 'çalışmıyor', 'hata']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment, score, explanation = "Pozitif", 0.7, "Yerel analiz: Pozitif anahtar kelimeler tespit edildi."
        elif neg_count > pos_count:
            sentiment, score, explanation = "Negatif", 0.7, "Yerel analiz: Negatif anahtar kelimeler tespit edildi."
        else:
            sentiment, score, explanation = "Nötr", 0.5, "Yerel analiz: Belirgin bir duygu tonu saptanamadı."

        # Eğer hata 429 ise veya başka bir API hatasıysa bu fallback'i döndür
        return jsonify({
            "sentiment": sentiment,
            "score": score,
            "explanation": f"{explanation} (Not: Gemini API kotası dolduğu için yerel model kullanıldı.)",
            "is_fallback": True
        }), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)