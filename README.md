#  Broader Named Entity Identification and Linking

## About

The purpose of this script is to assign ontology classes from DBpedia to
word in text corpus. Text corpus must be in Engligh because we use nltk for removing English stopwords from corpus.

Libraries used are:
- SPARQLWrapper - writing SPARQL queries
- nltk - text sanitazation and tokenization
- rdflib - creating Graph and exporting it to XML format

Ontology classes recognized by script are:
- dbo:Building
- dbo:Animal
- dbo:Person
- dbo:University
- dbo:Organisation

When no classes are avaliable for a token on dbpedia, the class "http://localhost/Other" is assigned.

## Usage:

# Install prerequisites

`pip install SPARQLWrapper nltk rdflib`

# Generate XML graph

```
❯ python main.py
Enter the file name: test.txt
<Graph identifier=N025e13216a2148aabfafc3db6a66faf0 (<class 'rdflib.graph.Graph'>)>
```

Output is saved in triples.xml file.

### Podział prac

| Osoba               | Zadanie                                     | Wykonane           |
| ------------------- | ------------------------------------------- | ------------------ |
| Anna Ciszak         | Wczytanie tekstu źródłowego                 | :heavy_check_mark: |
| Anna Ciszak         | Podzielenie tekstu na słowa kluczowe        | :heavy_check_mark: |
| Bartosz Ciesielczyk | Utworzenie zapytania SPARQL                 | :heavy_check_mark: |
| Bartosz Ciesielczyk | Generowanie "trójek" XML na podstawie grafu | :heavy_check_mark: |