import optparse
import os
from whoosh.index import create_in, open_dir
# from whoosh.fields import *
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.support.charset import charset_table_to_dict, default_charset
from whoosh.analysis import CharsetFilter, StandardAnalyzer, LowercaseFilter, IDTokenizer

from xmlparser import EndnoteXMLParser

from django.utils.encoding import smart_unicode

def main():
    usage = """
        usage: %prog [options] <input file>
    """
    
    parser = optparse.OptionParser(usage)
    # parser.add_option("-x", dest="col_x", default=0, help="X Column [default: %default]")
    # parser.add_option("-y", dest="col_y", default=1, help="Y Column [default: %default]")

    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error("No input file specified")
    
    f = open(args[0])
    xmldata = f.read()
    f.close()
    
    # Parse the Endnote XML file
    xi = XMLIndexer(name=args[0])
    xi.create_index(xmldata)
    
    # Parse the MEDLINE XML file into individual papers
    # for each paper p
    #   score(p)
    #   add to sorted array
    
class XMLIndexer(object):
    def __init__(self, name):
        self.name = name
        self.index_dir = "%s_index" % name
        self.authors_dir = os.path.join(self.index_dir, "authors")
        self.keywords_dir = os.path.join(self.index_dir, "keywords")
        self.journals_dir = os.path.join(self.index_dir, "journals")
        
        # Make 3 indicies: authors, keywords, journals
        # charmap = charset_table_to_dict(default_charset)
        # authors_ana = CharsetFilter(charmap)
        authors_ana = StandardAnalyzer()
        self.schema_authors = Schema(author=TEXT(analyzer=authors_ana, stored=False))
        
        keywords_ana = StandardAnalyzer()
        self.schema_keywords = Schema(keyword=TEXT(analyzer=keywords_ana, stored=False, phrase=False))
        
        journal_ana = IDTokenizer() | LowercaseFilter()
        self.schema_journals = Schema(journal=TEXT(analyzer=journal_ana, stored=False, phrase=True))
        
        self.searcher_journals = None
        self.searcher_keywords = None
        self.searcher_authors = None
    
    def get_idf_of_journal(self, journal):
        if self.searcher_journals is None:
            self.searcher_journals = self.index_journals.searcher()
        return self.searcher_journals.idf(u'journal', u"\"%s\"" % journal)
    
    def tokenize_keywords(self, keywords):
        ana = StandardAnalyzer(minsize=4)
        return [ smart_unicode(token.text) for token in ana(smart_unicode(keywords)) ]
    
    def get_idf_of_keyword(self, keyword):
        if self.searcher_keywords is None:
            self.searcher_keywords = self.index_keywords.searcher()
        return self.searcher_keywords.idf(u'keyword', u"%s" % keyword)
    
    def get_idf_of_author(self, author):
        if self.searcher_authors is None:
            self.searcher_authors = self.index_authors.searcher()
        return self.searcher_authors.idf(u'author', u"%s" % author)
    
    def load_index(self):
        self.index_authors = open_dir(self.authors_dir)
        self.index_keywords = open_dir(self.keywords_dir)
        self.index_journals = open_dir(self.journals_dir)
    
    def create_index(self, xmldata):
        xp = EndnoteXMLParser(xmldata)
        documents = xp.process()

        # Make the index directories
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        if not os.path.exists(self.authors_dir):
            os.mkdir(self.authors_dir)

        if not os.path.exists(self.keywords_dir):
            os.mkdir(self.keywords_dir)

        if not os.path.exists(self.journals_dir):
            os.mkdir(self.journals_dir)

        self.index_authors = create_in(self.authors_dir, self.schema_authors)
        self.index_keywords = create_in(self.keywords_dir, self.schema_keywords)
        self.index_journals = create_in(self.journals_dir, self.schema_journals)
        
        # Authors
        writer = self.index_authors.writer()
        for a in documents['authors']:
            writer.add_document(author=smart_unicode(a))
        writer.commit()

        # Keywords
        writer = self.index_keywords.writer()
        for k in documents['keywords']:
            writer.add_document(keyword=smart_unicode(k))
        writer.commit()

        # Journals
        writer = self.index_journals.writer()
        for j in documents['journals']:
            writer.add_document(journal=smart_unicode(j))
        writer.commit()

if __name__ == '__main__':
    main()
