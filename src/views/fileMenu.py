from views.menu import Menu
import kanjishuffle


class FileMenu(Menu):
    def __init__(self, window, height, width, botans, handler, horizontally, commands=None, files=None):
        self.files = files
        super().__init__(window, height, width, botans, handler, horizontally, commands, files)
        self.init_commands()

    def init_commands(self):
        comms = [lambda c=c: self.select_kanji_file(c) for c in self.files]
        self.commands = comms

    def select_kanji_file(self, file):
        chosen_file = file
        no_file_extension = chosen_file[0:-4]
        kanjis = no_file_extension + "_merkit.txt"
        kun = no_file_extension + "_kun.txt"
        on = no_file_extension + "_on.txt"
        yomi, kanjis, kun, on = kanjishuffle.get_all_lists([chosen_file, kanjis, on, kun], "kanjit")
        self.handler(chosen_file, [yomi, kanjis, kun, on])