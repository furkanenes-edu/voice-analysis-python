import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
def open_file():
    filename = fd.askopenfilename(title="Ses Dosyası Seç", filetypes=[("Ses Dosyaları", "*.wav *.mp3 *.ogg"), ("Tüm Dosyalar", "*.*")])

    if filename:
        lbl_dosya_yolu.config(text=f"Seçilen Dosya: {filename}")
        lbl_dosya_yolu.pack(pady=10)
    else:
        messagebox.showinfo("Bilgi", "Hiçbir dosya seçilmedi.")

#UYGULAMA EKRANI
window = tk.Tk()
window.title("Ses Analiz Programı")
window.minsize(width=400, height=200)
window.config(pady=40,padx=40)

lbl_ses_yukle = tk.Label(text="Lütfen Ses Yükleyiniz")
lbl_ses_yukle.pack()

btn_ses_yukle = tk.Button(text="Ses Yükle", command=open_file)
btn_ses_yukle.pack()

lbl_dosya_yolu = tk.Label(window, text="", wraplength=300)

window.mainloop()