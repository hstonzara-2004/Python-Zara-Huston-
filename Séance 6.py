#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

iles = ouvrirUnFichier("./data/island-index.csv")
#print(iles.head())

#Question 3 : isoler la colonne surface km² et ajouter la liste des continents
surfaces = iles["Surface (km²)"]
surfaces = surfaces.dropna()
print(surfaces.head())

continents = [85545323, 37856841, 7768030, 7605049]
surfaces = surfaces.astype(float)#en décimales
surfaces = pd.concat([surfaces, pd.Series(continents)], ignore_index=True)

print(surfaces.tail())

#Question 4 : ordre decroissant
def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste
surfaces_triees = ordreDecroissant(surfaces.tolist())
print(surfaces_triees[:5])#les plus grandes valeurs

#Question 5 : loi rang-taille
rangs= list(range(1, len(surfaces_triees)+1))
plt.figure(figsize=(10,6))
plt.plot(rangs, surfaces_triees, marker='o', color='red')
plt.title("Loi rang-taille des surfaces des continents et des îles")
plt.xlabel("Rang")
plt.ylabel("Surface km²")
plt.savefig("img/loi_rang_taille.png")
plt.close()

#Question 6 : Fonction pour convertir les données en données logarithmiques ????? pourquoi faire
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

rangs_log = conversionLog(rangs)
surfaces_log = conversionLog(surfaces_triees)
plt.figure(figsize=(10, 6))
plt.plot(rangs_log, surfaces_log, marker='o', linestyle='-', color='blue', linewidth=1)
plt.title("Loi rang–taille (axes converties en Log)")
plt.xlabel("log(rang)")
plt.ylabel("log(surface en km²)")
plt.grid(True, linewidth=0.3)
plt.savefig("img/loi_rang_taille_log.png", dpi=150)
plt.close()

#Question 7 : On peut pas faire des tests sur des rangs...car ce sont des rangs ? donc pas des données statistiques. 
#un rang = position dans un classement à partir des valeurs que j'ai triées c'est tout.


#Q7-fin 

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

monde = ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv")
#print(monde.head())

#Question 10 : isoler les colonnes 
colonnes = ["État", "Pop 2007", "Pop 2025", "Densité 2007", "Densité 2025"]
monde_selection = monde[colonnes]
print(monde_selection.head())

#Question 11 : Fonction pour obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop
etats = monde["État"].tolist()
pop2007 = monde["Pop 2007"].astype(float).tolist()
pop2025 = monde["Pop 2025"].astype(float).tolist()
dens2007 = monde["Densité 2007"].astype(float).tolist()
dens2025 = monde["Densité 2025"].astype(float).tolist()

classement_pop2007 = ordrePopulation(pop2007, etats)
classement_pop2025 = ordrePopulation(pop2025, etats)
classement_dens2007 = ordrePopulation(dens2007, etats)
classement_dens2025= ordrePopulation(dens2025, etats)

print(classement_pop2007[:10])

#question 12 : comparaison des listes 

pop2007_ordre = ordrePopulation(pop2007, etats)
pop2025_ordre = ordrePopulation(pop2025, etats)
dens2007_ordre = ordrePopulation(dens2007, etats)
dens2025_ordre = ordrePopulation(dens2025, etats)

def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement
comparaison_2007 = classementPays(pop2007_ordre, dens2007_ordre)
comparaison_2025 = classementPays(pop2025_ordre, dens2025_ordre)
comparaison_2007.sort()
comparaison_2025.sort()

#Question 13 : isoler

rangs_pop_2007 = []
rangs_dens_2007 = []

for ligne in comparaison_2007:
    rangs_pop_2007.append(ligne[0])
    rangs_dens_2007.append(ligne[1])

rangs_pop_2025 = []
rangs_dens_2025 = []

for ligne in comparaison_2025:
    rangs_pop_2025.append(ligne[0])
    rangs_dens_2025.append(ligne[1])

#Question 14: coef de corrélation et concordance des rangs 

from scipy.stats import spearmanr, kendalltau

print("Kendall et Spearman")

coef_spear_2007, p_spear_2007 = spearmanr(rangs_pop_2007, rangs_dens_2007)
coef_kendall_2007, p_kendall_2007 = kendalltau(rangs_pop_2007, rangs_dens_2007)
print("Spearman :", coef_spear_2007, "p-value :", p_spear_2007)
print("Kendall :", coef_kendall_2007, "p-value :", p_kendall_2007)

coef_spear_2025, p_spear_2025 = spearmanr(rangs_pop_2025, rangs_dens_2025)
coef_kendall_2025, p_kendall_2025 = kendalltau(rangs_pop_2025, rangs_dens_2025)
print("Spearman :", coef_spear_2025, "p-value :", p_spear_2025)
print("Kendall :", coef_kendall_2025, "p-value :", p_kendall_2025)

