import tkinter as tk
import kanjishuffle

class ChopMenu:
    def __init__(self, window, files, chosen_file, handler):
        self.window = window
        self.files = files
        self.chosen_file = chosen_file
        self.holding = None
        self.widgets = []
        self.frames = []
        self.handler = handler
        self.where = 1
        self.to = len(chosen_file[0])
        self.shuffle = True
        self.commands = {0: ((lambda event: self.hold_button(self.handle_where_change, False)), (lambda event: self.hold_button(self.handle_where_change, True))), 2: ((lambda event: self.hold_button(self.handle_to_change, False)), (lambda event: self.hold_button(self.handle_to_change, True))), 1: lambda: self.handle_submit()}

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
        self.create_buttons()
        self.create_where_and_to_texts()

    def create_buttons(self):
        for i in (0, 2):
            freimi = tk.Frame(relief=tk.SUNKEN, borderwidth=10)
            freimi2 = tk.Frame(relief=tk.SUNKEN, borderwidth=10)
            botan = tk.Button(text="Up", width=50, height=10, bg="blue", fg="red", master=freimi)
            botan2 = tk.Button(text="Down", width=50, height=10, bg="blue", fg="red", master=freimi2)
            botan.bind('<ButtonPress-1>', self.commands[i][0])
            botan.bind('<ButtonRelease-1>', lambda event: self.stop_holding())
            botan2.bind('<ButtonPress-1>', self.commands[i][1])
            botan2.bind('<ButtonRelease-1>', lambda event: self.stop_holding())
            freimi.grid(row=0, column=i, pady=10)
            freimi2.grid(row=2, column=i, pady=10)
            botan.grid(row=0, column=i, sticky="s")
            botan2.grid(row=2, column=i, sticky="n")
            self.widgets.extend([botan, botan2])
            self.frames.extend([freimi, freimi2])
        submitFrame = tk.Frame(relief=tk.GROOVE, borderwidth=10)
        submitFrame.grid(row=1, column=1, pady=10)
        submitBotan = tk.Button(text="submit", width=50, height=10, bg="red", fg="white", master=submitFrame, command=self.commands[1])
        submitBotan.pack()
        shuffleFrame = tk.Frame(relief=tk.GROOVE, borderwidth=10)
        shuffleFrame.grid(row=2, column=1, pady=10)
        self.shuffleBotan = tk.Button(text="Shuffle? Yes!", width=25, height=5, bg="purple", fg="white", master=shuffleFrame, command=self.shuffleButtonCommand)
        self.shuffleBotan.pack()
        self.widgets.extend([submitBotan, self.shuffleBotan])
        self.frames.extend([submitFrame, shuffleFrame])

    def shuffleButtonCommand(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            self.shuffleBotan.configure(text="Shuffle? Yes!")
        else:
            self.shuffleBotan.configure(text="Shuffle? No!")

    
    def create_where_and_to_texts(self):
        self.where_label = tk.Label(text=f"Mistä: {self.where}", font=("Arial", 25))
        self.to_label = tk.Label(text=f"Mihin: {self.to}", font=("Arial", 25))
        self.where_label.grid(row=1, column=0)
        self.to_label.grid(row=1, column=2)
        self.widgets.extend([self.where_label, self.to_label])

    def handle_where_change(self, neg):
        wait_values = {20: 100, 100: 50}
        by = 1
        wait = next((wait for limit, wait in wait_values.items() if self.how_long < limit), 5)
        if neg:
            by *= -1
        
        if (by < 0 and self.where > 1) or (by > 0 and self.where < self.to):
            self.where += by
        elif (by > 0 and self.to == self.where):
            self.where = 1
        elif (by < 0 and self.where == 1):
            self.where = 0 + self.to
        self.where_label["text"] = f"Mistä: {self.where}"
        self.how_long += 1
        self.holding = self.window.after(wait, self.handle_where_change, neg)

    def handle_to_change(self, neg):
        wait_values = {20: 100, 100: 50}
        by = 1
        wait = next((wait for limit, wait in wait_values.items() if self.how_long < limit), 5)
        if neg:
            by *= -1
        if (by < 0 and self.to > self.where) or (by > 0 and self.to < len(self.chosen_file[0])):
            self.to += by
        elif (by < 0 and self.to == self.where):
            self.to = len(self.chosen_file[0])
        elif (by > 0 and self.to == len(self.chosen_file[0])):
            self.to = 0 + self.where
        self.to_label["text"] = f"Mihin: {self.to}"
        self.how_long += 1
        self.holding = self.window.after(wait, self.handle_to_change, neg)

    def hold_button(self, handle, neg):
        if not self.holding:
            self.how_long = 0
            handle(neg)
        
    def stop_holding(self):
        if self.holding:
            self.how_long = 0
            self.window.after_cancel(self.holding)
            self.holding = None

    def handle_submit(self):
        choppedFiles = kanjishuffle.chop_and_shuffle_lists(self.chosen_file, self.where, self.to, self.shuffle)
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