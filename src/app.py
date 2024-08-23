import tkinter as tk
from tkinter import ttk
from views.fileMenu import FileMenu
from views.mainMenu import MainMenu
from views.chopMenu import ChopMenu
from views.kanjiView import KanjiView
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), 'kanjivg'))
#import kvg_lookup
import requests_cache
sys.stdout.reconfigure(encoding='utf-8')


class App:
    def __init__(self, window):
        self.window = window
        self.window.tk.call("source", "Forest-ttk-theme/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")
        self.window.geometry("1400x700")
        self.current_view = None
        requests_cache.install_cache("kanjicache", expire_after=7200, backend="memory")

    def start(self):
        self.current_view = MainMenu(self.window, 600, 1200, 3, self.handle_file_menu, True)
        self.current_view.init_commands()
        self.current_view.initiate_menu()

    def handle_file_menu(self, files):
        self.current_view.destroy()
        self.current_view = FileMenu(self.window, 600, 1200, len(files), self.handle_file_chop, False, files=files)
        self.current_view.initiate_menu()

    def handle_file_chop(self, files, chosen_files):
        self.current_view.destroy()
        self.current_view = ChopMenu(self.window, files, chosen_files, self.handle_kanji_view)
        self.current_view.initiate_menu()
        
    def handle_kanji_view(self, chopped_files):
        self.current_view.destroy()
        self.current_view = KanjiView(self.window, chopped_files)
        self.current_view.initiate_view()    

if __name__ == "__main__":
    window = tk.Tk()
    shuffler = App(window)
    shuffler.start()
    window.mainloop()