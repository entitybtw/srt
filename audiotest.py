from tkinter import ttk
from tkinter import Tk
import tkinter as tk
import webbrowser
import subprocess
import speech_recognition as sr
from sv_ttk import set_theme

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Устанавливаем темную цветовую схему
        set_theme("dark")
        
        self.languages = {"английский": "en_EN", "испанский": "es_ES", "французский": "fr_FR", "немецкий": "de_DE", "русский": "ru_RU", "итальянский": "it_IT", "китайский": "zh_CN", "японский": "ja_JP"}  # Замените на свои языки и коды

        self.label = ttk.Label(self.master, text="Выберите язык для распозnавания речи:")
        self.label.pack()

        self.selected_lang = tk.StringVar()
        for lang in self.languages.keys():
            ttk.Radiobutton(self.master, text=lang, variable=self.selected_lang, value=lang).pack()

        self.confirm_button = ttk.Button(self.master, text="Подтвердить", command=self.confirm)
        self.confirm_button.pack()

    def confirm(self):
        selected_lang = self.selected_lang.get()
        selected_code = self.languages[selected_lang]
        self.master.destroy()
        self.start_recognition(selected_code)

    def start_recognition(self, selected_lang):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Говорите:")
            audio = r.listen(source)

        try:
            print(f"Вы сказали: {r.recognize_google(audio_data=audio, language=selected_lang).lower()}")
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Не удалось обработать запрос: {e}")

    def setup_widgets(self):
        pass  

if __name__ == "__main__":
    root = Tk()
    my_gui = App(root)
    root.title('Speech recognition tools')
    root.geometry("500x300+100+100")
    root.mainloop()
