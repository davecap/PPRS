import optparse
import os

import xmlparser
import indexer

def main():
    usage = """
        usage: %prog [options] <Medline XML File> <Endnote XML File>
    """
    
    parser = optparse.OptionParser(usage)
    # parser.add_option("-x", dest="col_x", default=0, help="X Column [default: %default]")
    # parser.add_option("-y", dest="col_y", default=1, help="Y Column [default: %default]")

    options, args = parser.parse_args()
    if len(args) < 2:
        parser.error("Input files not specified")

    # Parse the Endnote XML file
    xi = indexer.XMLIndexer(args[1])
    xi.create_index()
    
    # Parse the MEDLINE XML file into individual papers
    xp = xmlparser.MedlineXMLParser(args[0])
    articles = xp.process()
    
    for a in articles:
        score = 0
        j_score = 0
        a_score = 0
        k_score = 0
        for j in a.journals:
            j_score = xi.get_idf_of_journal(j)
        for author in a.authors:
            a_score = xi.get_idf_of_author(author)
        for k in xi.tokenize_keywords(a.title):
            k_score = xi.get_idf_of_keyword(k)
        for k in xi.tokenize_keywords(a.abstract):
            k_score += xi.get_idf_of_keyword(k)
        score = j_score+a_score+k_score
        print "%s %f %f %f %f" % (a.pmid, j_score, a_score, k_score, score)
        #print score

if __name__ == '__main__':
    main()
