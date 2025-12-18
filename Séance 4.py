#coding:utf8

import pandas as pd
import scipy
import scipy.stats as stats 
import numpy as np


#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']
#print(dist_names)

#Question 1 (partie 1) : visualisation dans le terminal

#variables discrètes

valeur_dirac = 5 #loi de dirac (=valeur absolue)
echantillon_dirac = np.full(10, valeur_dirac)
print("Loi de Dirac:", echantillon_dirac)

echantillon_uniforme_discret = stats.randint.rvs(1, 7, size=10)#loi uniforme discrète (dé de 6)
print("Loi uniforme discrète", echantillon_uniforme_discret)

echantillon_binomiale = stats.binom.rvs(n=15, p=0.6, size=10)#loi binomiale
print("Loi binomiale", echantillon_binomiale)

echantillon_poisson = stats.poisson.rvs(mu=5, size=10)
print("Loi du poisson", echantillon_poisson)

echantillon_zipf= stats.zipf.rvs(a=4, size=10)
print("Loi de Zipf-Mandelbrot", echantillon_zipf)

#variables continues

echantillon_poisson = stats.poisson.rvs(mu=5, size=1000)
print("Loi du Poisson", echantillon_poisson)

echantillon_normale = stats.norm.rvs(loc=0, scale=1, size=1000)
print("Loi Normale", echantillon_normale)

echantillon_lognormale = stats.lognorm.rvs(s=0.5, size=1000)
print("Loi Lognormale", echantillon_lognormale[:10])

echantillon_uniforme = stats.uniform.rvs(0, 1, size=1000)
print("Loi Uniforme", echantillon_uniforme[:10])

echantillon_chi2 = stats.chi2.rvs(df=3, size=1000)
print("Loi X²", echantillon_chi2[:10])

echantillon_pareto = stats.pareto.rvs(b=3, size=1000)
print("Loi de Pareto", echantillon_pareto[:10])

#Question 2 : fonctions math pour calculer la moyenne et l'écart type 

def ma_moyenne(data):
    """calcule la moyenne d'une liste ou d'un tableau"""
    return sum(data) / len(data)

def mon_ecart_type(data):
    """calcul de l'écart-type """
    m = ma_moyenne(data)
    variance = sum((x-m)**2 for x in data) / len(data)
    return variance ** 0.5

distributions = {
    "Poisson": echantillon_poisson,
    "Normale": echantillon_normale,
    "Log-normale": echantillon_lognormale,
    "X²": echantillon_chi2,
    "Uniforme": echantillon_uniforme,
    "Pareto": echantillon_pareto,
    "Dirac": echantillon_dirac,
    "Uniforme discrète": echantillon_uniforme_discret,
    "Binomale": echantillon_binomiale,
    "Zipf-Mandelbrot": echantillon_zipf
    }
for nom, data in distributions.items(): 
    moyenne_calculee = ma_moyenne(data)
    ecart_calcule = mon_ecart_type(data)

#Question 1 (Partie 2): visualisation graphique des différentes lois

import matplotlib.pyplot as plt
import os

os.makedirs("img_lois", exist_ok=True)

for nom, data in distributions.items():
    plt.figure()

    if nom == "Dirac":
        plt.axvline(data[0], linewidth=3)
        plt.title("Loi de Dirac (valeur unique)")
        plt.xlabel("Valeur")
        plt.ylabel("Fréquence")

    elif nom == "Zipf-Mandelbrot":
        valeurs_uniques, effectifs = np.unique(data, return_counts=True)
        plt.bar(valeurs_uniques, effectifs)
        plt.yscale('log')
        plt.title("Loi de Zipf-Mandelbrot (log-échelle)")
        plt.xlabel("Valeurs")
        plt.ylabel("Effectifs (log)")

    elif nom in ["Uniforme discrète", "Binomale", "Poisson"]:
        valeurs_uniques, effectifs = np.unique(data, return_counts=True)
        plt.bar(valeurs_uniques, effectifs)
        plt.title(f"{nom} (loi discrète)")
        plt.xlabel("Valeurs")
        plt.ylabel("Effectifs")

    else:
        x = np.linspace(min(data), max(data), 500)
        if nom == "Normale":
            pdf = stats.norm.pdf(x, np.mean(data), np.std(data))
        elif nom == "Log-normale":
            pdf = stats.lognorm.pdf(x, s=0.5)
        elif nom == "Uniforme":
            pdf = stats.uniform.pdf(x)
        elif nom == "X²":
            pdf = stats.chi2.pdf(x, df=3)
        elif nom == "Pareto":
            pdf = stats.pareto.pdf(x, b=3)
        else:
            continue
        
        plt.plot(x, pdf)
        plt.title(f"{nom} (loi continue)")
        plt.xlabel("x")
        plt.ylabel("densité")

    plt.tight_layout()
    plt.savefig(f"img_lois/{nom.replace(' ', '_')}.png")
    plt.close()
