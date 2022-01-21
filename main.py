def main(file_name):
    from SPARQLWrapper import SPARQLWrapper, JSON
    from pprint import pprint
    import nltk
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import string
    import rdflib
    nltk.download("stopwords")
    nltk.download("punkt")
    stop_words = set(stopwords.words("english"))
    table = str.maketrans('', '', string.punctuation)

    i = open(file_name, "r", encoding="utf8")
    text = i.read()
    text = word_tokenize(text)
    text = [w.translate(table) for w in text]
    text = [word for word in text if word.isalpha()]
    text = [w for w in text if not w in stop_words]
    text = [w.capitalize() for w in text]
    pprint(text)

    triples = []

    for word in text:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        SELECT DISTINCT ?obj WHERE{""" +
                        f"<http://dbpedia.org/resource/{word}>  rdf:type ?obj " +
                        "FILTER (strstarts(str(?obj), str(dbo:))) " +
                        "FILTER regex(?obj, \"(Building|Animal|Person|University|Organisation)$\")}")

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results['results']['bindings']:
            triples.extend([(rdflib.term.URIRef(f"http://dbpedia.org/resource/{word}"), rdflib.term.URIRef(
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), rdflib.term.URIRef(v['obj']['value'])) for v in results['results']['bindings']])
        else:
            triples.extend([(rdflib.term.URIRef(f"http://dbpedia.org/resource/{word}"), rdflib.term.URIRef(
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), rdflib.term.URIRef("http://localhost/Other"))])

    g = rdflib.Graph()
    g.bind("dbr", rdflib.namespace.Namespace("http://dbpedia.org/resource/"))
    g.bind("dbo", rdflib.namespace.Namespace("http://dbpedia.org/ontology/"))

    for t in triples:
        g.add(t)

    pprint(g.serialize(destination="triples.xlm", format="xml"))


if __name__ == "__main__":
    import os.path
    filename = input("Enter the file name: ")
    main(filename if os.path.isfile(filename) else "test.txt")
