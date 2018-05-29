# -*- coding: utf-8 -*-
"""
Created on Sun May 20 22:09:55 2018

@author: Lenovo
"""

import pandas as pd
import unidecode

def stripos(os):
    if "ő" in os.lower() or "ű" in os.lower() or "ü" in os.lower() or "ö" in os.lower():
        return unidecode.unidecode(os)
    else:
        return os

def process_fb(excelfile, sheet, match):
    fb = pd.read_excel(excelfile, sheet_name=sheet)
    fb = fb.drop(columns = ['Description']).set_index('Date').T
    fb['Location'] = pd.Series(fb.index, index=fb.index)
    fb['jaras'] = fb['Location'].map(pd.DataFrame.to_dict(match)['jaras'])
    fb['telepules'] = fb['Location'].str.split(', ').str[0]
    fb['megye'] = fb['telepules'].str.split(', ').str[1]
    fb = fb.drop(columns = ['Location'])
    return fb

def process_asz(excelfile, match):    
    asz = pd.read_excel(excelfile)
    asz['Location2'] = pd.Series(asz.ASZ, index=asz.index)
    asz['Location2'] = asz['Location2'].str.split(' és környéke').str[0]
    asz['jaras'] = asz['Location2'].map(pd.DataFrame.to_dict(match)['jaras'])
    asz['Location'] = asz['Location2'].apply(stripos)
    BPtagok = 0
    BPjelentkezők = 0
    for i in range(len(asz)):
        if asz['ASZ'][i].split(' ')[0] == 'Budapest':
            BPtagok += asz['Tagok száma'][i]
            BPjelentkezők += asz['Jelentkezők száma'][i]
        else:
            pass
        
    bp = pd.DataFrame(['Budapest', 'Nem', 'Nem', BPjelentkezők, BPtagok, 'Budapest', 'Budapest']).T
    bp = bp.rename(index=str, columns={0: "ASZ", 1: "Fiktív", 2: "Vezető nélkül", 3: "Jelentkezők száma", 4: "Tagok száma", 5: "Location2", 6: "City", })
    asz = asz.append(bp, ignore_index=True)
    asz['telepules'] = asz['Location2'].str.split(". kerület").str[0].str.split(" ").str[0]
    asz = asz.drop('Location2', axis=1)
    return asz