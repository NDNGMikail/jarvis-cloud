import customtkinter as ctk
import os

# Render gibi ekranı olmayan (headless) sunucularda hata vermemesi için
if os.environ.get('DISPLAY','') == '':
    print('Ekran bulunamadı, bulut modu aktif.')
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

def baslat():
    # Pencere ayarları
    app = ctk.CTk()
    app.geometry("400x240")
    app.title("Jarvis Cloud")

    # Arayüz elemanları - İsmin burada güncellendi Mikail!
    label = ctk.CTkLabel(app, text="Jarvis Bulut Sistemine Hoş Geldin, Mikail!", font=("Arial", 16))
    label.pack(pady=20)

    btn = ctk.CTkButton(app, text="Sistemi Kontrol Et", command=lambda: print("Sistem Aktif!"))
    btn.pack(pady=10)

    print("Jarvis başarıyla başlatıldı...")
    app.mainloop()

if __name__ == "__main__":
    baslat()
