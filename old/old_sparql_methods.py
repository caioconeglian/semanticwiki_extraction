import urllib3
from bs4 import BeautifulSoup
from SPARQLWrapper import SPARQLWrapper, JSON

def findEntity(query):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?entity 
        WHERE { ?entity rdfs:label \""""+query+"""\"@en.
               
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wikidata = "Not found"

    count = 0
    for result in results["results"]["bindings"]:
        if(count==0):
            wikidata = result["entity"]["value"]        

    return wikidata


def findEntityWikidataWithDbpedia(entity_dbpedia):
    """with the dbpedia entity find the wikidata entity"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    querysparql="""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?entity 
        WHERE { 
            <"""+entity_dbpedia+""" owl:sameAs ?entity
            FILTER ( strstarts(str(?a), "http://www.wikidata.org/entity") )   
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #sujeitos = []
    count = 0
    for result in results["results"]["bindings"]:
        
        try:
            sujeitos.append(result["entity"]["value"])
            count=count+1
        except:
            print('erro')      

    return sujeitos


def findEntitiesCategory(category, sujeitos):
    """only work with dbpedia"""
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?sujeitos 
        WHERE { ?category rdfs:label \""""+category+"""\"@en.
            ?sujeitos dct:subject ?category

               
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #sujeitos = []
    count = 0
    for result in results["results"]["bindings"]:
        
        try:
            sujeitos.append(result["sujeitos"]["value"])
            count=count+1
        except:
            print('erro')      

    return sujeitos


def findTriplesEntity(entity, option):
    """ option 1 --> Dbpedia 
        option 2 --> Wikidata"""
    url_dataset = ''
    if option ==1:
        url_dataset = 'http://dbpedia.org/sparql'
    elif option ==2:
        url_dataset = 'https://query.wikidata.org/sparql'
    else:
        return []

    sparql = SPARQLWrapper(url_dataset)
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?p ?o 
        WHERE { 
            <"""+entity+"""> ?p ?o.
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    triples = []
    for result in results["results"]["bindings"]:
        triple = {}
        try:
            triple['subject'] = entity
            triple['property'] = result["p"]["value"]
            triple['object'] = result["o"]["value"]
            triples.append(triple)
        except:
            print('erro')      

    return triples



def findProperties(entity):
    """an example about how to find properties in wikidata"""
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?instance ?date_birth
        WHERE { <"""+entity+"""> wdt:P31 ?instance;
                                 wdt:P569 ?date_birth
               
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    instance = "Not found"
    date_birth = "Not found"

    count = 0
    for result in results["results"]["bindings"]:
        if(count==0):
            instance = result["instance"]["value"] 
            date_birth = result["date_birth"]["value"]       
    values = {'instance': instance, 'date_birth': date_birth}
    return values

    
def consultar(query):
    #query = 'Dilma Rousseff'

    entity = findEntity(query)
    properties = findProperties(entity)
    print(properties['instance'])
    print(properties['date_birth'])
    
    return entity


def findAllTriplesRelated(list_counter, dbpedia_boolean, wikidata_boolean):
    """
    list_counter --> only list from counter. Ex: Counter({'<concept1>': 2, '<concept2>': 1})
    """
    triples_dbpedia = []
    triples_wikidata = []
    for subject in list_counter:
        if dbpedia_boolean:
            triples_dbpedia.append(findTriplesEntity(subject[0]), 1)
        if wikidata_boolean:
            entity_wikidata = findEntityWikidataWithDbpedia(subject[0])
            triples_wikidata.append(findTriplesEntity(entity_wikidata), 2)

    results = {'triples_dbpedia':triples_dbpedia, 'triples_wikidata': triples_wikidata}

    return results
