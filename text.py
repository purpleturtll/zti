from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    ASK WHERE { 
        <http://dbpedia.org/resource/Asturias> rdfs:label "Asturias"@es
    }    
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)
