import threading
from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# --- YAPILANDIRMA ---
app = Flask(__name__)
API_KEY = "AIzaSyCkXF24v2u64WP_STvRDwQjj5AR0btkgjg" # Senin anahtarın
genai.configure(api_key=API_KEY)

# Bulutta geçmişi tutmak için
chat_history = ["Sistem çekirdeği bulutta hazır, Mikail efendim."]

# Model ayarları
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def mobil():
    return """
    <html><head>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>JARVIS CLOUD - MIKAIL</title>
    <style>
        body { background: #000; color: #00e5ff; font-family: 'Consolas', monospace; padding: 10px; text-align: center; }
        .header { font-size: 20px; text-shadow: 0 0 10px #00e5ff; margin-bottom: 20px; }
        .chat-box { background: #0a0a0a; border: 2px solid #00e5ff; padding: 15px; border-radius: 10px; height: 60vh; overflow-y: auto; font-size: 16px; margin-bottom: 10px; text-align: left; white-space: pre-wrap; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #00e5ff; color: #fff; border-radius: 10px; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 15px; background: #00e5ff; color: #000; border: none; font-weight: bold; margin-top: 10px; border-radius: 10px; cursor: pointer; }
    </style>
    </head><body>
        <div class="header">STARK INDUSTRIES - CLOUD HUB v73</div>
        <div id='display' class='chat-box'>Sistem Bekleniyor...</div>
        <input type='text' id='cmd' placeholder='Emriniz, Mikail?' onkeypress="if(event.keyCode==13) send()">
        <button onclick="send()">GÖNDER</button>
        <script>
            function send(){
                let v = document.getElementById('cmd').value;
                if(!v) return;
                fetch('/c?k=' + encodeURIComponent(v));
                document.getElementById('cmd').value = '';
            }
            function update(){
                fetch('/get_history').then(r => r.json()).then(data => {
                    document.getElementById('display').innerText = data.history.join('\\n\\n');
                    document.getElementById('display').scrollTop = document.getElementById('display').scrollHeight;
                });
            }
            setInterval(update, 2000);
        </script>
    </body></html>
    """

@app.route('/c')
def cmd():
    k = request.args.get('k')
    def ai_islem(komut):
        global chat_history
        chat_history.append(f"> Mikail: {komut}")
        try:
            res = model.generate_content(f"Sen Jarvis'sin. Mikail'e cevap ver. Soru: {komut}")
            chat_history.append(f"JARVIS: {res.text}")
        except Exception as e:
            chat_history.append(f"JARVIS HATA: {str(e)}")
    
    threading.Thread(target=ai_islem, args=(k,)).start()
    return "OK"

@app.route('/get_history')
def get_history():
    return jsonify({"history": chat_history})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
