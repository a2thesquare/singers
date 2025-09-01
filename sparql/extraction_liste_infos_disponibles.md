Ce document explique le cheminement pour obtenir une liste de propriétés et valeurs lisibles pour des chanteurs. 

**Objectif:** récuperer toutes les propritétés et valeurs lisibles pour les chanteurs nés après 1801 depuis wikidata, avec les colonnes suivantes: 
- 'p': propriété
- 'propLabel': nom lisible de la propriété
- 'oLabel' : valeur lisible

#### Essai 1) Extraction brute

```sparql
SELECT ?singer ?singerLabel ?property ?propertyLabel ?value ?valueLabel WHERE {
  ?singer wdt:P31 wd:Q5;          # instance of human
          wdt:P106 wd:Q177220;    # occupation: singer
          wdt:P569 ?birthDate.    # date of birth
  FILTER(YEAR(?birthDate) > 1801)

  ?singer ?prop ?value.
  ?property wikibase:directClaim ?prop.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

```
Le résultat était trop lourd et wikidata a retourné "upstream request timeout".

#### Essaie 2) Sélectionner seulement quelques chanteurs choisis alétoirement

```sparql
SELECT ?s ?p ?o
WHERE {
  {
    SELECT ?s
    WHERE {
      ?s wdt:P31 wd:Q177220 .   # ?s est une instance de chanteur
    }
    ORDER BY RAND()
    LIMIT 5                     # ← prends 5 chanteurs aléatoires
  }
  ?s ?p ?o .
}
```
Encore une fois trop lourd, "upstream request timeout"

#### Essaie 3) Un chanteur au hasard + labels
```sparql
SELECT ?s ?sLabel ?pLabel ?o ?oLabel
WHERE {
  {
    SELECT ?s
    WHERE {
      ?s wdt:P31 wd:Q177220 .   # instance of singer
    }
    ORDER BY RAND()
    LIMIT 1                     # ← un seul chanteur
  }
  ?s ?p ?o .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 200   # limite à 200 triplets pour éviter timeout

```
Toujours trop lourd, "upstream request timeout"

#### Essaie 4) Filtrer seulement les propriétés directes
```sparql
SELECT ?s ?sLabel ?propLabel ?value ?valueLabel

WHERE {
  {
    SELECT ?s
    WHERE {
      ?s wdt:P31 wd:Q177220 .
    }
    ORDER BY RAND()
    LIMIT 1    # un chanteur au hasard
  }
  ?s ?prop ?value .
  FILTER(STRSTARTS(STR(?prop), STR(wdt:)))   # seulement propriétés directes
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
```
Meme problème que précédemment.

#### Essai 5) 
Après plusieurs tentatives échouées, notamment à cause de la randomisation (`ORDER BY RAND()`) qui provoquait des timeouts, j’ai choisi de me concentrer sur un artiste les plus connu possible, Michael Jackson (Q2831). Sa page, très documentée, contient de nombreuses propriétés et valeurs différentes, ce qui permet : d’extraire efficacement toutes ses informations (`p`, `propLabel`, `oLabel`) sans surcharger Wikidata, et de s’assurer que le format et la lisibilité des données sont corrects avant d’étendre éventuellement la méthode à d’autres chanteurs.

```sparql
SELECT ?p ?propLabel ?oLabel
WHERE {
  wd:Q2831 ?p ?o .
  FILTER(STRSTARTS(STR(?p), STR(wdt:)))  # seulement propriétés directes

  # récupérer le label lisible de la propriété
  ?property wikibase:directClaim ?p .
  ?property rdfs:label ?propLabel .
  FILTER(LANG(?propLabel) = "fr")

  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "fr,en". 
    ?o rdfs:label ?oLabel .
  }
}
```
Le csv obtenu par cette requète est au lien suivant. 
