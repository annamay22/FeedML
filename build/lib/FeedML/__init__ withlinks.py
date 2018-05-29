import pandas as pd
import matplotlib.pyplot as plt
from . import get_data

class faszom:
    
    def __init__(self):
        self.valasztas10_data = pd.DataFrame()
        self.valasztas14_data = pd.DataFrame()
        self.valasztas18_data = pd.DataFrame()
        self.like_data = pd.DataFrame()
        self.reach_data = pd.DataFrame()
        self.asz_data = pd.DataFrame()
        self.kozmunka_data = pd.DataFrame()
        self.terstat_data = pd.DataFrame()
        self.terstat_city_data = pd.DataFrame()
        self.match = pd.read_csv("https://www.dropbox.com/s/nukb9fqv3p3gd7y/match.csv?dl=1").set_index("telepules")
    
    def get_fb_data(self, source = "/Users/macintosh/Dropbox/Prog2/Momentum_feladat/FacebookInsightsDataExportMomentumMozgalom2018-05-20.xlsx", sheets = ["Lifetime Likes by City","Weekly Reach by City"], match = None):
        if match == None:
            match = self.match
        self.like_data = get_data.process_fb(source, sheets[0], match) #ez a get_data nevu scriptbol a get_facebook fv
        sheets = sheets[1:]
        if len(sheets) > 0:
            self.reach_data = get_data.process_fb(source, sheets[0], match) #ez a get_data nevu scriptbol a get_facebook fv

    def get_valasztas_data(self,sources = {2010: "https://www.dropbox.com/s/bynj7gn6l61835n/eredmeny_2010.csv?dl=1",2014: "https://www.dropbox.com/s/rv6f8kioqllqub0/eredmeny_2014.csv?dl=1",2018: "https://www.dropbox.com/s/ah07z7p86m3qaus/eredmeny_2018.csv?dl=1"}):
        """sources: dictionary of source links with integer year keys"""
        if 2010 in sources.keys():
            self.valasztas10_data = pd.read_csv(sources[2010])
        if 2014 in sources.keys():
            self.valasztas14_data = pd.read_csv(sources[2014])
        if 2018 in sources.keys():
            self.valasztas18_data = pd.read_csv(sources[2018])

    def get_asz_data(self, source = "/Users/macintosh/Dropbox/Prog2/Momentum_feladat/alapszervezet.xlsx", match = None):
        if match == None:
            match = self.match
        self.asz_data = get_data.process_asz(source, match)

    def get_kozmunka(self, source = "https://www.dropbox.com/s/bj9rhpptt0e29zh/kozmunka.csv?dl=1"):
        self.kozmunka_data = pd.read_csv(source)

    def get_terstat(self, source = "https://www.dropbox.com/s/6yujm3375w2mg33/terstat.csv?dl=1"):
        self.terstat_data = pd.read_csv(source)

    def get_terstat_city(self, source = "https://www.dropbox.com/s/3fl9xnpbee91ncz/terstat_city.csv?dl=1"):
        self.terstat_city_data = pd.read_csv(source)

    def merge_listdf(listdf, level):
        merged = None
        for i in listdf:
            if merged is None:
                merged = i.set_index(level)
            else:
                merged = merged.merge(i.set_index(level), how='outer', left_index=True, right_index=True)
        return merged

def merge_listdf(listdf, level):
    merged = None
    for i in listdf:
        if merged is None:
            merged = i.set_index(level)
        else:
            merged = merged.merge(i.set_index(level), how='outer', left_index=True, right_index=True)
    return merged

def tablemaker(tables, level='jaras'):
    """
    elerheto tablak
    jarasi szinten: terstat, likes, reach, asz
    telepulesi szinten: terstat_city, kozmunka, likes, reach, asz, valasztasos dolgok
    nagyvarosi szinten: terstat_bigcity, kozmunka, likes, reach, asz,  valasztasos dolgok 
    """
    if level == 'jaras':
        for table in tables:
            try:
                table.set_index('jaras')
            except:
                print('A tablakat nem lehet jarasi szinten bemutatni')
                return None
            return merge_listdf(listdf = tables, level = level)
        
    elif level == 'telepules':
        for table in tables:
            try:
                table.set_index('telepules')
            except:
                print('A tablakat nem lehet telepulesi szinten bemutatni')
                return None
        return merge_listdf(listdf = tables, level = level)
    
    elif level == 'nagyvaros':
        lok = self.asz_data.telepules.unique()
        return tablemaker(tables, level = 'telepules').loc[lok]
        
    else:
        print('Az aggregáltsági szintet nem ismerem, gazdám. Adj meg egyet a jaras, telepules, nagyvaros 3asbol.')
        return None

def faszomkivan(mivel):
    return(print("Faszom kivan a " + mivel + "!!!"))