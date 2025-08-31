# Analyse des chanteurs de Wikipedia
Ce travail vise à expérimenter les différentes étapes de production et d’analyse de données, en appliquant des méthodes de recherche à une population spécifique : les chanteurs et chanteuses nés entre 1801 et 2000.

**Questions de recherche :**

1) Comment le nombre de chanteurs et chanteuses notables a-t-il évolué au fil des décennies ?
2) Existe-t-il une relation statistiquement significative entre le pays de citoyenneté et le style musical ?
3) Quels genres musicaux apparaissent le plus souvent associés chez les chanteurs et chanteuses ?
   
Au départ, ce travail devait être réalisé sur la population de grimpeurs, en suivant la méthode proposée par l’enseignant (repository au [lien suivant](https://github.com/a2thesquare/Grimpeurs). Après de nombreux essais et plusieurs heures de travail, j’ai décidé de recommencer à zéro en choisissant une autre population et une méthode que je comprenais mieux, tout en utilisant autant que possible les outils demandés.

La multiplicité des documents et l’organisation des données m’avaient perdue, et je ne comprenais ni les requêtes ni les notebooks Jupyter. En appliquant une méthode plus originale, j’ai pu mieux apprendre et comprendre le processus, en espérant avoir atteint le résultat attendu.

-------------------------------

## Extraction des données

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
Au départ, j’ai utilisé des tranches de 50 ans, puis, à partir de 1950, le nombre de personnes étant beaucoup plus important, j’ai réduit les tranches à 10 ans, et enfin à partir de 1990 à des tranches de 5 ans. Le détail de cette procédure est documenté dans le fichier SPARQL. Ensuite, j’ai utilisé le script Python suivant pour fusionner tous les CSV obtenus en un seul document.

```python
import pandas as pd
import glob

csv_files = glob.glob("/Users/angelikiandreadi/Library/CloudStorage/OneDrive-unine.ch/Unine/Semestre_4/Environnement_Python/csv_dates_naissance/*.csv")
print(csv_files)

dfs = [pd.read_csv(f) for f in csv_files]
combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv("/Users/angelikiandreadi/Downloads/combined_singers.csv", index=False)
```
-----------------------------
## Base de données RDF
La base de données RDF demandée a été obtenue en transformant le CSV original en RDF à l’aide d’un script Python fourni par ChatGPT, car cette opération dépasse actuellement mes compétences. Le fichier généré est disponible au lien suivant, et le script utilisé est :

```python
import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace

df = pd.read_csv("combined_singers.csv")  
g = Graph()
EX = Namespace("http://example.org/")  

for idx, row in df.iterrows():
    sujet = URIRef(f"http://example.org/ligne{idx}")
    for col in df.columns:
        g.add((sujet, EX[col], Literal(row[col])))

g.serialize("wikidata.rdf", format="turtle")
```
Cependant, lors de la tentative d’import de ce fichier dans AllegroGraph, l’application a renvoyé l’erreur « Restricted Access Mode ». Après recherche, la seule solution disponible semble être de télécharger AllegroGraph Desktop, ce qui permet un usage local mais ne répond pas à l’objectif initial consistant à disposer d’un serveur RDF en ligne.

---------------------
## Questions de recherche
### 1) Comment evolue le nombre de chanteurs.euses notables nés par decennies ? 
**→ Application de la distribution de variable qualitative avec évolution temporelle**

Pour l’analyse de la distribution d’une variable qualitative dans le temps, j’ai retenu le sexe des artistes et étudié son évolution décennie par décennie. J'ai retenu uniquement les sexes "male" and "female" pour simplifier la tache. 

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

On observe que le nombre de chanteuses augmente progressivement des années 1800 à 1910, puis de façon plus marquée jusqu’aux années 1980, où il atteint un pic avant de diminuer légèrement. Cette évolution pourrait reflèter l’essor des opportunités pour les femmes dans la musique, l’industrialisation de l’industrie musicale et les changements socioculturels favorisant leur visibilité. Cependant, cette représentation seule ne permet pas de comparer correctement les époques, car elle ne tient pas compte du nombre total de chanteurs. Une analyse plus pertinente consiste à examiner les proportions d’hommes et de femmes par décennie, comme dans le graphique suivant.

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

--------------------------------

### 2) Existe-il une relation statistiquement importante entre le pays de citoyenneté et le style musical des chanteurs et chanteuses ? 
**→ Application de l'analyse bivariée**

Pour l’analyse bivariée de variables qualitatives, j’ai retenu le pays de citoyenneté et le style musical des artistes, afin d’examiner si le style pratiqué est lié à la localisation géographique (en supposant que les artistes chantent dans leur pays d’origine) et d’identifier les préférences musicales dans les pays les plus représentés, grace au test de chi^2. 

```python
import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv("combined_singers.csv")

# Filtrer si nécessaire, par exemple uniquement pour les pays les plus représentés
top_countries = df['citizenshipLabel'].value_counts().nlargest(10).index
df_filtered = df[df['citizenshipLabel'].isin(top_countries)]

# Table de contingence
contingency = pd.crosstab(df_filtered['citizenshipLabel'], df_filtered['genreLabel'])
print(contingency)

chi2, p, dof, expected = chi2_contingency(contingency)
print(f"Chi2 = {chi2:.2f}, p-value = {p:.4f}")
```
**Resultat: Chi2 = 93652.10, p-value = 0.0000**

La valeur très élevée du Chi2 indique qu’il existe un écart important entre les effectifs observés et ceux attendus sous l’hypothèse d’indépendance entre le pays de citoyenneté et le style musical. La p-value proche de 0 montre que cet écart est hautement significatif, ce qui permet de rejeter l’hypothèse nulle. Autrement dit, il existe une association statistiquement significative entre le pays et le style musical : certains genres sont beaucoup plus fréquents dans certains pays. Pour illustrer cette association, nous avons construit une heatmap représentant les 10 pays et les 10 genres musicaux les plus fréquents.

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))
sns.heatmap(contingency, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Top 10 Countries vs Top 10 Genres")
plt.ylabel("Country")
plt.xlabel("Genre")
plt.show()
```

<img width="1034" height="765" alt="image" src="https://github.com/user-attachments/assets/181d0090-1e0f-4808-9139-6192bc7ca858" />

On observe que la pop est le style le plus représenté, suivi du rock, tandis que le hip-hop est beaucoup plus marginal. Une forte concentration d’artistes est visible aux États-Unis, où la pop domine largement, suivie par la country. Au Japon, le genre le plus populaire est la J-Pop, ce qui reflète les préférences musicales locales.

Il convient de noter que cette visualisation ne montre que les pays et genres les plus représentés ; certaines tendances moins fréquentes sont donc masquées. Néanmoins, elle permet de comprendre rapidement comment la distribution des styles musicaux varie selon les pays et met en évidence des préférences culturelles distinctes.

AJOUTER QUE PROPORTIONNALITé AURAIT éTé INTERESSANTE 

----------------------------------------

### 3) Quels genres musicaux sont le plus souvent associés entre eux chez les chanteurs.euses ?
**→ Application de l'analyse de réseaux**
Quels genres musicaux sont le plus performés ensembles, pas les memes artistes. Les noeuds sont les styles de musiques, les arretes sont reliées si un artiste appartient aux deux. Cela pourrait nous permettre de voir quels genres musicaux apparaissent souvent ensembles, quels genres sont des ponts, et eventuellement détecter des communcautés de genres. 


```python

# centralité en degré (genres les plus connectés)
deg_cent = nx.degree_centrality(G)

# centralité d’intermédiarité (genres-passerelles)
bet_cent = nx.betweenness_centrality(G, weight="weight")

# trier et afficher les top 10
print("Top 10 degré:")
print(sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10])

print("Top 10 intermédiarité:")
print(sorted(bet_cent.items(), key=lambda x: x[1], reverse=True)[:10])

Top 10 degré:
[('pop music', 1.0, ('rhythm and blues', 1.0), ('jazz', 1.0), ('pop rock', 1.0), ('rock music', 1.0), ('folk music', 1.0), ('hip-hop', 0.9473684210526315), ('reggae', 0.9473684210526315), ('soul', 0.9473684210526315), ('blues', 0.9473684210526315)]

Top 10 intermédiarité:
[('opera', 0.27309941520467834), ('K-pop', 0.26286549707602336), ('hard rock', 0.2218323586744639), ('chanson', 0.188401559454191), ('reggae', 0.17426900584795318), ('indie rock', 0.06374269005847952), ('blues', 0.04434697855750487), ('traditional folk music', 0.04327485380116959), ('J-pop', 0.039473684210526314), ('alternative rock', 0.017738791423001946)]
```

Dans le Top 10 de la centralité en degré, on observe que la majorité des genres (pop, R&B, jazz, rock, folk, etc.) ont une valeur proche de 1, ce qui signifie qu’ils sont connectés à presque tous les autres genres du réseau.

Cela s’explique par le fait que nous avons restreint notre analyse au top 20 des genres les plus fréquents, qui sont donc très souvent co-associés chez les artistes. En d’autres termes, les genres dominants forment un noyau fortement interconnecté, où presque chaque genre est lié aux autres.
Ici, un score de 1 veut dire que le genre est lié à 100 % des autres genres considérés. En revanche, la centralité d’intermédiarité (betweenness) raconte une histoire différente. Le Top 10 met en évidence certains genres qui jouent un rôle de “ponts” stratégiques dans le réseau : Opera (0.27) et K-pop (0.26) apparaissent comme des genres charnières reliant des communautés autrement peu connectées (par exemple, la musique classique ou la musique asiatique moderne vers le réseau principal pop/rock).

Hard rock et chanson remplissent aussi ce rôle de médiateurs entre différents ensembles musicaux. Des genres comme reggae ou blues servent de passerelles entre des familles musicales plus spécialisées (urbain, traditionnel, etc.) et le noyau central pop/rock.
Toutes ce que nous disent ces chiffres peut etre confirmé graçe au shema suivant: 
```python
mport pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

df = pd.read_csv("combined_singers.csv")

# trie les top 20 genres qui apparaissent le plus souvent
top_genres = df["genreLabel"].value_counts().nlargest(20).index
df_top = df[df["genreLabel"].isin(top_genres)]

# regroupe les genres par artiste
artist_genres = df_top.groupby("singerLabel")["genreLabel"].apply(list)

G = nx.Graph()

for genres in artist_genres:
    # Toutes les paires de genres pour cet artiste
    for g1, g2 in combinations(set(genres), 2):  
        if G.has_edge(g1, g2):
            G[g1][g2]["weight"] += 1
        else:
            G.add_edge(g1, g2, weight=1)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=15)  # layout pour la visualisation
edges = nx.draw_networkx_edges(G, pos, alpha=0.3)
nodes = nx.draw_networkx_nodes(G, pos, node_size=500, node_color="orange")
labels = nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Réseau des genres musicaux (basé sur artistes multi-genres)")
plt.axis("off")
plt.show()
```
<img width="1758" height="1256" alt="image" src="https://github.com/user-attachments/assets/0274cfcb-0c8b-45be-bf53-c064957a250c" />

Au départ, j’avais inclus l’ensemble des styles de musique disponibles dans mon schéma. Cependant, le résultat était illisible et ne permettait aucune interprétation. J’ai donc retravaillé plusieurs fois la visualisation jusqu’à parvenir à une version plus lisible, en me concentrant sur les 20 styles de musique les plus représentés.

## Discussion

**Limites:**
- La population étudiée était trop vaste, ce qui a réduit l’utilité de Wikidata et a limité l’usage d’AllegroGraph, qui n’a finalement pas pu être exploité comme prévu.
- Les méthodes employées ont parfois été développées de manière personnelle, cela implique qu’elles n’ont pas été validées par un enseignant et qu’il est possible que d’autres approches plus efficaces existent.
- L’analyse de réseaux aurait pu être approfondie davantage, avec un travail supplémentaire sur la détection de communautés, les poids des liens ou l’évolution temporelle.
  
**Perspectives:**
- L’analyse de réseaux a été une partie particulièrement intéressante et nouvelle pour moi. J’aimerais par la suite explorer comment certains styles gagnent ou perdent en popularité selon les époques, et observer les différents réseaux que cela engendre au fil du temps.

- Pour les artistes plus récents, il serait également pertinent d’étudier les liens avec les maisons de disques : identifier lesquelles sont les plus présentes, si certaines concentrent une majorité d’artistes connus, et comment elles structurent le paysage musical actuel.
  
## Conclusion
En somme, ce projet m’a permis de découvrir de nouvelles méthodes d’analyse tout en mettant en évidence les limites de mes choix techniques. Il ouvre néanmoins de nombreuses pistes futures, tant sur l’étude de l’évolution des genres musicaux que sur l’exploration des réseaux industriels qui structurent le monde de la musique.
