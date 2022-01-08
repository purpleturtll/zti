from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import string
import rdflib
nltk.download("stopwords")
nltk.download("punkt")
stop_words = set(stopwords.words("english"))
table = str.maketrans('', '', string.punctuation)

text = "We left in pretty good time, and came after nightfall to Klausenburgh. Here I stopped for the night at the Hotel Royale. I had for dinner, or rather supper, a chicken done up some way with red pepper, which was very good but thirsty Horse."

text = word_tokenize(text)
text = [w.translate(table) for w in text]
text = [word for word in text if word.isalpha()]
text = [w for w in text if not w in stop_words]
text = [w.capitalize() for w in text]
pprint(text)

result = []

triples = []

for word in text:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbr: <http://dbpedia.org/resource>
PREFIX dbo: <http://dbpedia.org/ontology>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?obj WHERE{""" +
f"<http://dbpedia.org/resource/{word}>  rdf:type ?obj " +
"FILTER strstarts(str(?obj), str(dbo:))}")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    triples.extend([(rdflib.term.URIRef(f"http://dbpedia.org/resource/{word}"), rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), rdflib.term.URIRef(v['obj']['value'])) for v in results['results']['bindings']])

g = rdflib.Graph()
g.bind("dbr", rdflib.namespace.Namespace("http://dbpedia.org/resource/"))
g.bind("dbo", rdflib.namespace.Namespace("http://dbpedia.org/ontology/"))

for t in triples:
    g.add(t)

print(g.serialize(destination="triples.xlm", format="xml"))
