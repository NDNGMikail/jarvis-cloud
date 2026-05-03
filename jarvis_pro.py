import customtkinter as ctk
import threading
from flask import Flask, request, jsonify
import google.generativeai as genai

# --- YAPILANDIRMA ---
app = Flask(__name__)
API_KEY = "AIzaSyCkXF24v2u64WP_STvRDwQjj5AR0btkgjg"
genai.configure(api_key=API_KEY)

chat_history = ["Sistem çekirdeği hazır, Mikail efendim."]

try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = next((m for m in available_models if 'flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
except:
    model = genai.GenerativeModel('gemini-pro')

class JarvisHybridSync(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS - HYBRID SYNC v73")
        self.geometry("900x950")
        ctk.set_appearance_mode("dark")
        
        self.label = ctk.CTkLabel(self, text="STARK INDUSTRIES - MASTER HUB", text_color="#00e5ff", font=("Orbitron", 24, "bold"))
        self.label.pack(pady=20)

        # PC Ekranı
        self.textbox = ctk.CTkTextbox(self, width=850, height=650, fg_color="#050505", border_color="#00e5ff", border_width=2, text_color="#00e5ff", font=("Consolas", 14))
        self.textbox.pack(pady=10)

        # PC Giriş Kutusu (Geri geldi!)
        self.pc_entry = ctk.CTkEntry(self, placeholder_text="Buradan da yazabilirsiniz Mikail efendim...", width=800, height=45, border_color="#00e5ff")
        self.pc_entry.pack(pady=10)
        self.pc_entry.bind("<Return>", lambda e: self.pc_islem())

        threading.Thread(target=self.run_flask, daemon=True).start()

    def yazdir(self, mesaj):
        self.textbox.insert("end", f"\n[JARVIS]: {mesaj}\n")
        self.textbox.see("end")

    def pc_islem(self):
        komut = self.pc_entry.get()
        self.pc_entry.delete(0, 'end')
        self.textbox.insert("end", f"\n>>> PC TALİMAT: {komut}\n")
        threading.Thread(target=self.ai_islem, args=(komut,), daemon=True).start()

    def ai_islem(self, komut):
        global chat_history
        chat_history.append(f"> Mikail: {komut}")
        try:
            res = model.generate_content(f"Sen Jarvis'is. Mikail'e cevap ver. Soru: {komut}")
            cevap = res.text
            chat_history.append(f"JARVIS: {cevap}")
            self.yazdir(cevap)
        except Exception as e:
            chat_history.append(f"JARVIS: Hata: {e}")
            self.yazdir(str(e))

    def run_flask(self):
        @app.route('/')
        def mobil():
            return """
            <html><head>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <style>
                body { background: #000; color: #00e5ff; font-family: monospace; padding: 10px; }
                .chat-box { background: #0a0a0a; border: 2px solid #00e5ff; padding: 15px; border-radius: 10px; height: 65vh; overflow-y: scroll; font-size: 16px; margin-bottom: 10px; }
                input { width: 100%; padding: 15px; background: #111; border: 1px solid #00e5ff; color: #fff; border-radius: 10px; box-sizing: border-box; }
                button { width: 100%; padding: 15px; background: #00e5ff; color: #000; border: none; font-weight: bold; margin-top: 10px; border-radius: 10px; }
            </style>
            </head><body>
                <div id='display' class='chat-box'>Sistem Bekleniyor...</div>
                <input type='text' id='cmd' placeholder='Emriniz?'>
                <button onclick="send()">GÖNDER</button>
                <script>
                    function send(){
                        let v = document.getElementById('cmd').value;
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
            threading.Thread(target=self.ai_islem, args=(k,)).start()
            return "OK"
        @app.route('/get_history')
        def get_history():
            return jsonify({"history": chat_history})
        app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    JarvisHybridSync().mainloop()