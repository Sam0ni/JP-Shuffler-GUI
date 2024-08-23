# JP-Shuffler-GUI
A GUI project for an practice app that shuffles Japanese-Finnish word/kanji-pairs (and maybe more).

## Installation and running the app
The project uses poetry to manage dependencies and thus can be installed with `poetry install`. One can then run the app with the command `poetry run python3 src/app.py`.

## Structure
The app is written with Python, and more specifically its tkinter library. The app is by its looks very barebones, since tkinter is quite restrictive, but maybe someday switching language and GUI frameworks and remaking the app could be done. Since the project fetches the kanji gif animations with requests library, a cache is also deployed during the runtime (max 2h, though this can be changed) to avoid requesting same gifs many times.  

## Features
The project at the moment includes only a mode where you can choose number of kanjis from a file and whether they are shuffled or not. Then the meanings of these kanji are displayed and one can see the stroke order, kunyomi and onyomi of the kanji by pressing the up arrow. One can come back from the previous view by pressing the down arrow, and go to the next/previous with the left and right arrows.

At the moment the project includes all of the kanji from Basic Kanji Book 1 and some from 2. The meanings are in Finnish in files kanji.txt and kanji2.txt. The kunyomis and onyomis in romaji are in files kanji_kun.txt and kanji_on.txt (kanji2 for the second), and the kanji are in kanji_merkit.txt.

## Credits
The project uses the [Forest-ttk-theme](https://github.com/rdbende/Forest-ttk-theme) as the styling for tkinter.

For the kanji stroke order animations [Kanji.gif](https://github.com/jcsirot/kanji.gif) files are used.
