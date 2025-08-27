## Introduction
L'objectif de ce cet enseignement est d'expérimenter les differentes phases de la production et analyse d'information sous forme de données à partir de questions qu'on a posées.

## Objectifs 
Le but de notre étude est d'appliquer des méthodes de recherche via des questionnements sur une population donnée, dans notre cas, celle des chanteurs/chanteuses.  

### 1) Comment evolue le nombre de chanteurs.euses notables nés par decennies ? → Application de la distribution de variable qualitative avec évolution temporelle
Pour la partie de l'analyse concernant une distribution de variable qualitative dans le temps, j'ai pris les sexes des différents artistes et distribué. 

```
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("combined_singers.csv") # lecture du csv

df['birth_date'] = pd.to_datetime(df['birthDate'], errors='coerce') # conversion en datatime pour pouvoir le traiter comme une date

df['birth_year'] = df['birth_date'].dt.year # extraction de l'année

df['decade'] = (df['birth_year'] // 10) * 10 # calcul de la decennie

df = df[df['genderLabel'].isin(['male', 'female'])] # pour simplification de l'analyse, on prends en compte uniquement les genres male et female

decade_gender_counts = df.groupby(['decade', 'genderLabel'])['singerLabel'].count().unstack(fill_value=0) # decompte des chanteurs par decennie et genres

decade_gender_counts.plot(kind='bar', figsize=(12,6), color=['lightpink', 'skyblue'])

plt.xlabel('Décennie de naissance')
plt.ylabel('Nombre de chanteur.euses')
plt.title('Nombre de chanteurs et de chanteuses par décennie')
plt.xticks(rotation=45)
plt.legend(title='Genre')
plt.tight_layout()
plt.show()
```
<img width="2384" height="1206" alt="image" src="https://github.com/user-attachments/assets/0baa4147-66a9-470a-a9c7-4840d81fd5a9" />

On observe que le nombre de chanteuses augmente progressivement des années 1800 à 1910, puis de façon plus marquée jusqu’aux années 1980, où il atteint un pic avant de diminuer légèrement. Cette évolution reflète l’essor des opportunités pour les femmes dans la musique, l’industrialisation de l’industrie musicale et les changements socioculturels favorisant leur visibilité. Cependant, cette représentation seule ne permet pas de comparer correctement les époques, car elle ne tient pas compte du nombre total de chanteurs. Une analyse plus pertinente consiste à examiner les proportions d’hommes et de femmes par décennie, comme dans le graphique suivant.

```
decade_gender_prop = decade_gender_counts.div(decade_gender_counts.sum(axis=1), axis=0)

decade_gender_prop.plot(kind='bar', figsize=(12,6), color=['lightpink', 'skyblue'])
plt.xlabel('Décennie de naissance')
plt.ylabel('Proportion de chanteurs')
plt.title('Proportion d’hommes et de femmes chanteurs par décennie')
plt.xticks(rotation=45)
plt.legend(title='Genre')
plt.tight_layout()
plt.show()
```
<img width="2384" height="1206" alt="image" src="https://github.com/user-attachments/assets/83c02995-ada2-437e-b6ad-42d26566e4c4" />

Cette fois, on peut distinguer deux périodes de montée significative : la première vers 1860 et la seconde autour de 1980, mettant en évidence l’évolution relative de la représentation féminine dans la musique au fil du temps.

### 2) La répartition des genres musicaux varie-t-elle selon le pays de citoyenneté des chanteurs.euses ?** → Application de l'analyse bivariée
### Analyse de réseaux

### 3) Quels genres musicaux sont le plus souvent associés entre eux chez les chanteurs.euses ?** → Application de l'analyse de réseaux

## Discussion

## Conclusion
