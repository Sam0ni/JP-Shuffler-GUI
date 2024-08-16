import tkinter as tk
import kanjishuffle
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'kanjivg'))
#import kvg_lookup
from PIL import Image, ImageTk, ImageSequence
from io import BytesIO
import requests
import requests_cache
sys.stdout.reconfigure(encoding='utf-8')


class App:
    def __init__(self, window):
        self.window = window
        self.current_view = None
        requests_cache.install_cache("kanjicache", expire_after=7200, backend="memory")

    def start(self):
        self.current_view = ShufflerMenu(self.window, 600, 1200, 3, self.handle_file_menu, True)
        self.current_view.commands = {0: self.current_view.kanji_command, 1: lambda: print("punajuur"), 2: lambda: print("kurpitsasalaatti")}
        self.current_view.initiate_menu()

    def handle_file_menu(self, files):
        self.current_view.destroy()
        self.current_view = ShufflerMenu(self.window, 600, 1200, len(files), self.handle_file_chop, False, files)
        comms = [lambda c=c: self.current_view.select_kanji_file(c) for c in files]
        self.current_view.commands = comms
        self.current_view.initiate_menu()

    def handle_file_chop(self, files, chosen_files):
        self.current_view.destroy()
        self.current_view = ChopMenu(self.window, files, chosen_files, self.handle_kanji_view)
        self.current_view.initiate_menu()
        
    def handle_kanji_view(self, chopped_files):
        self.current_view.destroy()
        self.current_view = KanjiView(self.window, chopped_files)
        self.current_view.initiate_view()    

class ShufflerMenu:
    def __init__(self, window, height, width, botans, handler, horizontally, commands=None, files=None):
        self.widgets = []
        self.frames = []
        self.window = window
        self.files = files
        self.handler = handler
        self.horizontally = horizontally
        self.height = height
        self.width = width
        self.botans = botans
        self.commands = commands

    def divide_screen(self, gauge, by, function):
        if gauge % by != 0:
            raise Exception("Not divisible width")
        one_gauge = gauge // by
        for i in range(by):
            function(i, weight=1, minsize=one_gauge)
    
    def create_buttons(self, number_of_buttons):
        for i in range(number_of_buttons):
            freimi = tk.Frame(relief=tk.SUNKEN, borderwidth=10)
            botan = tk.Button(text="hellou tere", width=50, height=10, bg="blue", fg="red", master=freimi, command=self.commands[i])
            if self.horizontally:
                freimi.grid(row=0, column=i, padx=10)
            else:
                freimi.grid(row=i, column=0, pady=10)
            botan.pack()
            self.widgets.append(botan)
            self.frames.append(freimi)
    
    def initiate_menu(self):
        if self.horizontally:
            self.divide_screen(self.height, 1, self.window.rowconfigure)
            self.divide_screen(self.width, self.botans, self.window.columnconfigure)
        else:
            self.divide_screen(self.height, self.botans, self.window.rowconfigure)
            self.divide_screen(self.width, 1, self.window.columnconfigure)
        self.create_buttons(self.botans)

    def kanji_command(self):
        self.files = kanjishuffle.get_files("kanjit", lambda fail: any(x in fail for x in ["_merkit", "_on", "_kun"]))
        self.handler(self.files)

    def select_kanji_file(self, file):
        chosen_file = file
        no_file_extension = chosen_file[0:-4]
        kanjis = no_file_extension + "_merkit.txt"
        kun = no_file_extension + "_kun.txt"
        on = no_file_extension + "_on.txt"
        yomi, kanjis, kun, on = kanjishuffle.get_all_lists([chosen_file, kanjis, on, kun], "kanjit")
        self.handler(chosen_file, [yomi, kanjis, kun, on])

    def destroy(self):
        for i in self.widgets:
            i.destroy()
        for i in self.frames:
            i.destroy()
        for i in range(self.window.grid_size()[1]):
            self.window.grid_rowconfigure(i, weight=0, minsize=0)
        for i in range(self.window.grid_size()[0]):
            self.window.grid_columnconfigure(i, weight=0, minsize=0)

class ChopMenu:
    def __init__(self, window, files, chosen_file, handler):
        self.window = window
        self.files = files
        self.chosen_file = chosen_file
        self.widgets = []
        self.frames = []
        self.handler = handler
        self.where = 1
        self.to = len(chosen_file[0])
        self.where_label = tk.Label()
        self.to_label = tk.Label()
        self.commands = {0: ((lambda: self.handle_where_change(1)), (lambda: self.handle_where_change(-1))), 2: ((lambda: self.handle_to_change(1)), (lambda: self.handle_to_change(-1))), 1: lambda: self.handle_submit()}

    def divide_screen(self, gauge, by, function):
        if gauge % by != 0:
            raise Exception("Not divisible width")
        one_gauge = gauge // by
        for i in range(by):
            function(i, weight=1, minsize=one_gauge)
    
    def initiate_menu(self):
        self.divide_screen(750, 3, self.window.rowconfigure)
        self.window.rowconfigure(1, weight=1, minsize=100)
        self.divide_screen(1200, 3, self.window.columnconfigure)
        for i in (0, 2):
            freimi = tk.Frame(relief=tk.SUNKEN, borderwidth=10)
            freimi2 = tk.Frame(relief=tk.SUNKEN, borderwidth=10)
            botan = tk.Button(text="hellou tere", width=50, height=10, bg="blue", fg="red", master=freimi, command=self.commands[i][0])
            botan2 = tk.Button(text="hellou tere", width=50, height=10, bg="blue", fg="red", master=freimi2, command=self.commands[i][1])
            freimi.grid(row=0, column=i, pady=10)
            freimi2.grid(row=2, column=i, pady=10)
            botan.grid(row=0, column=i, sticky="s")
            botan2.grid(row=2, column=i, sticky="n")
            self.widgets.append(botan)
            self.widgets.append(botan2)
            self.frames.append(freimi)
            self.frames.append(freimi2)
        self.where_label = tk.Label(text=f"Mistä: {self.where}", font=("Arial", 25))
        self.to_label = tk.Label(text=f"Mihin: {self.to}", font=("Arial", 25))
        self.where_label.grid(row=1, column=0)
        self.to_label.grid(row=1, column=2)
        submitFrame = tk.Frame(relief=tk.GROOVE, borderwidth=10)
        submitFrame.grid(row=1, column=1, pady=10)
        submitBotan = tk.Button(text="submit", width=50, height=10, bg="red", fg="white", master=submitFrame, command=self.commands[1])
        submitBotan.pack()
        self.widgets.append(submitBotan)
        self.frames.append(submitFrame)

    def handle_where_change(self, by):
        if (by < 0 and self.where > 1) or (by > 0 and self.where < self.to):
            self.where += by
        elif (by > 0 and self.to == self.where):
            self.where = 1
        elif (by < 0 and self.where == 1):
            self.where = 0 + self.to
        self.where_label["text"] = f"Mistä: {self.where}"

    def handle_to_change(self, by):
        if (by < 0 and self.to > self.where) or (by > 0 and self.to < len(self.chosen_file[0])):
            self.to += by
        elif (by < 0 and self.to == self.where):
            self.to = len(self.chosen_file[0])
        elif (by > 0 and self.to == len(self.chosen_file[0])):
            self.to = 0 + self.where
        self.to_label["text"] = f"Mihin: {self.to}"

    def handle_submit(self):
        choppedFiles = kanjishuffle.chop_and_shuffle_lists(self.chosen_file, self.where, self.to)
        self.handler(choppedFiles)

    def destroy(self):
        for i in self.widgets:
            i.destroy()
        for i in self.frames:
            i.destroy()
        self.to_label.destroy()
        self.where_label.destroy()
        for i in range(self.window.grid_size()[1]):
            self.window.grid_rowconfigure(i, weight=0, minsize=0)
        for i in range(self.window.grid_size()[0]):
            self.window.grid_columnconfigure(i, weight=0, minsize=0)

class KanjiView:
    def __init__(self, window, chosen_files):
        self.window = window
        self.files = chosen_files
        self.current = 0
        self.frames, self.widgets = self.set_up_frames_and_labels()
        self.anim_is_running = None
        self.bind_keys()

    def set_up_frames_and_labels(self):
        cur_kanji_frame = tk.Frame(borderwidth=2, background="black")
        cur_kun_frame = tk.Frame(borderwidth=2, background="black")
        cur_on_frame = tk.Frame(borderwidth=2, background="black")
        cur_gif_frame = tk.Frame(borderwidth=2, background="black")
        cur_kanji_frame.grid(row=0, column=1)
        cur_kun_frame.grid(row=0, column=0)
        cur_on_frame.grid(row=0, column=2)
        cur_gif_frame.grid(row=1, column=1)
        self.current_kanji = tk.Label(text=self.files[0][0],font=("Arial", 25), master=cur_kanji_frame)
        self.current_kun = tk.Label(text=f"Kun: {self.files[3][0]}",font=("Arial", 25), master=cur_kun_frame)
        self.current_on = tk.Label(text=f"On: {self.files[2][0]}",font=("Arial", 25), master=cur_on_frame)
        self.gif_label = tk.Label(master=cur_gif_frame)
        return [cur_kanji_frame, cur_gif_frame, cur_kun_frame, cur_on_frame], [self.current_kanji, self.current_kun, self.current_on, self.gif_label]
    
    def bind_keys(self):
        self.window.bind("<Up>", self.handle_kanji_view)
        self.window.bind("<Down>", self.handle_yomi_view)
        self.window.bind("<Right>", self.handle_next)
        self.window.bind("<Left>", self.handle_previous)

    def initiate_view(self):
        self.window.rowconfigure(0, weight=1, minsize=600)
        self.window.rowconfigure(1, weight=1, minsize=150)
        self.window.columnconfigure(0, weight=1, minsize=400)
        self.window.columnconfigure(1, weight=1, minsize=400)
        self.window.columnconfigure(2, weight=1, minsize=400)
        self.current_kanji.pack()

        
    def handle_kanji_view(self, event):
        self.load_gif()
        self.gif_label.pack()
        self.current_kanji.config(text=self.files[1][self.current],font=("Arial", 25))
        self.current_kun.pack()
        self.current_on.pack()
        self.start_animation()

    def load_gif(self):
        gif_bytes = Comms.request_kanji(self.files[1][self.current])
        gif_image = Image.open(gif_bytes)
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif_image)]
        self.frame_count = len(self.frames)

    def animate_gif(self, indx):
        frame = self.frames[indx]
        indx = (indx + 1) % self.frame_count
        self.gif_label.configure(image=frame)
        self.anim_is_running = self.window.after(50, self.animate_gif, indx)

    def start_animation(self):
        if not self.anim_is_running:
            self.animate_gif(0)

    def stop_animation(self):
        if self.anim_is_running:
            self.gif_label.grid_forget()
            self.window.after_cancel(self.anim_is_running)
            self.anim_is_running = None

    def handle_yomi_view(self, event):
        self.current_kanji.config(text=self.files[0][self.current])
        self.current_kun.grid_forget()
        self.current_on.grid_forget()
        self.stop_animation()

    def handle_next(self, event):
        if self.current == len(self.files[0]) - 1:
            return
        self.current += 1
        self.current_kanji.config(text=self.files[0][self.current],font=("Arial", 25))
        self.current_kun.config(text=f"Kun: {self.files[3][self.current]}",font=("Arial", 25))
        self.current_on.config(text=f"On: {self.files[2][self.current]}",font=("Arial", 25))

    def handle_previous(self, event):
        if self.current == 0:
            return
        self.current -= 1
        self.current_kanji.config(text=self.files[0][self.current],font=("Arial", 25))
        self.current_kun.config(text=f"Kun: {self.files[3][self.current]}",font=("Arial", 25))
        self.current_on.config(text=f"On: {self.files[2][self.current]}",font=("Arial", 25))

        

    def destroy(self):
        for i in self.widgets:
            i.destroy()
        for i in self.frames:
            i.destroy()
        self.current_kanji.destroy()
        for i in range(self.window.grid_size()[1]):
            self.window.grid_rowconfigure(i, weight=0, minsize=0)
        for i in range(self.window.grid_size()[0]):
            self.window.grid_columnconfigure(i, weight=0, minsize=0)

    



class Comms:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def request_kanji(kanji):
        req = requests.get(f"https://raw.githubusercontent.com/Sam0ni/kanji.gif/master/kanji/gif/150x150/{kanji}.gif")
        gif_bytes = BytesIO(req.content)
        return gif_bytes

if __name__ == "__main__":
    window = tk.Tk()
    shuffler = App(window)
    shuffler.start()
    window.mainloop()