from random import shuffle
import os

def generatorf(x: list):
    for i in x:
        yield i

def kanjishuffle():
    
    chosenfile = filu_service("kanjit")

    ilman_tiedostopäätettä = chosenfile[0:-4]
    merkit = ilman_tiedostopäätettä + "_merkit.txt"

    mrlist = file_strip_and_list(chosenfile)
    mrmerkillist = file_strip_and_list(merkit)
    mrlist, mrmerkillist = katko_lista(mrlist, mrmerkillist)
    genmrlist, genmrmerkillist = shufflea_kaks_listaa(mrlist, mrmerkillist)
    iteraattori(len(mrlist), genmrlist, genmrmerkillist)

def on_kun_shuffle():

    chosenfile = filu_service("kanjit")
    
    ilman_tiedostopäätettä = chosenfile[0:-4]
    kun = ilman_tiedostopäätettä + "_kun.txt"
    on = ilman_tiedostopäätettä + "_on.txt"
    #merkit = ilman_tiedostopäätettä + "_merkit.txt"

    mrlist = file_strip_and_list(chosenfile)
    mrkunlist = file_strip_and_list(kun)
    mronlist = file_strip_and_list(on)
    #mrmerkillist = file_strip_and_list(merkit)

    #mrmerkillist, mryomilist = katko_lista(mrmerkillist, [f"merkitys: {mrlist[i]}, kun: {mrkunlist[i]}, on: {mronlist[i]}" for i in range(len(mrkunlist))])
    mrlist, mryomilist = katko_lista(mrlist, [f"kun: {mrkunlist[i]}, on: {mronlist[i]}" for i in range(len(mrkunlist))])

    genmrlist, genmryomilist = shufflea_kaks_listaa(mrlist, mryomilist)
    iteraattori(len(mrlist), genmrlist, genmryomilist)



def sanashuffle():
    mrlist = []
    mrlist2 = []
    while True:
        try:
            print("1. Suomi-Japani\n2. Japani-Suomi")
            kumminpäin = int(input())
            if kumminpäin in (1, 2):
                break
        except:
            continue


    chosenfile = filu_service("sanat")
    with open(chosenfile, "r", encoding="utf-8") as file:
        data = file.read()
        ykks, kakks = data.split("-----")
        for word in ykks.split("\n"):
            if word != "\n" and word != "":
                mrlist.append(word.replace("\n", ""))
        for word in kakks.split("\n"):
            if word != "\n" and word != "":
                mrlist2.append(word.replace("\n", ""))
    
    genmrlist, genmrlist2 = shufflea_kaks_listaa(mrlist, mrlist2)

    if kumminpäin == 1:
        iteraattori(len(mrlist), genmrlist, genmrlist2)
    else:
        iteraattori(len(mrlist), genmrlist2, genmrlist)


def katko_lista(lista1, lista2=None):
    print(f"Listassa on {len(lista1)} kanjia")
    mistä = int(input("Mistä: "))
    mihin = int(input("Mihin: "))
    
    klista1 = katko_apu(lista1, mistä, mihin)
    if lista2:
        klista2 = katko_apu(lista2, mistä, mihin)
        return klista1, klista2
    return klista1

def chop_and_shuffle_lists(files, where, to):
    chopped_files = [katko_apu(l, where, to) for l in files]
    return shuffle_kanji_parts(chopped_files[0], chopped_files[1], chopped_files[2], chopped_files[3])
    

def katko_apu(lista, mistä, mihin):
    return lista[mistä - 1:mihin]

def shufflea_kaks_listaa(lista1, lista2):
    temp = list(zip(lista1, lista2))
    shuffle(temp)
    mrlist, mrlist2 = zip(*temp)
    mrlist, mrlist2 = list(mrlist), list(mrlist2)
    genmrlist = generatorf(mrlist)
    genmrlist2 = generatorf(mrlist2)

    return genmrlist, genmrlist2

def shuffle_kanji_parts(yomikata, kanji, ony, kun):
    temp = list(zip(yomikata, kanji, ony, kun))
    shuffle(temp)
    yomi, kan, on, ku = zip(*temp)
    yomi, kan, on, ku = list(yomi), list(kan), list(on), list(ku)
    return yomi, kan, on, ku

def get_all_lists(files, path):
    polkujatallataan = os.path.join(os.path.dirname(__file__), path)
    all_files = []
    for file in files:
        all_files.append(file_strip_and_list(os.path.join(path, file)))
    return all_files

                    

def file_strip_and_list(filu):
    with open(f"src/{filu}", "r", encoding="utf-8") as file:
        return [line.replace("\n", "") for line in file if line != "\n"]



def filu_service(faili):
    polkujatallataan = os.path.join(os.path.dirname(__file__), faili)

    files = [f for f in os.listdir(polkujatallataan) if os.path.isfile(os.path.join(faili, f))]

    files = [f for f in files if not any(x in f for x in ["_merkit", "_on", "_kun"])]

    print("valitse tiedosto: ")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    numero = int(input("tiedoston numero: "))
    chosenfile = os.path.join(faili, files[numero - 1])
    print("")
    print("")
    return chosenfile

def get_files(type, condition=None):
    polkujatallataan = os.path.join(os.path.dirname(__file__), type)

    files = [f for f in os.listdir(polkujatallataan) if os.path.isfile(os.path.join(polkujatallataan, f))]
    if condition:
        files = [f for f in files if not condition(f)]
    return files


def iteraattori(pituus, lista1, lista2=None):
    left = pituus
    os.system("")
    while True:
        left -=1
        try:
            print(next(lista1))
            if lista2:
                input()
                print(next(lista2))
            print("Jäljellä: ", left, end="")
            input("\r")
            print("\033[A                                             ")
        except:
            print("")
            print("loppu, paina enter", end="")
            input()
            break


def main():
    moodit = {1: kanjishuffle, 2: sanashuffle, 3: on_kun_shuffle}
    while True:
        moodi = int(input("1. Kanjishuffle\n2. Sanashuffle\n3. Yomishuffle\n"))
        if moodi not in moodit.keys():
            continue
        break
    moodit[moodi]()

if __name__ == "__main__":
    main()