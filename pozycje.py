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
    try:
        df.columns = columns
        poz_DataFrame = poz_DataFrame.append(df)
    except:
        
        if len(df.columns) > 12:
            print(d, "Za dużo kolumn \n")
            # print(df.info())
            drop_col = [x for x in df.columns if "Unnamed" in x]
            df.drop(drop_col, axis=1, inplace=True)
            df.columns = columns
            poz_DataFrame = poz_DataFrame.append(df)
        elif len(df.columns) < 12:
            print(d, "Za mało kolumn \n")
        else:
            print(d, "jakiś inny problem \n")


poz_DataFrame = poz_DataFrame.loc[
    (poz_DataFrame["Towar"] != "A-VISTA")
    & (poz_DataFrame["Towar"] != "FRACHT")
    & (poz_DataFrame["Towar"] != "PALETA(Y)")
]


def NazwaFormy(n):
    if (type(n) != str):
        return "Brak tekstu w komórce!!"        
    try:
        n = n.split(" ")
        nazwa = str(n[0][0]) + " " + str(n[0][1:])
        return nazwa
    except:
        return "Nazwa towaru wedłóg innego formatu"


def Obiorca(n):
    if (type(n) != str):
        return "Brak tekstu w komórce!!"
    try:
        n = n.split(" ")
        nazwa = str(n[-1][1:])
        return nazwa.strip()
    except:
        return "Nazwa towaru wedłóg innego formatu"


def Kategoria(n):
    if (type(n) != str):
        return "Brak tekstu w komórce!!"
    try: 
        if n[0] == "0":
            return "bezb"
        elif n[0] == "1":
            return "opal"
        elif n[0] == "2":
            return "donica"
        else:
            return "BRAK DANYCH!"
    except:
        return "Nazwa towaru wedłóg innego formatu"


poz_DataFrame["Nr Formy"] = poz_DataFrame["Nazwa"].apply(NazwaFormy)

poz_DataFrame["Odbiorca"] = poz_DataFrame["Nazwa"].apply(Obiorca)

poz_DataFrame["Kategoria"] = poz_DataFrame["Towar"].apply(Kategoria)

poz_DataFrame.drop(
    ["Lp.", "Towar", "Jm", "Cena", "Waluta", "Netto", "Brutto", "Rabat", "Nazwa"],
    axis=1,
    inplace=True,
)


