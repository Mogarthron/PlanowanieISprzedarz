from os import path
import requests
import pandas as pd


dir_path = os.getcwd()

kursy = "Dane\KursyNBP"

rok = 2020

nazwapliku = f"Archiwum_Tab_C_{str(2020)}.xls"


lokacjapliku = path.join(dir_path, kursy, nazwapliku)


if path.exists(lokacjapliku):
    print("Plik istnieje")
    nbp = pd.read_excel(path.join(kursy, nazwapliku), "kupno")
    print(nbp.head())
else:
    print("Plik nie istnieje \nPobieram plik ze strony NBP")

    url = "https://www.nbp.pl/kursy/archiwum/" + nazwapliku

    r = requests.get(url)

    print("Zapisuje plik w folderze")

    with open(lokacjapliku, "wb") as f:
        f.write(r.content)

    nbp = pd.read_excel(path.join(kursy, nazwapliku), "kupno")
