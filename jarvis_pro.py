import os
import threading
from flask import Flask, request, jsonify
import google.generativeai as genai

# --- KRİTİK AYAR: Render (Bulut) mu yoksa PC mi? ---
IS_CLOUD = "RENDER" in os.environ

if not IS_CLOUD:
    try:
        import customtkinter as ctk
    except ImportError:
        print("PC modundasınız ama customtkinter yüklü değil!")

# --- YAPILANDIRMA ---
app = Flask(__name__)
API_KEY = "AIzaSyCkXF24v2u64WP_STvRDwQjj5AR0btkgjg" # Mikail'in anahtarı
genai.configure(api_key=API_KEY)

chat_history = ["Sistem çekirdeği hazır, Mikail efendim."]

# 404 Hatasını Çözmek İçin En Garanti Model Seçimi
def get_model():
    try:
        # En stabil model ismi
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-pro')

model = get_model()

# --- AI İŞLEM FONKSİYONU ---
def ai_islem_logic(komut, gui_callback=None):
    global chat_history
    chat_history.append(f"> Mikail: {komut}")
    try:
        # Prompt'u basitleştirdik ki hata payı kalmasın
        res = model.generate_content(f"Sen Jarvis'sin. Mikail'e kısa ve öz cevap ver. Soru: {komut}")
        cevap = res.text
        chat_history.append(f"JARVIS: {cevap}")
        if gui_callback:
            gui_callback(cevap)
    except Exception as e:
        hata_mesaji = f"Hata oluştu: {str(e)}"
        chat_history.append(f"JARVIS: {hata_mesaji}")
        if gui_callback:
            gui_callback(hata_mesaji)

# --- PC ARAYÜZ SINIFI (Sadece PC'de çalışır) ---
if not IS_CLOUD:
    class JarvisHybridSync(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("JARVIS - HYBRID SYNC v73")
            self.geometry("900x950")
            ctk.set_appearance_mode("dark")
            
            self.label = ctk.CTkLabel(self, text="STARK INDUSTRIES - MASTER HUB", text_color="#00e5ff", font=("Orbitron", 24, "bold"))
            self.label.pack(pady=20)

            self.textbox = ctk.CTkTextbox(self, width=850, height=650, fg_color="#050505", border_color="#00e5ff", border_width=2, text_color="#00e5ff", font=("Consolas", 14))
            self.textbox.pack(pady=10)

            self.pc_entry = ctk.CTkEntry(self, placeholder_text="Emriniz nedir Mikail efendim?", width=800, height=45, border_color="#00e5ff")
            self.pc_entry.pack(pady=10)
            self.pc_entry.bind("<Return>", lambda e: self.pc_islem())

            threading.Thread(target=self.run_flask, daemon=True).start()

        def yazdir(self, mesaj):
            self.textbox.insert("end", f"\n[JARVIS]: {mesaj}\n")
            self.textbox.see("end")

        def pc_islem(self):
            komut = self.pc_entry.get()
            if not komut: return
            self.pc_entry.delete(0, 'end')
            self.textbox.insert("end", f"\n>>> PC TALİMAT: {komut}\n")
            threading.Thread(target=ai_islem_logic, args=(komut, self.yazdir), daemon=True).start()

        def run_flask(self):
            run_server()

# --- FLASK SUNUCU AYARLARI ---
@app.route('/')
def mobil():
    return """
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <style>
        body { background: #000; color: #00e5ff; font-family: 'Consolas', monospace; padding: 10px; }
        .chat-box { background: #0a0a0a; border: 2px solid #00e5ff; padding: 15px; border-radius: 10px; height: 70vh; overflow-y: auto; font-size: 16px; margin-bottom: 10px; white-space: pre-wrap; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #00e5ff; color: #fff; border-radius: 10px; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 15px; background: #00e5ff; color: #000; border: none; font-weight: bold; margin-top: 10px; border-radius: 10px; width: 100%; cursor: pointer; }
    </style></head><body>
        <h2 style='text-align:center'>JARVIS CLOUD HUB</h2>
        <div id='display' class='chat-box'>Sistem Bekleniyor...</div>
        <input type='text' id='cmd' placeholder='Buraya yazın...'>
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
    if k:
        threading.Thread(target=ai_islem_logic, args=(k,)).start()
    return "OK"

@app.route('/get_history')
def get_history():
    return jsonify({"history": chat_history})

def run_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- ANA ÇALIŞTIRMA ---
if __name__ == "__main__":
    if IS_CLOUD:
        run_server()
    else:
        JarvisHybridSync().mainloop()
