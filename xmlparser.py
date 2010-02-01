import xml.parsers.expat
from xml.etree.ElementTree import ElementTree

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

    if options.medline:
        xp = MedlineXMLParser(args[0])
        xp.process()
    else:
        xp = EndnoteXMLParser(args[0])
        xp.process()

class XMLTreeParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.skip_elements = []
        self.allowed_elements = []
    
    def parse(self):
        tree = ElementTree()
        tree.parse(self.filename)
        return tree

class XMLParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.skip_elements = []
        self.allowed_elements = []
    
    def parse(self):
        self.skip_elements = self.clean_set(self.skip_elements)
        self.allowed_elements = self.clean_set(self.allowed_elements)
        
        self.elements = []
        self.documents = { 'authors': [], 'keywords': [], 'journals': [] }
        
        self.current_element = None
        self.depth = 1
        
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        
        f = open(self.filename, 'r')
        p.Parse(f.read(), 1)
        f.close()
    
    def process(self):
        pass
    
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
                    self.elements.append(self.current_element)
                    self.current_element = None
        
    def char_data(self, data):
        #print 'Character data:', repr(data)
        if self.current_element is not None:
            self.current_element[1] += data

class MedlineArticle(object):
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
        # self.allowed_elements = ['title', 'isoabbreviation', 'articletitle', 'lastname', 'abstracttext']
        tree = self.parse()
        articles = []
        for a in tree.findall('MedlineCitation'):
            articles.append(MedlineArticle(a))
            # for a in p.getiterator('Article')
        #print "%d articles found." % len(articles)
        return articles
        
        # for e in self.elements:
        #     if e[0] in ('lastname'):
        #         self.documents['authors'].append(e[1])
        #     elif e[0] in ('articletitle', 'abstracttext'):
        #         self.documents['keywords'].append(e[1])
        #     elif e[0] in ('title', 'isoabbreviation'):
        #         self.documents['journals'].append(e[1])
        # return self.documents

class EndnoteXMLParser(XMLParser):
    def process(self):
        self.allowed_elements = ['author', 'authors', 'title', 'abstract', 'keyword', 'keywords', 'full-title', 'secondary-title', 'secondary_title', 'journal']
        self.parse()
        for e in self.elements:
            if e[0] in ('author', 'authors'):
                self.documents['authors'].append(e[1])
            elif e[0] in ('title', 'abstract', 'keyword', 'keywords', 'full-title'):
                self.documents['keywords'].append(e[1])
            elif e[0] in ('secondary-title', 'secondary_title', 'journal'):
                if e[1].lower().find('submit') < 0:
                    self.documents['journals'].append(e[1])
        return self.documents

if __name__ == '__main__':
    main()
