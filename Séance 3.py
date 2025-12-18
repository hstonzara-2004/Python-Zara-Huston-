#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
# Sources des données : production de M. Forriez, 2016-2023*

with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

#Question 5 : les colonnes à caractères quantitatifs

colonnes_quantitatives = [col for col in contenu.columns if contenu[col].dtype in ['int64', 'float64']] #valeur quantitatives avec/sans décimales
moyennes = [] #listes
medianes = []
modes = []
ecarts_types = []
ecarts_absolus = []
etendues = []

for col in colonnes_quantitatives:
    data = contenu[col].dropna()

    moy = data.mean()#moyenne
    moyennes.append(moy)

    med = data.median()#médiane
    medianes.append(med)
    
    mode_val = data.mode()#mode (!!!!difficile alignement)
    if not mode_val.empty:
        modes.append(mode_val.iloc[0])
    else:
        modes.append(np.nan)
    
    ecart = data.std()#écart-type
    ecarts_types.append(ecart)
    
    ecart_abs = np.abs(data - moy).mean()#écart absolu à la moyenne
    ecarts_absolus.append(ecart_abs)
    
    etendue = data.max() - data.min()#étendue
    etendues.append(etendue)

stats = pd.DataFrame({
    "Colonne": colonnes_quantitatives,
    "Moyenne": moyennes,
    "Médiane": medianes,
    "Mode": modes,
    "Ecart-type": ecarts_types,
    "Ecart absolu moy": ecarts_absolus,
    "Etendue": etendues
})
stats = stats.round(2) #arrondir à 2 déclimal max
print(stats)

#Question 6 : liste

print(list(stats.columns))

#Question 7 : distance quartile et interdécile 

iqr = [] #quartile
idr = [] #décile 

for col in colonnes_quantitatives:
    data = contenu[col].dropna()

    q1 = data.quantile(0.25) #25% - quartiles
    q3 = data.quantile(0.75)
    iqr.append(q3 - q1)

    d1 = data.quantile(0.1)#10% - #décile
    d9 = data.quantile(0.9)
    idr.append(d9 - d1)

stats['IQR'] = iqr
stats['IDR'] = idr

print(stats.round(2))

#Question 8 : boîte à moustache 

for col in colonnes_quantitatives:
    data = contenu[col].dropna()
    plt.figure(figsize=(6,6))
    plt.boxplot(data)
    plt.title(f"Boîte à moustache - {col}")
    plt.ylabel("Valeurs")
    plt.savefig(f"img/boxplot_{col}.png") #choisir l'emplacement
    plt.close()

#Question 9

with open ("data/island-index.csv", encoding= "utf-8") as fichier2:
    contenu = pd.read_csv(fichier2, low_memory=False) #problème car colonne 6 a plusieurs types
print(contenu)

#question 10 : nombres d'îles/superficie 
#organigramme

contenu["Surface (km²)"] = pd.to_numeric(contenu["Surface (km²)"], errors='coerce')# bien copier coller la façon dont surface est noté sur le csv sinon ça marche pas
surface = contenu["Surface (km²)"].dropna() #sélection de la colonne 
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, float('inf')]
labels = ("0-10", "10-25","25-50","50-100", "100-2500", "2500-5000","5000-10000", "10000+")
categories = pd.cut(surface, bins=bins, labels=labels, right=True, include_lowest=True)
compte = categories.value_counts().sort_index()
print("nombre d'île / catégorie de surface :")
print(compte)













