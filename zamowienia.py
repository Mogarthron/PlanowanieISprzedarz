from dokumenty import dok_DataFrame
from pozycje import poz_DataFrame
from Classys import DaneZBazy
from pandas import merge, DataFrame



Orders = merge(dok_DataFrame, poz_DataFrame, how="inner", on="Dokument")
# print(Orders.info())


Formy = Orders["Nr Formy"].unique()

dzb = DaneZBazy()

def UtworzListeParametrow():
    ciap_Formy = ["'" + x + "'" for x in Formy.tolist()]
    list = ["(",")"]
    data = ",".join(ciap_Formy).join(list)   

    
    return data



df = dzb.PobierzDane(UtworzListeParametrow())

df = df.groupby("Nr Formy", as_index = False).mean()
df.to_excel("DaneFormy.xlsx")
# print(df.info())


# sredniaWagaBrutto = df[["Nr Formy", "WAGA_BRUTTO"]]

# SzacowaneWytobycie = merge(Orders, sredniaWagaBrutto, on="Nr Formy", how="inner")
# SzacowaneWytobycie["Szacowane Wydobycie Brutto"] = SzacowaneWytobycie["Ilość"] * SzacowaneWytobycie["WAGA_BRUTTO"] / 1000
# # SzacowaneWytobycie.to_excel("SzacowaneWydobycie.xlsx", index=False)
# print(SzacowaneWytobycie.info())


