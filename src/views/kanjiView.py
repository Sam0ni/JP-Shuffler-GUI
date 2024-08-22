from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
from utils.comms import Comms


class KanjiView:
    def __init__(self, window, chosen_files):
        self.window = window
        self.files = chosen_files
        self.current = 0
        self.frames, self.widgets = self.set_up_frames_and_labels()
        self.anim_is_running = None
        self.bind_keys()

    def set_up_frames_and_labels(self):
        cur_kanji_frame = tk.Frame(borderwidth=2, background="grey")
        cur_kun_frame = tk.Frame(borderwidth=2, background="grey")
        cur_on_frame = tk.Frame(borderwidth=2, background="grey")
        cur_gif_frame = tk.Frame(borderwidth=2, background="grey")
        cur_label_frame = tk.Frame(borderwidth=2, background="grey")
        cur_label_frame.grid(row=1, column=1)
        self.current_kanji = tk.Label(text=self.files[0][0],font=("Arial", 25), master=cur_kanji_frame)
        self.current_kun = tk.Label(text=f"Kun: {self.files[3][0]}",font=("Arial", 25), master=cur_kun_frame)
        self.current_on = tk.Label(text=f"On: {self.files[2][0]}",font=("Arial", 25), master=cur_on_frame)
        self.gif_label = tk.Label(master=cur_gif_frame)
        self.current_label = tk.Label(master=cur_label_frame, text=f"{self.current + 1}/{len(self.files[0])}", font=("Arial", 18))
        self.current_kanji.pack()
        self.current_kun.pack()
        self.current_on.pack()
        self.gif_label.pack()
        self.current_label.pack()
        return [cur_kanji_frame, cur_gif_frame, cur_kun_frame, cur_on_frame, cur_label_frame], [self.current_kanji, self.current_kun, self.current_on, self.gif_label, self.current_label]
    
    def bind_keys(self):
        self.window.bind("<Up>", self.handle_kanji_view)
        self.window.bind("<Down>", self.handle_yomi_view)
        self.window.bind("<Right>", self.handle_next)
        self.window.bind("<Left>", self.handle_previous)

    def initiate_view(self):
        self.window.rowconfigure(0, weight=1, minsize=550)
        self.window.rowconfigure(1, weight=1, minsize=150)
        self.window.columnconfigure(0, weight=1, minsize=400)
        self.window.columnconfigure(1, weight=1, minsize=400)
        self.window.columnconfigure(2, weight=1, minsize=400)
        self.current_kanji.master.grid(row=0, column=1)

        
    def handle_kanji_view(self, event):
        self.load_gif()
        self.gif_label.master.grid(row=0, column=1)
        self.current_kanji.master.grid_forget()
        self.current_kun.master.grid(row=0, column=0, sticky="se")
        self.current_on.master.grid(row=0, column=2, sticky="sw")
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
            self.gif_label.master.grid_forget()
            self.window.after_cancel(self.anim_is_running)
            self.anim_is_running = None

    def handle_yomi_view(self, event):
        self.current_kanji.config(text=self.files[0][self.current])
        self.current_kanji.master.grid(row=0, column=1)
        self.current_kun.master.grid_forget()
        self.current_on.master.grid_forget()
        self.stop_animation()

    def handle_next(self, event):
        if self.current == len(self.files[0]) - 1:
            return
        if self.anim_is_running:
            self.handle_yomi_view(None)
        self.current += 1
        self.update_labels()

    def handle_previous(self, event):
        if self.current == 0:
            return
        if self.anim_is_running:
            self.handle_yomi_view(None)
        self.current -= 1
        self.update_labels()

    def update_labels(self):
        self.current_kanji.config(text=self.files[0][self.current],font=("Arial", 25))
        self.current_kun.config(text=f"Kun: {self.files[3][self.current]}",font=("Arial", 25))
        self.current_on.config(text=f"On: {self.files[2][self.current]}",font=("Arial", 25))
        self.current_label.config(text=f"{self.current + 1}/{len(self.files[0])}")

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