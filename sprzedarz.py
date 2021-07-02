from os import path
import pandas as pd
from pandas import DataFrame, merge, to_datetime
from matplotlib import pyplot as plt

kursy = "Dane\KursyNBP"

eksport = "Dane\Eksport"

sprzedarz = "Dane\Sprzedarz"


rok = 2020
nazwaplikuEksport = f"Eksport{str(rok)}.xlsx"
nazwaplikuSprzedarz = f"Sprzedarz{str(rok)}.xlsx"
nazwaplikuNBP = f"Archiwum_Tab_C_{str(rok)}.xls"

spr = pd.read_excel(path.join(sprzedarz, nazwaplikuSprzedarz), "Sprzedarz")

spr = spr.loc[(spr["Akronim"] != "Anulowany")]
spr.drop(
    [
        "Miasto",
        "Data wystawienia",
        "Brutto",
        "Źródłowy",
        "Magazynowe",
        "Cecha transakcji",
        "Opis",
    ],
    axis=1,
    inplace=True,
)

spr["Waluta"] = "PLN"
spr["Kurs odniesienia"] = 1

# print(spr)


nbp = pd.read_excel(path.join(kursy, nazwaplikuNBP), "kupno")

new_headers = nbp.loc[nbp["data"] == "kod ISO"].values.tolist()
new_headers[0][0] = "Data"
new_headers[0][-1] = "pełny numer tabeli"
new_headers[0][-2] = "nr tabeli"

nbp.columns = new_headers[0]
nbp.drop(nbp.head(1).index, inplace=True)
nbp.drop(nbp.tail(4).index, inplace=True)

nbp["Data"] = to_datetime(nbp["Data"])


eks = pd.read_excel(path.join(eksport, nazwaplikuEksport), "Eksport")
eks.drop(["Opis", "Cecha transakcji", "Źródłowy", "Miasto"], axis=1, inplace=True)


def WartoscSprzedarzyWPLN(waluta):
    eksWal = merge(
        eks.loc[
            (eks["Waluta"] == waluta)
            & (eks["Akronim"] != "Anulowany")
            & (eks["Netto"] > 0)
        ],
        nbp[["Data", waluta]],
        how="inner",
        on="Data",
    )

    eksWal["Kurs odniesienia"] = eksWal[waluta]
    eksWal.drop([waluta], axis=1, inplace=True)
    return eksWal


eksWal = DataFrame()
eksWal = eksWal.append(WartoscSprzedarzyWPLN("EUR"))
eksWal = eksWal.append(WartoscSprzedarzyWPLN("USD"))
eksWal = eksWal.append(WartoscSprzedarzyWPLN("SEK"))
eksWal = eksWal.append((spr))


eksWal["Wartość sprzedarzy PLN"] = eksWal["Kurs odniesienia"] * eksWal["Netto"]
eksWal["Wartość sprzedarzy PLN"] = eksWal["Wartość sprzedarzy PLN"].astype("float32")

Odbiorca_Sprzedarz = eksWal.groupby(["Akronim"]).sum()

Odbiorca_Sprzedarz.sort_values("Wartość sprzedarzy PLN", ascending=False, inplace=True)

Odbiorca_Sprzedarz["Procent całości"] = (
    Odbiorca_Sprzedarz["Wartość sprzedarzy PLN"]
    / Odbiorca_Sprzedarz["Wartość sprzedarzy PLN"].sum()
)

Odbiorca_Sprzedarz["Narastający procent"] = Odbiorca_Sprzedarz[
    "Procent całości"
].cumsum()

Odbiorca_Sprzedarz.to_excel("O_S.xlsx")

# O_S_80 = Odbiorca_Sprzedarz.loc[Odbiorca_Sprzedarz["Narastający procent"] <= 0.8]
# O_S_20 = Odbiorca_Sprzedarz.loc[Odbiorca_Sprzedarz["Narastający procent"] >= 0.8]

# print(O_S_80)

# print(
#     f"Wszyscy odbiorcy: {Odbiorca_Sprzedarz.shape[0]}. Odbiorcy generujący 80% zysku: {O_S_80.shape[0]}"
# )

# print("Wartość sprzedarzy O_S_80", O_S_80["Wartość sprzedarzy PLN"].sum())


# print(O_S_80.info())


# plt.bar(O_S_80.index.values, O_S_80["Wartość sprzedarzy PLN"])
# plt.xlabel("Akronim")
# plt.ylabel("Wartość sprzedarzy PLN")

# plt.xticks(rotation=45)

# plt.tight_layout()

# plt.show()
