import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("combined_singers.csv")
# Filter top countries and top genres
top_countries = df['citizenshipLabel'].value_counts().nlargest(10).index
top_genres = df['genreLabel'].value_counts().nlargest(10).index

df_filtered = df[df['citizenshipLabel'].isin(top_countries) & df['genreLabel'].isin(top_genres)]

# Contingency table
contingency = pd.crosstab(df_filtered['citizenshipLabel'], df_filtered['genreLabel'])

# Plot heatmap
plt.figure(figsize=(12,8))
sns.heatmap(contingency, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Top 10 Pays vs Top 10 Genres")
plt.ylabel("Pays")
plt.xlabel("Genre")
plt.show()
