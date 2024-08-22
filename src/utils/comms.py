from io import BytesIO
import requests


class Comms:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def request_kanji(kanji):
        req = requests.get(f"https://raw.githubusercontent.com/Sam0ni/kanji.gif/master/kanji/gif/150x150/{kanji}.gif")
        gif_bytes = BytesIO(req.content)
        return gif_bytes