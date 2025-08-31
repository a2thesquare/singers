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
