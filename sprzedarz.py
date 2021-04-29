from os import path
import pandas as pd
from pandas import DataFrame, merge, to_datetime
from matplotlib import pyplot as plt

kursy = "Dane\KursyNBP"

eksport = "Dane\Eksport"

rok = 2020
nazwaplikuEksport = f"Eksport{str(rok)}.xlsx"
nazwapliku = f"Archiwum_Tab_C_{str(rok)}.xls"

nbp = pd.read_excel(path.join(kursy, nazwapliku), "kupno")

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

# eksEUR = merge(
#     eks.loc[
#         (eks["Waluta"] == "EUR") & (eks["Akronim"] != "Anulowany") & (eks["Netto"] > 0)
#     ],
#     nbp[["Data", "EUR"]],
#     how="inner",
#     on="Data",
# )
# eksEUR.drop(["Waluta"], axis=1, inplace=True)
# eksEUR["Wartość sprzedarzy PLN"] = eksEUR["EUR"] * eksEUR["Netto"]
# eksEUR["Procent całości"] = (
#     eksEUR["Wartość sprzedarzy PLN"] / eksEUR["Wartość sprzedarzy PLN"].sum()
# )

eksUSD = merge(
    eks.loc[
        (eks["Waluta"] == "USD") & (eks["Akronim"] != "Anulowany") & (eks["Netto"] > 0)
    ],
    nbp[["Data", "USD"]],
    how="inner",
    on="Data",
)
eksUSD.drop(["Waluta"], axis=1, inplace=True)
eksUSD["Wartość sprzedarzy PLN"] = eksUSD["USD"] * eksUSD["Netto"]
eksUSD["Procent całości"] = (
    eksUSD["Wartość sprzedarzy PLN"] / eksUSD["Wartość sprzedarzy PLN"].sum()
)

df = eksUSD.sort_values(by=["Procent całości"], ascending=False)

print(df)

# plt.bar(df["Akronim"], df["Wartość sprzedarzy PLN"])
# plt.xlabel("Akronim")
# plt.ylabel("Wartość sprzedarzy PLN")
# plt.xticks(rotation=45)

# plt.tight_layout()


# plt.show()

# df.to_excel("SprzedarzUSD.xlsx", index=False)
