from pandas import read_sql, read_excel, DataFrame
from os import listdir, path
import fdb
import json

class Pozycje:
    """
    okres: okres pobierania pozycji za rok (21), 
            miesąc (2106) lub gdy nie podany pobiera 
            wszystkie dostępne pliki
    """

    list_of_dir = None
    path_to_poz = ".\Dane\Zamowienia\Poz"
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

    def __init__(self, okres=None):
        
        if okres == None:
            self.list_of_dir = [x for x in listdir(self.path_to_poz)]
        else:

            okres = "Poz" + str(okres)

            self.list_of_dir = [x for x in listdir(self.path_to_poz) if okres in x]

        for d in self.list_of_dir:
            df = read_excel(path.join(self.path_to_poz, d))
            try:
                df.columns = self.columns
                self.poz_DataFrame = self.poz_DataFrame.append(df)
            except:
                
                if len(df.columns) > 12:
                    print(d, "Za dużo kolumn \n")
                    # print(df.info())
                    drop_col = [x for x in df.columns if "Unnamed" in x]
                    df.drop(drop_col, axis=1, inplace=True)
                    df.columns = self.columns
                    self.poz_DataFrame = self.poz_DataFrame.append(df)
                elif len(df.columns) < 12:
                    print(d, "Za mało kolumn \n")
                else:
                    print(d, "jakiś inny problem \n")
        
        self.poz_DataFrame = self.poz_DataFrame.loc[
                        (self.poz_DataFrame["Towar"] != "A-VISTA")
                        & (self.poz_DataFrame["Towar"] != "FRACHT")
                        & (self.poz_DataFrame["Towar"] != "PALETA(Y)")
                    ]
        
        self.poz_DataFrame["Nr Formy"] = self.poz_DataFrame["Nazwa"].apply(self.__NazwaFormy)

        self.poz_DataFrame["Odbiorca"] = self.poz_DataFrame["Nazwa"].apply(self.__Obiorca)

        self.poz_DataFrame["Kategoria"] = self.poz_DataFrame["Towar"].apply(self.__Kategoria)

    def TabelaZNrFormyOdbiorcaKategoria(self):

        tab = self.poz_DataFrame
        

        tab.drop(["Lp.", "Nazwa"], axis=1, inplace=True,)
        
        return tab

    def __NazwaFormy(self, n):
        if (type(n) != str):
            return "Brak tekstu w komórce!!"        
        try:
            n = n.split(" ")
            nazwa = str(n[0][0]) + " " + str(n[0][1:])
            return nazwa
        except:
            return "Nazwa towaru wedłóg innego formatu"


    def __Obiorca(self, n):
        if (type(n) != str):
            return "Brak tekstu w komórce!!"
        try:
            n = n.split(" ")
            nazwa = str(n[-1][1:])
            return nazwa.strip()
        except:
            return "Nazwa towaru wedłóg innego formatu"


    def __Kategoria(self, n):
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

class DaneZBazy():


    QUERY = """SELECT r."Forma" as "Nr Formy", r."Brutto", r."Do Sor.", r."Sortownia brutto", r."Sortownia braki",
        r."Sortownia stan", r."Do Obr.", r."Obrobka brutto", r."Obrobka braki", 
        r."Obrobka stan", r."Do Mal.", r."Malarnia brutto", r."Malarnia braki", 
        r."Malarnia stan", r."Do Mat.", r."Matownia brutto", r."Matownia braki", 
        r."Matownia stan", r."Pakowanie brutto", r."Pakowanie braki", 
        r."Pakowanie stan", r."PW brutto", r."PW braki", r."Do Pak.", 
        r."Obrobka braki masy i form.",
        r."Obrobka braki masy", r."Obrobka braki formowania",
        r.WAGA_BRUTTO, r.WAGA_NETTO, r.BRAKI_RAZEM, r.WYKONANIE, r.DEKOR
    FROM "Stany" r
    where r."Forma" in xyz"""

    
    CONNECTION = None

    def __init__(self):

        file = open("Conn.json", mode="r")
        con = json.load(file)
        file.close()
        self.CONNECTION = fdb.connect(dsn=con["Dsn"], user=con["User"], password=con["Password"])

    def PobierzDane(self, params):

        self.QUERY = self.QUERY.replace("xyz", params)

        return read_sql(self.QUERY, self.CONNECTION)

    def __del__(self):

        if self.CONNECTION:
            self.CONNECTION.close()
            del self.CONNECTION
