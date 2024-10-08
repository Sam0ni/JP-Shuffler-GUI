from views.menu import Menu
import kanjishuffle

class MainMenu(Menu):
    def __init__(self, window, height, width, botans, handler, horizontally, commands=None):
        super().__init__(window, height, width, botans, handler, horizontally, commands, ["Kanjishuffle", "Under Construction", "Under Construction"])

    def init_commands(self):
        comms = {0: self.kanji_command, 1: lambda: print("punajuur"), 2: lambda: print("kurpitsasalaatti")}
        self.commands = comms

    def kanji_command(self):
        self.files = kanjishuffle.get_files("kanjit", lambda fail: any(x in fail for x in ["_merkit", "_on", "_kun"]))
        self.handler(self.files)