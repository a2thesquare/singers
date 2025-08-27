## Introduction
L'objectif de ce cet enseignement est d'expérimenter les differentes phases de la production et analyse d'information sous forme de données à partir de questions qu'on a posées.

### Objectifs 
Le but de notre étude est d'appliquer des méthodes de recherche via des questionnements sur une population donnée, dans notre cas, celle des chanteurs/chanteuses. 

**2) La répartition des genres musicaux varie-t-elle selon le pays de citoyenneté des chanteurs.euses ?** → Application de l'analyse bivariée

**3) Quels genres musicaux sont le plus souvent associés entre eux chez les chanteurs.euses ?** → Application de l'analyse de réseaux 


## Résultats et analyses 
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
![Chanteurs.euses par décennies](<img width="2384" height="1206" alt="image" src="https://github.com/user-attachments/assets/86d451a6-62ca-4af6-98c1-de0778f49b32" />
)
### Analyse bivariée
### Analyse de réseaux

## Discussion

## Conclusion
