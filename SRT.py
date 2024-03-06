# Импорты
from tkinter import ttk
from tkinter import Tk
import tkinter as tk
from pathlib import Path
import speech_recognition as sr
from sv_ttk import set_theme
import subprocess
import os
import time

# Код
class VoiceAssistantGUI:
    existing_actions = set()

    def __init__(self):
        self._create_gui()
        self._add_listener()

    def _create_gui(self):
        root = tk.Tk()
        set_theme("dark")
        root.title("Speech Recognition Tools")

        label = ttk.Label(root, text="Билдинг")
        label.pack()

        button = ttk.Button(root, text="Создать голосового ассистента", command=self._on_create_va)
        button.pack()

        label = ttk.Label(root, text="Введите фразу для добавления в код:")
        label.pack()
        self._entry = ttk.Entry(root)
        self._entry.bind("<Return>", self._on_enter_pressed)
        self._entry.pack()


        button = ttk.Button(root, text="Добавить действие", command=self._on_add_action)
        button.pack()
        button = ttk.Button(root, text="Открыть тесты аудио", command=lambda: subprocess.run(["python", "audiotest.py"]))
        button.pack()



        root.mainloop()

    @staticmethod
    def _check_file_exists(filename):
        return Path(filename).is_file()

    def _create_or_update_voice_assistant_script(self, script_content):
        filename = "voice_assistant.py"
        if not self._check_file_exists(filename):
            with open(filename, mode='w+', newline='', encoding='utf-8'):
                pass

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            file.write(script_content)

        _remove_duplicate_elif()

    def _create_or_update_voice_assistant_script2(self, script_content):
        filename = "voice_assistant.py"
        if not self._check_file_exists(filename):
            with open(filename, mode='w+', newline='', encoding='utf-8'):
                pass

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            file.write(script_content)

        _remove_duplicate_elif()

    def _on_create_va(self):
        self._clear_textbox()
        self._create_or_update_voice_assistant_script(_generate_initial_code())
        self._move_actions_to_end()
        self._create_or_update_voice_assistant_script2(_generate_initial_code2())

    def _on_add_action(self):
        action_to_add = self._entry.get().strip()

        if action_to_add and action_to_add.lower() not in self.existing_actions:
            self._create_or_update_voice_assistant_script(_append_action_to_script(action_to_add))
            self._create_or_update_voice_assistant_script2(_append_action_to_script(action_to_add))
            self.existing_actions.add(action_to_add.lower())
            self._entry.delete(0, tk.END)
            self._entry.focus_set()

    def _clear_textbox(self):
        self._entry.delete(0, tk.END)

    def _on_enter_pressed(self, event):
        self._on_add_action()

    def _move_actions_to_end(self):
        with open("voice_assistant.py", mode='r', encoding='utf-8') as file:
            lines = file.readlines()

        actions_to_move = []
        other_actions = []

        for line in lines:
            if "            elif query == '" in line:
                actions_to_move.append(line)
            else:
                other_actions.append(line)

        actions_in_script = "".join(other_actions + actions_to_move)

        with open("voice_assistant.py", mode='w', encoding='utf-8') as file:
            file.write(actions_in_script)
# Первая часть прописываемого кода в файл
def _generate_initial_code():
    initial_code = """
import speech_recognition as sr
import os
import time
import webbrowser

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Слушаю...')
        audio = r.listen(source)

    first_iteration = True

    while True:
        try:
            query = r.recognize_google(audio, language='ru-RU').lower()
            if query == 'выход':
                break

"""
    return initial_code + "\n\n"


def _append_action_to_script(action_to_add):
    actions_in_script = ""
    with open("voice_assistant.py", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines[:-2]:
            actions_in_script += line
            if "            elif query == '" in line:
                if action_to_add.lower() != line[len("elif query == '"): len(line)-1].lower():
                    actions_in_script 

        actions_in_script += f"""\
            elif query == '{action_to_add}':
    
"""
    return actions_in_script

def _remove_duplicate_elif():
    with open("voice_assistant.py", mode='r', encoding='utf-8') as file:
        lines = file.readlines()

    unique_lines = []
    seen_elifs = set()

    for line in lines:
        if "elif query == '" in line:
            condition = line[line.index("elif query == '"):]
            if condition not in seen_elifs:
                unique_lines.append(line)
                seen_elifs.add(condition)
        else:
            unique_lines.append(line)

    with open("voice_assistant.py", mode='w', encoding='utf-8') as file:
        file.writelines(unique_lines)
# Вторая часть прописываемого кода в файл
def _generate_initial_code2():
    initial_code2 = """            else:
                continue
                
            first_iteration = False
            
            time.sleep(1)  
            
        except sr.UnknownValueError:
            continue
        
        if first_iteration:
            continue
        else:
            with sr.Microphone() as source:
                audio = r.listen(source)

if __name__ == "__main__":
    main()
"""
    return initial_code2 + "\n\n"
VoiceAssistantGUI()
