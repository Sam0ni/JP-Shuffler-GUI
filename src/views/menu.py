from tkinter import ttk as tk

class Menu:
    def __init__(self, window, height, width, botans, handler, horizontally, commands=None, button_text=None):
        self.widgets = []
        self.frames = []
        self.window = window
        self.handler = handler
        self.horizontally = horizontally
        self.height = height
        self.width = width
        self.botans = botans
        self.commands = commands
        self.button_text = button_text

    def divide_screen(self, gauge, by, function):
        if gauge % by != 0:
            raise Exception("Not divisible width")
        one_gauge = gauge // by
        for i in range(by):
            function(i, weight=1, minsize=one_gauge)
    
    def create_buttons(self, number_of_buttons):
        for i in range(number_of_buttons):
            freimi = tk.Frame(borderwidth=10, style="Card")
            botan = tk.Button(text=self.button_text[i], width=25, master=freimi, command=self.commands[i], style='Accent.TButton')
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

    def destroy(self):
        for i in self.widgets:
            i.destroy()
        for i in self.frames:
            i.destroy()
        for i in range(self.window.grid_size()[1]):
            self.window.grid_rowconfigure(i, weight=0, minsize=0)
        for i in range(self.window.grid_size()[0]):
            self.window.grid_columnconfigure(i, weight=0, minsize=0)