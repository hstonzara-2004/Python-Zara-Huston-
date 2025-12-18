#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats

def ouvrirUnFichier(nom):
    with open(nom, "r", encoding="utf-8") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

donnees = ouvrirUnFichier("data/Echantillonnage-100-Echantillons.csv")
print("\nNombre total de lignes :", len(donnees)) #moyenne
print("Noms des colonnes :", list(donnees.columns))
print(donnees)

#Théorie de l'échantillonnage (intervalles de fluctuation)
print("Résultat sur le calcul d'un intervalle de fluctuation")

moyennes = {} #listes 
for col in donnees.columns:
    moyenne_col = donnees[col].mean()
    moyenne_arrondie = round(moyenne_col)
    moyennes[col] = moyenne_arrondie

print("\nMoyenne arrondie:")
for opinion, valeur in moyennes.items():
    print(f"{opinion} : {valeur}")

somme_moyennes = sum(moyennes.values())
frequences_echantillon= {}

for opinion, valeur in moyennes.items():
    freq = valeur / somme_moyennes
    frequences_echantillon[opinion] = round(freq, 2)

print("\nFréquence moyennes (échantillons)")
for opinion, freq in frequences_echantillon.items():
    print(f"{opinion}:{freq}")

#pop mère fréquence
population_mere = {
    "Pour": 852, 
    "Contre": 911, 
    "Sans opinion": 422
}

total_pop = sum(population_mere.values())
frequences_population = {}

for opinion, valeur in population_mere.items():
    freq = valeur / total_pop
    frequences_population[opinion] = round(freq, 2)

print("\nFréquence de la population mère")

for opnion, freq in frequences_population.items():
    print(f"{opinion}:{freq}")

n = 2185#taille de la pop
zC = 1.96

frequences_population = {op: val / sum(population_mere.values()) for op, val in population_mere.items()}#freq pop mère
intervalles = {}

for opinion, f in frequences_population.items():
    erreur = zC * math.sqrt((f * (1 - f)) / n)
    borne_inf = round(f - erreur, 3)
    borne_sup = round(f + erreur, 3)
    intervalles[opinion] = (borne_inf, borne_sup)

print("\nIntervalles de fluctuation à 95 %")
for opinion, (inf, sup) in intervalles.items():
    print(f"{opinion} : [{inf}, {sup}]")


#Théorie de l'estimation (intervalles de confiance)
print("Résultat sur le calcul d'un intervalle de confiance")

premier_echantillon = donnees.iloc[0]
print(premier_echantillon)
valeurs = list(premier_echantillon)
total = sum(valeurs)
print(total)

#calcul des fréquences
print("Résultat du calcul de la fréquence")
frequences_echantillon_1 = {}
for i, col in enumerate(donnees.columns):
    freq= valeurs[i] / total
    frequences_echantillon_1[col] = round(freq, 2)
for opinion, freq in frequences_echantillon_1.items():
    print(f"{opinion}:{freq}")

#calcul de l'intervalle pour chaque opinion
zC = 1.96#95%
n = total
intervalles_confiance = {}

for opinion, f in frequences_echantillon_1.items():
    erreur = zC * math.sqrt((f * (1 - f)) / n)
    borne_inf = round(f - erreur, 3)
    borne_sup = round(f + erreur, 3)
    intervalles_confiance[opinion] = (borne_inf, borne_sup)

print("Intervalle de confiance à 95 % (du premier échantillon)")

for opinion, (inf, sup) in intervalles_confiance.items(): 
    print(f"{opinion} : [{inf}, {sup}]")

#Théorie de la décision (tests d'hypothèse)

print("Théorie de la décision")
print("Résultats du test de shapiro")

from scipy.stats import shapiro

#sii p>0.05 alors loi normale 

data1 = pd.read_csv("data/Loi-normale-Test-1.csv")
data2 = pd.read_csv("data/Loi-normale-Test-2.csv")

serie1 = data1["Test"]
serie2 = data2["Test"]

#test de shapiro
stat1, p1 = shapiro(serie1)
stat2, p2 = shapiro(serie2)
def interpretation_shapiro(p):
    if p > 0.05:
        return "Distribution normale (p > 0.05)"
    else:
        return "Distribution non normale (p < 0.05)"

print(f"Fichier 1 → p = {p1:.4f} → {interpretation_shapiro(p1)}")#résultat arrondi (car trop long sinon)
print(f"Fichier 2 → p = {p2:.4f} → {interpretation_shapiro(p2)}")

#Fin + BONUS 

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 4))

#Fichier 1
plt.subplot(1, 2, 1) 
sns.histplot(serie1, kde=True, color='skyblue', bins=30)
plt.title("Fichier 1 - Loi normale ?")
plt.xlabel("Valeurs")
plt.ylabel("Effectifs")

#Fichier 2
plt.subplot(1, 2, 2)
sns.histplot(serie2, kde=True, color='salmon', bins=30)
plt.title("Fichier 2 - Loi normale ?")
plt.xlabel("Valeurs")
plt.ylabel("Effectifs")

plt.tight_layout()
plt.savefig(f"img/loi_normale.png")
plt.show()

#BONUS (explication dans le rapport)
