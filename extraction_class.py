import urllib3
import requests
import xml.etree.ElementTree as ET

class ExtractionFromWiki:

    def __init__(self, uri_wiki, query):
        """
        uri--> Wiki URI (without plugin) Ex: 'https://en.wikipedia.org/w'
        query --> page name. Ex: 'Dilma_Rousseff'
        """
        self.uri_wiki = uri_wiki
        self.query = query
        self.uri_final = self.uri_wiki+'/index.php?title=Special:Export&pages='+query+'&curonly=true'
        self.textwiki = ''
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        #exemplos wiki funciona
        #response = http.request('POST', "https://en.wikipedia.org/w/index.php?title=Special:Export&pages="+query+"&curonly=true")
        #response = http.request('POST', "http://plataformanodos.org/index.php?title=Especial:Exportar&pages=El_Tartufo_de_Moli%C3%A8re&curonly=true")
        #response = http.request('POST', "https://eu4.paradoxwikis.com/index.php?title=Special:Export&pages=English_Civil_War&curonly=true")
        #response = http.request('POST', "https://eu4.paradoxwikis.com/index.php?title=Special:Export&pages=England&curonly=true")
        #response = http.request('POST', "http://awful-movies.wikia.com/index.php?title=Special:Export&pages=Batman_v_Superman:_Dawn_of_Justice&curonly=true")
        response = http.request('POST', self.uri_final)

        if response:
            root = ET.fromstring(response.data)
            #print(root.text)
            el1 = root.find('{http://www.mediawiki.org/xml/export-0.10/}page').find('{http://www.mediawiki.org/xml/export-0.10/}revision').find('{http://www.mediawiki.org/xml/export-0.10/}text')
            #print(el1.text)
            self.textwiki = el1.text
    

    

    def __remove_stop_words(self, list_resource):
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
        return list_resource


    def find_categories(self):
        """
        return --> a list with all categories of the page
        """
        listterms = []
        text = self.textwiki
        while True:
            start = text.find('[[Category')
            text = text[start:]
            end = text.find(']]')
            #print(start)
            #print(end)
            if start == -1:
                break
            newstring = text[11:end]
            #print(newstring)
            listterms.append(newstring)
            text = text[end:]
        return listterms


    def find_concepts_spot(self):
        """
        return --> a list with URI of the concepts
        """

        text = self.textwiki
        lenwiki = int(len(text)/4000)
        query_spot = SpotlightQuery(0.8, 20)
        list_resource = []
        for i in range(lenwiki+1):
            list_resource = query_spot.find_resources_spot(text[i*4000:(i+1)*4000],list_resource)
        list_resource = self.__remove_stop_words(list_resource)
        return list_resource



class SpotlightQuery:

    def __init__(self, confidence, support):
        self.confidence = confidence
        self.support = support
        

    def find_resources_spot(self, texttoprocess, list_resource):
        print("http://model.dbpedia-spotlight.org/en/annotate?text="+texttoprocess+"&confidence="+str(self.confidence)+"&support="+str(self.support))
        req = requests.get("http://model.dbpedia-spotlight.org/en/annotate?text="+texttoprocess+"&confidence="+str(self.confidence)+"&support="+str(self.support))

        text_full = ET.fromstring(req.text)
        try:
            resources_xml = text_full.find('Resources').findall('Resource')
            #list_resource = []
            for resource_xml in resources_xml:
                list_resource.append(resource_xml.get('URI'))
        except:
            print('no resource')
        return list_resource

