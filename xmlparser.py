import xml.parsers.expat
import xml.etree.ElementTree

import datetime
import optparse

def main():
    usage = """
        usage: %prog [options] <input file>
    """
    
    parser = optparse.OptionParser(usage)
    parser.add_option("-m", dest="medline", action="store_true", default=False, help="MEDLINE XML [default: EndNote XML]")

    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error("No input file specified")

    f = open(args[0])
    xmldata = f.read()
    f.close()

    if options.medline:
        xp = MedlineXMLParser(xmldata)
        elements = xp.process()
        print "%d elements found in '%s'" % (len(elements), args[0])
    else:
        xp = EndnoteXMLParser(xmldata)
        documents = xp.process()
        for k in documents.keys():
            print "%d %s in '%s'" % (len(documents[k]), k, args[0])

class XMLTreeParser(object):
    def __init__(self, xmldata):
        self.xmldata = xmldata
        self.elements = None
    
    def parse(self):
        tree = xml.etree.ElementTree.fromstring(self.xmldata)
        return tree
    
    def process(self):
        raise Exception('this should be implemented in the subclass!')

# TODO: use XMLTreeParser eventually
class XMLParser(object):
    def __init__(self, xmldata):
        self.xmldata = xmldata
        self.skip_elements = []
        self.allowed_elements = []
    
    def parse(self):
        self.skip_elements = self.clean_set(self.skip_elements)
        self.allowed_elements = self.clean_set(self.allowed_elements)
        
        self.xml_elements = []
        self.documents = { 'authors': [], 'keywords': [], 'journals': [] }
        
        self.current_element = None
        
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(self.xmldata, 1)
    
    def process(self):
        raise Exception('this should be implemented in the subclass!')
    
    def clean(self, name):
        return name.lower()
        
    def clean_set(self, nameset):
        return [ n.lower() for n in nameset ]
    
    def start_element(self, name, attrs):
        name = self.clean(name)
        #print 'Start element:', name, attrs
        if name in self.allowed_elements:
            self.current_element = [name, '']
        
    def end_element(self, name):
        name = self.clean(name)
        # print 'End element:', name
        if self.current_element is not None:
            # make sure the current element is the one being ended
            if name == self.current_element[0]:
                if name in self.allowed_elements:
                    self.xml_elements.append(self.current_element)
                    self.current_element = None
        
    def char_data(self, data):
        #print 'Character data:', repr(data)
        if self.current_element is not None:
            self.current_element[1] += data

class MedlineCitation(object):
    def __init__(self, xmldata):
        self.xmldata = xmldata
        self.pmid = xmldata.findtext("PMID")
        xmlarticle = xmldata.find("Article")
        self.journals = []
        self.journals.append(xmlarticle.findtext("Journal/Title"))
        self.journals.append(xmlarticle.findtext("Journal/ISOAbbreviation"))
        self.abstract = xmlarticle.findtext("Abstract/AbstractText")
        if self.abstract is None:
            self.abstract = ''
        self.title = xmlarticle.findtext("ArticleTitle")
        if self.title is None:
            self.title = ''
        self.authors = []
        for a in xmlarticle.findall("AuthorList/Author"):
            if a.get("ValidYN") == "Y":
                self.authors.append(a.findtext("LastName"))
    
    def __repr__(self):
        return u'%s' % (self.pmid)

class MedlineXMLParser(XMLTreeParser):
    def process(self):
        if self.elements is None:
            tree = self.parse()
            self.elements = []
            if tree.find('MedlineCitation'):
                all_articles = tree.findall('MedlineCitation')
            elif tree.find('PubmedArticle'):
                all_articles = tree.findall('PubmedArticle/MedlineCitation')
            else:
                raise Exception("Unsupported Medline XML file format... I can't parse it!")
            for a in all_articles:
                self.elements.append(MedlineCitation(a))
        return self.elements

class EndnoteXMLParser(XMLParser):
    def process(self):
        self.allowed_elements = ['author', 'authors', 'title', 'abstract', 'keyword', 'keywords', 'full-title', 'secondary-title', 'secondary_title']
        self.parse()
        for e in self.xml_elements:
            if e[0] in ('author', 'authors'):
                self.documents['authors'].append(e[1])
            elif e[0] in ('title', 'abstract', 'keyword', 'keywords'):
                self.documents['keywords'].append(e[1])
            elif e[0] in ('secondary-title', 'secondary_title', 'full-title'):
                if e[1].lower().find('submit') < 0:
                    #ignore duplicates...
                    if e[1] not in self.documents['journals']:
                        self.documents['journals'].append(e[1])
        return self.documents

if __name__ == '__main__':
    main()
