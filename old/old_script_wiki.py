import urllib3
import requests
import teste
import xml.etree.ElementTree as ET
from collections import Counter
from extraction_class import ExtractionFromWiki as Extraction
"""
def getTextWiki(query):
    #Test NODO
    #http://plataformanodos.org/
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    #response = http.request('POST', "https://en.wikipedia.org/w/index.php?title=Special:Export&pages="+query+"&curonly=true")
    #response = http.request('POST', "http://plataformanodos.org/index.php?title=Especial:Exportar&pages=El_Tartufo_de_Moli%C3%A8re&curonly=true")
    #response = http.request('POST', "https://eu4.paradoxwikis.com/index.php?title=Special:Export&pages=English_Civil_War&curonly=true")
    #response = http.request('POST', "https://eu4.paradoxwikis.com/index.php?title=Special:Export&pages=England&curonly=true")
    #response = http.request('POST', "http://awful-movies.wikia.com/index.php?title=Special:Export&pages=Batman_v_Superman:_Dawn_of_Justice&curonly=true")
    
    if response:
        root = ET.fromstring(response.data)
        print(root.text)
        el1 = root.find('{http://www.mediawiki.org/xml/export-0.10/}page').find('{http://www.mediawiki.org/xml/export-0.10/}revision').find('{http://www.mediawiki.org/xml/export-0.10/}text')
        print(el1.text)

    return el1.text
"""

"""def findCategoriesWiki(wikitext):
    listterms = []
    while True:
        start = wikitext.find('[[Category')
        wikitext = wikitext[start:]
        end = wikitext.find(']]')
        print(start)
        print(end)
        if start == -1:
            break
        newstring = wikitext[11:end]
        print(newstring)
        listterms.append(newstring)
        wikitext = wikitext[end:]
    return listterms
"""

"""def findConceptsSpot(texttoprocess,list_resource):
    #req = requests.get("http://model.dbpedia-spotlight.org/en/annotate?text=President%20Michelle%20Obama%20called%20Thursday%20on%20Congress%20to%20extend%20a%20tax%20break%20for%20students%20included%20in%20last%20year%27s%20economic%20stimulus%20package,%20arguing%20that%20the%20policy%20provides%20more%20generous%20assistance.&confidence=0.2&support=20")
    req = requests.get("http://model.dbpedia-spotlight.org/en/annotate?text="+texttoprocess+"&confidence=0.8&support=20")
    text_full = ET.fromstring(req.text)
    try:
        resources_xml = text_full.find('Resources').findall('Resource')
        #list_resource = []
        for resource_xml in resources_xml:
            list_resource.append(resource_xml.get('URI'))
    except:
        print('no resource')
    return list_resource
"""

"""def removeStopWords(list_resource):
    while 'http://dbpedia.org/resource/Hypertext_Transfer_Protocol' in list_resource: list_resource.remove('http://dbpedia.org/resource/Hypertext_Transfer_Protocol')
    while 'http://dbpedia.org/resource/Uniform_Resource_Locator' in list_resource: list_resource.remove('http://dbpedia.org/resource/Uniform_Resource_Locator')
    while 'http://dbpedia.org/resource/Citation' in list_resource: list_resource.remove('http://dbpedia.org/resource/Citation')
    while 'http://dbpedia.org/resource/World_Wide_Web' in list_resource: list_resource.remove('http://dbpedia.org/resource/World_Wide_Web')
    while 'http://dbpedia.org/resource/HTTPS' in list_resource: list_resource.remove('http://dbpedia.org/resource/HTTPS')
    while 'http://dbpedia.org/resource/December' in list_resource: list_resource.remove('http://dbpedia.org/resource/December')
    while 'http://dbpedia.org/resource/November' in list_resource: list_resource.remove('http://dbpedia.org/resource/November')
    while 'http://dbpedia.org/resource/October' in list_resource: list_resource.remove('http://dbpedia.org/resource/October')
    while 'http://dbpedia.org/resource/September' in list_resource: list_resource.remove('http://dbpedia.org/resource/September')
    while 'http://dbpedia.org/resource/August' in list_resource: list_resource.remove('http://dbpedia.org/resource/August')
    while 'http://dbpedia.org/resource/July' in list_resource: list_resource.remove('http://dbpedia.org/resource/July')
    while 'http://dbpedia.org/resource/June' in list_resource: list_resource.remove('http://dbpedia.org/resource/June')
    while 'http://dbpedia.org/resource/May' in list_resource: list_resource.remove('http://dbpedia.org/resource/May')
    while 'http://dbpedia.org/resource/April' in list_resource: list_resource.remove('http://dbpedia.org/resource/April')
    while 'http://dbpedia.org/resource/March' in list_resource: list_resource.remove('http://dbpedia.org/resource/March')
    while 'http://dbpedia.org/resource/February' in list_resource: list_resource.remove('http://dbpedia.org/resource/February')
    while 'http://dbpedia.org/resource/January' in list_resource: list_resource.remove('http://dbpedia.org/resource/January')
    while 'http://dbpedia.org/resource/HTML' in list_resource: list_resource.remove('http://dbpedia.org/resource/HTML')
    while 'http://dbpedia.org/resource/Website' in list_resource: list_resource.remove('http://dbpedia.org/resource/Website')
    while 'http://dbpedia.org/resource/File_sharing' in list_resource: list_resource.remove('http://dbpedia.org/resource/File_sharing')
    while 'http://dbpedia.org/resource/Case_citation' in list_resource: list_resource.remove('http://dbpedia.org/resource/Case_citation')
    while 'http://dbpedia.org/resource/Pacific_Time_Zone' in list_resource: list_resource.remove('http://dbpedia.org/resource/Pacific_Time_Zone')
    #while '' in list_resource: list_resource.remove('')
    return list_resource"""


def testCategories(uri, query):
    extraction = Extraction (uri, query)
    categories = extraction.find_categories()

    entitiescat = []   
    sujeitos = []
    for category in categories:
        sujeitos = teste.findEntitiesCategory(category, sujeitos)
    print(Counter(sujeitos).most_common(10))

    return "sujeitos"

def testDbpediaSpot(uri, query):
    #exemplo script_wiki.testDbpediaSpot('https://en.wikipedia.org/w', 'Dilma_Rousseff')
    extraction = Extraction (uri, query)
    list_resource = extraction.find_concepts_spot()
    print(Counter(list_resource).most_common(30))
   
    """está ok, só tirei para fazer outros testes
    triples = []

    for subject in list_subjects:
        triples.append(teste.findInformationEntity(subject))

    print('Only test')
    print('S: '+triples[0][0]['subject']+'\nP: '+triples[0][0]['property']+'\nO: '+triples[0][0]['object'])"""

    return "list_resource"