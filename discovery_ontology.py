from SPARQLWrapper import SPARQLWrapper, JSON


def findTermOntologySparql(term, uri_sparql_ontology):
    """find the entity with this label"""
    #term = 'horse mussels'
    uri_sparql_ontology = 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc'
    sparql = SPARQLWrapper(uri_sparql_ontology)
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?entity ?p ?o
        WHERE { ?entity skos:altLabel \""""+term+"""\"@en.

            ?entity ?p ?o.
               
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    list_triple = []

    count = 0
    for result in results["results"]["bindings"]:
        triple = {}
        triple['uri'] = result["entity"]["value"]
        triple['p'] = result["p"]["value"]
        triple['o'] = result["o"]["value"]     
        list_triple.append(triple)   

    return list_triple