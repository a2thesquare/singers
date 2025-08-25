#### Nombre d'individus dans cette population
```
SELECT (COUNT(?singer) AS ?count) WHERE {
  ?singer wdt:P31 wd:Q5;         # instance of human
          wdt:P106 wd:Q177220;   # occupation: singer
          wdt:P569 ?birthDate.   # date of birth
  FILTER(YEAR(?birthDate) > 1801)
}
```
#### Selection des variables importantes
```
SELECT ?person ?personLabel ?dob ?pobLabel ?countryLabel ?sexLabel ?genreLabel
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P106 wd:Q177220.   # occupation: singer
  
  OPTIONAL { ?person wdt:P569 ?dob. }       # date of birth
  OPTIONAL { ?person wdt:P19 ?pob. }        # place of birth
  OPTIONAL { ?person wdt:P27 ?country. }    # country of citizenship
  OPTIONAL { ?person wdt:P21 ?sex. }        # sex or gender
  OPTIONAL { ?person wdt:P136 ?genre. }     # musical genre
```
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 200
`
#### Il y a enormement d'individus, donc j'ai téléchargé plusieurs csv par tranches d'années de naissance
```
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
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1850 && YEAR(?birthDate) < 1900)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1900 && YEAR(?birthDate) < 1950)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1950 && YEAR(?birthDate) < 1960)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1960 && YEAR(?birthDate) < 1970)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1970 && YEAR(?birthDate) < 1980)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1980 && YEAR(?birthDate) < 1990)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1990 && YEAR(?birthDate) < 1995)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
```
SELECT ?singer ?singerLabel ?birthDate ?birthPlaceLabel ?citizenshipLabel ?genderLabel ?genreLabel WHERE {
  ?singer wdt:P31 wd:Q5;           # instance of human
          wdt:P106 wd:Q177220;     # occupation: singer
          wdt:P569 ?birthDate.     # date of birth
  FILTER(YEAR(?birthDate) >= 1995 && YEAR(?birthDate) < 2000)

  OPTIONAL { ?singer wdt:P19 ?birthPlace. }       # place of birth
  OPTIONAL { ?singer wdt:P27 ?citizenship. }      # country of citizenship
  OPTIONAL { ?singer wdt:P21 ?gender. }           # sex or gender
  OPTIONAL { ?singer wdt:P136 ?genre. }           # musical genre

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY ?birthDate
```
