import os
import threading
from flask import Flask, request, jsonify
import google.generativeai as genai

# --- KRİTİK AYAR ---
IS_CLOUD = "RENDER" in os.environ

if not IS_CLOUD:
    try:
        import customtkinter as ctk
    except:
        pass

# --- YAPILANDIRMA ---
app = Flask(__name__)

# YENİ ANAHTARIN BURADA
API_KEY = "AIzaSyBPAD0_-S1de6OW2HpU1Uv8FszcLawws38" 
genai.configure(api_key=API_KEY)

chat_history = ["Sistem çekirdeği hazır, Mikail efendim."]

# --- MODEL SEÇİCİ ---
def get_working_model():
    try:
        # Hesabındaki modelleri listele
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Öncelik 1.5-flash, yoksa mevcut olan ilk model
        target = next((m for m in available_models if 'flash' in m), available_models[0])
        return genai.GenerativeModel(target)
    except Exception as e:
        # Eğer liste çekilemezse varsayılanı zorla
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_working_model()

def ai_islem_logic(komut, gui_callback=None):
    global chat_history
    chat_history.append(f"> Mikail: {komut}")
    try:
        # Jarvis kişiliği ile cevap üret
        res = model.generate_content(f"Sen Jarvis'sin. Mikail'e kısa ve zeki bir cevap ver: {komut}")
        cevap = res.text
        chat_history.append(f"JARVIS: {cevap}")
        if gui_callback: gui_callback(cevap)
    except Exception as e:
        hata_str = str(e)
        # Hata yönetimi
        if "403" in hata_str:
            cevap = "Efendim, bu API anahtarı da engellenmiş görünüyor. Güvenli yöntemle (ENV) girmeliyiz."
        elif "429" in hata_str:
            cevap = "Efendim, çok hızlı gidiyoruz. Kota doldu, biraz bekleyelim."
        else:
            cevap = f"Sistem hatası: {hata_str}"
        
        chat_history.append(f"JARVIS: {cevap}")
        if gui_callback: gui_callback(cevap)

# --- PC ARAYÜZÜ (CustomTkinter) ---
if not IS_CLOUD:
    class JarvisHybridSync(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("JARVIS - MASTER SYNC")
            self.geometry("900x950")
            ctk.set_appearance_mode("dark")
            
            self.textbox = ctk.CTkTextbox(self, width=850, height=750, fg_color="#050505", border_color="#00e5ff", border_width=2, text_color="#00e5ff", font=("Consolas", 14))
            self.textbox.pack(pady=20)

            self.pc_entry = ctk.CTkEntry(self, placeholder_text="Sisteme komut verin...", width=800, height=45, border_color="#00e5ff")
            self.pc_entry.pack(pady=10)
            self.pc_entry.bind("<Return>", lambda e: self.pc_islem())

            threading.Thread(target=run_server, daemon=True).start()

        def yazdir(self, mesaj):
            self.textbox.insert("end", f"\n[JARVIS]: {mesaj}\n")
            self.textbox.see("end")

        def pc_islem(self):
            k = self.pc_entry.get()
            if not k: return
            self.pc_entry.delete(0, 'end')
            self.textbox.insert("end", f"\n>>> MIKAIL: {k}\n")
            threading.Thread(target=ai_islem_logic, args=(k, self.yazdir), daemon=True).start()

# --- WEB PANEL ---
@app.route('/')
def index():
    return """
    <html><head><title>JARVIS HUB</title>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <style>
        body { background: #000; color: #00e5ff; font-family: 'Courier New', monospace; padding: 20px; }
        .chat { background: #050505; border: 2px solid #00e5ff; height: 70vh; overflow-y: auto; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #00e5ff; color: #fff; border-radius: 5px; }
    </style></head><body>
        <h2>JARVIS CLOUD INTERFACE</h2>
        <div id='box' class='chat'>Yükleniyor...</div>
        <input type='text' id='inp' onkeydown="if(event.key=='Enter')send()" placeholder='Komut gönder...'>
        <script>
            function send(){
                let i = document.getElementById('inp');
                fetch('/c?k=' + encodeURIComponent(i.value));
                i.value = '';
            }
            setInterval(() => {
                fetch('/get_history').then(r => r.json()).then(d => {
                    document.getElementById('box').innerText = d.history.join('\\n\\n');
                    document.getElementById('box').scrollTop = document.getElementById('box').scrollHeight;
                });
            }, 1000);
        </script>
    </body></html>
    """

@app.route('/c')
def cmd():
    k = request.args.get('k')
    if k: threading.Thread(target=ai_islem_logic, args=(k,)).start()
    return "OK"

@app.route('/get_history')
def get_history():
    return jsonify({"history": chat_history})

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    if IS_CLOUD:
        run_server()
    else:
        JarvisHybridSync().mainloop()
