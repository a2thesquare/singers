#### Nombre d'individus dans cette population
`
SELECT (COUNT(?person) AS ?count)
WHERE {
  ?person wdt:P31 wd:Q5;        # instance of human
          wdt:P106 wd:Q177220.  # occupation: singer
}
`
#### Selection des variables importantes
`
SELECT ?person ?personLabel ?dob ?pobLabel ?countryLabel ?sexLabel ?genreLabel
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P106 wd:Q177220.   # occupation: singer
  
  OPTIONAL { ?person wdt:P569 ?dob. }       # date of birth
  OPTIONAL { ?person wdt:P19 ?pob. }        # place of birth
  OPTIONAL { ?person wdt:P27 ?country. }    # country of citizenship
  OPTIONAL { ?person wdt:P21 ?sex. }        # sex or gender
  OPTIONAL { ?person wdt:P136 ?genre. }     # musical genre
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 200
`
