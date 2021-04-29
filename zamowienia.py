from dokumenty import dok_DataFrame
from pozycje import poz_DataFrame
from pandas import merge

Orders = merge(dok_DataFrame, poz_DataFrame, how="inner", on="Dokument")

print(Orders.head(30))
# Orders.to_excel("Orders.xlsx", index=False)
