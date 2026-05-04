from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Jarvis Sistemi Aktif, Mikail! Bulut üzerinden çalışıyorum."

def jarvis_logic():
    print("Jarvis arka planda çalışmaya başladı...")
    # Buraya daha sonra AI komutlarını ekleyeceğiz.
    while True:
        pass

if __name__ == "__main__":
    # Jarvis'i ayrı bir kolda (thread) çalıştırıyoruz
    t = threading.Thread(target=jarvis_logic)
    t.daemon = True
    t.start()
    
    # Render'ın beklediği web sunucusunu başlatıyoruz
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
