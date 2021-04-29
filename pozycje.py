from pandas import read_excel, DataFrame
from os import listdir, path

path_to_poz = ".\Dane\Zamowienia\Poz"

# Pliki pozycji zamówień z roku 2021
list_of_dir = [x for x in listdir(path_to_poz) if "Poz21" in x]

list_of_df = list()

poz_DataFrame = DataFrame()
columns = [
    "Dokument",
    "Lp.",
    "Towar",
    "Ilość",
    "Jm",
    "Cena",
    "Waluta",
    "Netto",
    "Brutto",
    "Rabat",
    "Nazwa",
    "Data realizacji",
]

for d in list_of_dir:
    df = read_excel(path.join(path_to_poz, d))
    df.columns = columns
    poz_DataFrame = poz_DataFrame.append(df)


poz_DataFrame = poz_DataFrame.loc[
    (poz_DataFrame["Towar"] != "A-VISTA")
    & (poz_DataFrame["Towar"] != "FRACHT")
    & (poz_DataFrame["Towar"] != "PALETA(Y)")
]


def NazwaFormy(n):
    n = n.split(" ")
    nazwa = str(n[0][0]) + " " + str(n[0][1:])
    return nazwa


def Obiorca(n):
    n = n.split(" ")
    nazwa = str(n[-1][1:])
    return nazwa.strip()


def Kategoria(n):
    if n[0] == "0":
        return "bezb"
    elif n[0] == "1":
        return "opal"
    elif n[0] == "2":
        return "donica"
    else:
        return "BRAK DANYCH!"


poz_DataFrame["Nr Formy"] = poz_DataFrame["Nazwa"].apply(NazwaFormy)

poz_DataFrame["Odbiorca"] = poz_DataFrame["Nazwa"].apply(Obiorca)

poz_DataFrame["Kategoria"] = poz_DataFrame["Towar"].apply(Kategoria)

poz_DataFrame.drop(
    ["Lp.", "Towar", "Jm", "Cena", "Waluta", "Netto", "Brutto", "Rabat", "Nazwa"],
    axis=1,
    inplace=True,
)
# print(poz_DataFrame)
