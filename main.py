import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import wave
from pydub import AudioSegment
import librosa
import librosa.display

def open_file():
    filename = fd.askopenfilename(title="Ses Dosyası Seç", filetypes=[("Ses Dosyaları", "*.wav *.mp3 *.ogg"), ("Tüm Dosyalar", "*.*")])

    if filename:
        lbl_dosya_yolu.config(text=f"Seçilen Dosya: {filename}", pady=10)
        lbl_dosya_yolu.pack()
        global current_file
        current_file = filename
        btn_histogram.config(state=tk.NORMAL)
        btn_histogram.pack()
    else:
        messagebox.showinfo("Bilgi", "Hiçbir dosya seçilmedi.")

def convert_to_wav(filepath):
    try:
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        messagebox.showerror("Hata", f"Ses dosyasını dönüştüremedik: {e}")
        return None

def visualize_audio(filepath):
    if not filepath.endswith(".wav"):
        filepath = convert_to_wav(filepath)
        if not filepath:
            return

    try:
        with wave.open(filepath, "rb") as wav_file:
            #ses parametreleri alır
            n_frames = wav_file.getnframes()
            framerate = wav_file.getframerate()
            audio_frames = wav_file.readframes(n_frames)

            #numpy dizisine çevirir
            audio_data = np.frombuffer(audio_frames, dtype=np.int16)
            time = np.linspace(0, len(audio_data) / framerate, num=len(audio_data))

            #Dalga formunu çizer
            plt.figure(figsize=(10,4))
            plt.subplot(2,1,1)
            plt.plot(time, audio_data, color="blue")
            plt.title("Ses Dalga Formu")
            plt.xlabel("Zaman (s)")
            plt.ylabel("Genlik")
            plt.grid()

            # Mel Spektrogramını hesaplar
            y, sr = librosa.load(filepath)
            mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
            mel_log = librosa.power_to_db(mel_spectrogram, ref=np.max)

            #Mel Spektrogramını çizer
            plt.subplot(2,1,2)
            librosa.display.specshow(mel_log, x_axis="time", y_axis="mel", sr=sr)
            plt.title("Mel Spektrogramı")
            plt.colorbar(format="%+2.0f dB")
            plt.tight_layout()
            plt.show()

    except Exception as e:
        messagebox.showerror("Hata", f"Ses dosyasını işleyemedik: {e}")

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

btn_histogram = tk.Button(text="Histogram Görüntüle", command=lambda: visualize_audio(current_file), state=tk.DISABLED)

current_file = None
window.mainloop()