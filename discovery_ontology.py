from SPARQLWrapper import SPARQLWrapper, JSON


def findEntityOntologySparql(term, uri_sparql_ontology):
    """find the entity with this label"""
    #term = 'horse mussels'
    uri_sparql_ontology = 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc'
    sparql = SPARQLWrapper(uri_sparql_ontology)
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?entity ?p ?o
        WHERE { 
         OPTIONAL{
            ?entity skos:prefLabel '"""+term+"""'@en.
            }
          OPTIONAL{
            ?entity skos:altLabel '"""+term+"""'@en.
            }
               
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    term_uri = 'not found'

    count = 0
    for result in results["results"]["bindings"]:
        term_uri = result["entity"]["value"]

    return term_uri


def findTermsSynonymous(entity, uri_sparql_ontology):
    uri_sparql_ontology = 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc'
    sparql = SPARQLWrapper(uri_sparql_ontology)
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?o1
        WHERE {
        {
         <"""+entity+"""> skos:prefLabel ?o1.
               
               FILTER (lang(?o1) = 'en')
        }UNION
        {
         <"""+entity+"""> skos:prefLabel ?o1.
               
               FILTER (lang(?o1) = 'pt')
        }UNION
        {
         <"""+entity+"""> skos:prefLabel ?o1.
               
               FILTER (lang(?o1) = 'es')
        }UNION
        { 
         <"""+entity+"""> skos:altLabel ?o1.
               
               FILTER (lang(?o1) = 'en')
        }UNION
        { 
         <"""+entity+"""> skos:altLabel ?o1.
               
               FILTER (lang(?o1) = 'pt')
        }UNION
        { 
         <"""+entity+"""> skos:altLabel ?o1.
               
               FILTER (lang(?o1) = 'es')
        } 
        
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    terms = []

    for result in results["results"]["bindings"]:
        terms.append(result["o1"]["value"])


    return terms



def findTermsRelated(entity, uri_sparql_ontology):
    uri_sparql_ontology = 'http://202.45.139.84:10035/catalogs/fao/repositories/agrovoc'
    sparql = SPARQLWrapper(uri_sparql_ontology)
    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?o1
        WHERE {
         <"""+entity+"""> skos:narrower ?o1.
        
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    terms = []

    for result in results["results"]["bindings"]:
        triple = {}
        triple['property'] = 'skos:narrower'
        triple['object'] = result["o1"]["value"]
        terms.append(triple)

    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?o1
        WHERE {
         <"""+entity+"""> <http://aims.fao.org/aos/agrontology#includes> ?o1.
        
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    for result in results["results"]["bindings"]:
        triple = {}
        triple['property'] = '<http://aims.fao.org/aos/agrontology#includes>'
        triple['object'] = result["o1"]["value"]
        terms.append(triple)


    querysparql="""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?o1
        WHERE {
         <"""+entity+"""> <http://aims.fao.org/aos/agrontology#makeUseOf> ?o1.
        
        }"""
    print(querysparql)
    sparql.setQuery(querysparql)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()



    for result in results["results"]["bindings"]:
        triple = {}
        triple['property'] = '<http://aims.fao.org/aos/agrontology#makeUseOf>'
        triple['object'] = result["o1"]["value"]
        terms.append(triple)


    return terms