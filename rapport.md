
L’objectif de cette étude est d’expérimenter les différentes phases de production et d’analyse de l’information sous forme de données, en appliquant des méthodes de recherche à une population spécifique : les chanteurs et chanteuses nés entre 1801 et 2000.

Le dataset de base a été extrait à l’aide de requêtes SPARQL sur le serveur Wikidata. Initialement, je souhaitais réaliser des requêtes distinctes pour chaque variable (date de naissance, pays d'origine, sexe, genre musical), mais en raison de la taille importante de la population étudiée (environ 200 000 individus), il a fallu procéder autrement : j’ai téléchargé toutes les valeurs d’intérêt simultanément, en segmentant la population par tranches d’années de naissance.
```sql
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1801 && YEAR(?birthDate) < 1850)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate

```
au départ, j’ai utilisé des tranches de 50 ans, puis, à partir de 1950, le nombre de personnes étant beaucoup plus important, j’ai réduit les tranches à 10 ans, et enfin à partir de 1990 à des tranches de 5 ans. Le détail de cette procédure est documenté dans le fichier SPARQL. Ensuite, j’ai utilisé le script Python suivant pour fusionner tous les CSV obtenus en un seul fichier.

---------------------

### 1) Comment evolue le nombre de chanteurs.euses notables nés par decennies ? 
**→ Application de la distribution de variable qualitative avec évolution temporelle**

Pour la partie de l'analyse concernant une distribution de variable qualitative dans le temps, j'ai pris les sexes des différents artistes et distribué. 

```python
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

```python
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

### 2) Existe-il une relation statistiquement importante entre le pays de citoyenneté et le style de musical des chanteurs et chanteuses ? 
**→ Application de l'analyse bivariée**


### 3) Quels genres musicaux sont le plus souvent associés entre eux chez les chanteurs.euses ?
**→ Application de l'analyse de réseaux**
```python
import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv("combined_singers.csv")

# Filtrer si nécessaire, par exemple uniquement pour les pays les plus représentés
top_countries = df['citizenshipLabel'].value_counts().nlargest(10).index
df_filtered = df[df['citizenshipLabel'].isin(top_countries)]

# Table de contingence
contingency = pd.crosstab(df_filtered['citizenshipLabel'], df_filtered['genreLabel'])
#print(contingency)


chi2, p, dof, expected = chi2_contingency(contingency)
print(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}")
```
**Resultat: Chi2 = 93652.10, p-value = 0.0000**
La valeur de Chi2 très élevée indique qu'il existe un écart important entre les effectifs observés et les effectifs attendus sous l'hypothèse d'indépendance. La p-value proche de 0 signifie que cet écart est hautement significatif, donc on peut rejeter l'hypothese nulle. La conclusion statistique est que il existe une assocaition significative entre le pays et citoyenneté et le style musical. Autrement dit, certains styles musicauy sont plus fréquents dans certains pays. Pour mieux comprendre, je vous propose le heatmap suivant:
## Discussion

## Conclusion
