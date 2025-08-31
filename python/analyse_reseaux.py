import pandas as pd
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

# centralité en degré (genres les plus connectés)
deg_cent = nx.degree_centrality(G)

# centralité d’intermédiarité (genres-passerelles)
bet_cent = nx.betweenness_centrality(G, weight="weight")

# trier et afficher les top 10
print("Top 10 degré:")
print(sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10])

print("Top 10 intermédiarité:")
print(sorted(bet_cent.items(), key=lambda x: x[1], reverse=True)[:10])
