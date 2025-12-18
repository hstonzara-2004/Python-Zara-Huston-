#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("data/resultats-elections-presidentielles-2022-1er-tour.csv", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)
pd.DataFrame(contenu)
print(contenu)

#Questions 6 : affichage des lignes et colonnes 

nb_lignes= len(contenu)
nb_colonnes= len(contenu.columns)

print("nombre de lignes :", nb_lignes)
print("nombre de colonnes :", nb_colonnes)

#Question 7 : afficher le type de données 

print(contenu.dtypes)
#int64=inscrits (=nombre entier) float64=abstension(=nombre décimal), object=dpartement libellé(=texte)
#faire liste

#Question 8 : afficher le nom des colonnes (1ere ligne)
print(contenu.head())
print(contenu.columns)

#Question 9 : sélectionner des inscrits

inscrits = contenu["Inscrits"]
print(inscrits)

#Question 10 : la somme totale des inscrits (boucles effectif de chaque colonne)

total_inscrits = inscrits.sum()
print("Nombre total d'inscrits", total_inscrits)

somme_colonnes=[] #liste pour stocker les noms

for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        somme_colonnes.append(contenu[col].sum())
print(somme_colonnes)#boucles qu'avec les données quantitatives donc int64(sans décimales)et flot64 (avec décimales)

for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        print(col, ":", contenu[col].sum()) #boucles plus lisible

#Question 11 : diagramme en barre nombre inscrits et votants/département (boucle)

for i in range(len(contenu)): #=>en haut = la boucle
    dept= contenu.loc[i, "Libellé du département"] 
    inscrits = contenu.loc[i, "Inscrits"]
    votants = contenu.loc[i, "Votants"]
    plt.figure(figsize=(6,4)) #le diagramme
    plt.bar(["Inscrits", "Votants"], [inscrits, votants], color=['blue', 'red'])
    plt.title(f"{dept}")
    plt.ylabel("Nombre de personnes")
    plt.ticklabel_format(style='plain', axis='y')
    #avoir les noms et pas les valeurs de matplotilib
    plt.savefig(f"{dept}.png") 
    plt.close() 

#Question 12 : diagramme circulaire votes blancs, nuls, votants, abstentions (boucle) 

import os
os.makedirs("images_circulaires", exist_ok=True)

for i in range(len(contenu)): #la boucle pour chaque département
    dept = contenu.loc[i, "Libellé du département"]
    blancs = contenu.loc[i, "Blancs"]
    nuls = contenu.loc[i, "Nuls"]
    votants = contenu.loc[i, "Votants"]
    abstention = contenu.loc[i, "Abstentions"]

    # les diff votes exprimés(donc,votants,blancs et les votes nuls)

    exprimés = votants - blancs - nuls

    valeurs = [blancs, nuls, exprimés, abstention]
    labels = ["Blancs", "Nuls", "Exprimés", "Abstention"]
    couleurs = ["lightgrey", "red", "green", "orange"]

    plt.figure(figsize=(6,6))
    plt.pie(valeurs, labels=labels, colors=couleurs, autopct='%1.1f%%', startangle=90)#les % servent à afficher les % dans le graphique circulaire!
    plt.title(f"{dept}")
    
    # Sauvegarder
    plt.savefig(f"images_circulaires/{dept}.png")
    plt.close()

#Question 13 : histogramme 

plt.figure(figsize=(8,5))
plt.hist(contenu["Inscrits"], bins=20, density=True, edgecolor='black', color='skyblue')
plt.title("Histogramme du nombre d'inscrits")
plt.xlabel("Nombre d'inscrits")
plt.ylabel("Densité")
plt.grid(alpha=0.3)
plt.show()

#BONUS 

#Diagramme circulaire/département 

noms_candidats = [
    "Arthaud", "Roussel", "Macron", "Lassalle", "Le Pen", "Zemmour",
    "Mélenchon", "Hidalgo", "Jadot", "Pécresse", "Poutou", "Dupont-Aignan"
]

colonnes_voix = [col for col in contenu.columns if "Voix" in col]

for i in range(len(contenu)):
    dept = contenu.loc[i, "Libellé du département"]
    voix = contenu.loc[i, colonnes_voix].fillna(0).tolist()
    if len(voix) != len(noms_candidats):
        print(f"Ligne {i} : {dept} → {len(voix)} valeurs Voix, {len(noms_candidats)} candidats. Skip.")
        continue

    plt.figure(figsize=(6, 6))
    plt.pie(voix, labels=noms_candidats, autopct="%1.1f%%")
    plt.title(f"Résultat du 1er tour – {dept}")
    plt.savefig(f"diagrammes2/camembert_{dept}.png", dpi=300, bbox_inches="tight")
    plt.close()

#Diagramme circulaire/France

colonnes_voix = [col for col in contenu.columns if "Voix" in col]
colonnes_noms = [col for col in contenu.columns if "Nom" in col]
voix_france = contenu[colonnes_voix].sum()
noms_candidats = contenu.loc[0, colonnes_noms].tolist()

plt.figure(figsize=(6,6))
plt.pie(voix_france, labels=noms_candidats, autopct="%1.1f%%")
plt.title("Voix par candidat – France entière")
plt.show()