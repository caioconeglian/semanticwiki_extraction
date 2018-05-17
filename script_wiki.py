import sparql_methods
from collections import Counter
from extraction_class import ExtractionFromWiki as Extraction
from extraction_class import SpotlightQuery
import discovery_ontology


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

    list_20 = extraction.find_most_commons_conpects_spot(20)
   
    """está ok, só tirei para fazer outros testes"""
    triples_dbpedia_wikidata = sparql_methods.findAllTriplesRelated(list_20, dbpedia_boolean, wikidata_boolean)


    """esse aqui é um teste que acha as classes que estão relacionadas a primeira"""
    #entidade = sparql_methods.findEntityDbpedia(query)
    #triples_dbpedia_wikidata = sparql_methods.findTest(list_20, entidade)

    #return triples_dbpedia_wikidata
    return triples_dbpedia_wikidata


def testOntologies(uri, query):
    #script_wiki.testOntologies('https://en.wikipedia.org/w', 'Dilma_Rousseff')
    extraction = Extraction (uri, query)
    list_resource = extraction.find_concepts_spot()
    list_20 = Counter(list_resource).most_common(20)

    list_label = []
    for resource in list_20:
        resource_complete = {}
        resource_complete['name'] = sparql_methods.findLabel(resource[0])
        resource_complete['uri'] = resource[0]
        resource_complete['count'] = resource[1]
        list_label.append(resource_complete)

    return list_label


def testOneTerm(term):
    query_spot = SpotlightQuery(0.2, 20)
    list_resource = []
    list_resource = query_spot.find_resources_spot(term, list_resource)
    uri_resource = list_resource[0]
    name_term = sparql_methods.findLabelDbepdia(uri_resource).lower()
    entity = discovery_ontology.findEntityOntologySparql(name_term,'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc')
    list_resources = discovery_ontology.findTermsSynonymous(entity, 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc')
    outros_termos = discovery_ontology.findTermsRelated(entity, 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc')
    return outros_termos


if __name__ == "__main__":
    testDbpediaSpot('https://en.wikipedia.org/w', 'Dilma_Rousseff', True, True)