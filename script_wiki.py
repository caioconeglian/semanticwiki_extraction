import sparql_methods
from collections import Counter
from extraction_class import ExtractionFromWiki as Extraction


def testCategories(uri, query):
    #exemplo script_wiki.testCategories('https://en.wikipedia.org/w', 'Dilma_Rousseff')
    extraction = Extraction (uri, query)
    categories = extraction.find_categories()

    entitiescat = []   
    sujeitos = []
    for category in categories:
        sujeitos = sparql_methods.findEntitiesCategory(category, sujeitos)
    print(Counter(sujeitos).most_common(10))

    return "sujeitos"

def testDbpediaSpot(uri, query, dbpedia_boolean, wikidata_boolean):
    """esse método irá extrair dá pagina wiki os 20 conceitos mais comuns e obter as propriedades delas"""
    #exemplo script_wiki.testDbpediaSpot('https://en.wikipedia.org/w', 'Dilma_Rousseff', True, True)
    extraction = Extraction (uri, query)
    list_resource = extraction.find_concepts_spot()

    list_20 = Counter(list_resource).most_common(20)
   
    """está ok, só tirei para fazer outros testes"""
    triples_dbpedia_wikidata = sparql_methods.findAllTriplesRelated(list_20, dbpedia_boolean, wikidata_boolean)

    return triples_dbpedia_wikidata


if __name__ == "__main__":
    testDbpediaSpot('https://en.wikipedia.org/w', 'Dilma_Rousseff', True, True)