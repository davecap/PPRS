#!/usr/bin/env python

import sys
from xmlparser import EndnoteXMLParser, MedlineXMLParser, MedlineCitation
import indexer
import StringIO

def test_xml_parsing_endnote():
    xp = EndnoteXMLParser(ENDNOTE_DATA)
    documents = xp.process()
    assert documents is not None
    assert len(documents['authors']) == 3
    assert len(documents['journals']) == 1
    assert len(documents['keywords']) == 3
    
def test_xml_parsing_medline():
    xp = MedlineXMLParser(MEDLINE_DATA)
    documents = xp.process()
    assert documents is not None
    assert len(documents) == 1
    
def test_xml_parsing_pubmed():
    pass
    
def test_indexing():
    pass
    
def test_search_keywords():
    pass
    
def test_search_authors():
    pass
    
def test_search_journals():
    pass
    
def test_scoring_article():
    pass
    

ENDNOTE_DATA="""<?xml version="1.0" encoding="UTF-8"?>
<xml>
    <records>
        <record>
        <database name="test1" path="">hello8</database>
        <source-app name="Papers" version="1.9.3">Papers</source-app>
        <rec-number>6458</rec-number>
        <ref-type>17</ref-type>
        <contributors>
            <authors>
                <author>
                    <style face="normal" font="default" size="100%">Sherrill, C</style>
                </author>
                <author>
                    <style face="normal" font="default" size="100%">Sumpter, B</style>
                </author>
                <author>
                    <style face="normal" font="default" size="100%">Sinnokrot, M</style>
                </author>
            </authors>
        </contributors>
        <periodical>
            <full-title>
                <style face="normal" font="default" size="100%">Journal of cellular biochemistry</style>
            </full-title>
        </periodical>
        <titles>
            <title>
                <style face="normal" font="default" size="100%">Hypoxia-induced modifications in plasma membranes and lipid microdomains in A549 cells and primary human alveolar cells.</style>
            </title>
            <secondary-title>
                <style face="normal" font="default" size="100%">Journal of cellular biochemistry</style>
            </secondary-title>
        </titles>
        <abstract>
            <style face="normal" font="default" size="100%">We evaluated the response to mild hypoxia exposure of A549 alveolar human cells and of a continuous alveolar cell line from human excised lungs (A30) exposed to 5% O(2) for 5 and 24 h. No signs of increased peroxidation and of early apoptosis were detected. After 24 h of hypoxia total cell proteins/DNA ratio decreased significantly by about 20%. Similarly, we found a decrease in membrane phospholipid and cholesterol content. The membrane fluidity assessed by fluorescence anisotropy measurements was unchanged. We also prepared the detergent resistant membrane fraction (DRM) to analyze the distribution of the two types of lipid microdomains, caveolae and lipid rafts. The DRM content of Cav-1, marker of caveolae, was decreased, while CD55, marker of lipid rafts, increased in both cell lines. Total content of these markers in the membranes was unchanged indicating remodelling of their distribution between detergent-resistant and detergent-soluble fraction of the cellular membrane. The changes in protein markers distribution did not imply changes in the corresponding mRNA, except in the case of Cav-1 for A30 line. In the latter case we found a parallel decrease in Cav-1 and in the corresponding mRNA. We conclude that an exposure to a mild degree of hypoxia triggers a significant remodelling of the lipid microdomains expression, confirming that they are highly dynamic structures providing a prompt signalling platform to changes of the pericellular microenvironment.</style>
        </abstract>
        <accession-num>
            <style face="normal" font="default" size="100%">related:y-jRYymFV0wJ</style>
        </accession-num>
        <dates><year><style face="normal" font="default" size="100%">2009</style></year><pub-dates><date><style face="normal" font="default" size="100%">Jan 1</style></date></pub-dates></dates><label><style face="normal" font="default" size="100%">p06458</style></label><custom3><style face="normal" font="default" size="100%">papers://5C8DECC7-C270-488D-AADB-6D96483270E1/Paper/p6458</style></custom3><keywords></keywords>
        </record>
    </records>
</xml>
"""

MEDLINE_DATA="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE MedlineCitationSet PUBLIC "-//NLM//DTD Medline Citation, 1st January, 2010//EN"
"http://www.nlm.nih.gov/databases/dtd/nlmmedlinecitationset_100101.dtd">
<MedlineCitationSet>
    <MedlineCitation Owner="NLM" Status="MEDLINE">
        <PMID>18636548</PMID>
        <DateCreated>
            <Year>2008</Year>
            <Month>09</Month>
            <Day>24</Day>
        </DateCreated>
        <DateCompleted>
            <Year>2009</Year>
            <Month>01</Month>
            <Day>05</Day>
        </DateCompleted>
        <DateRevised>
            <Year>2009</Year>
            <Month>12</Month>
            <Day>10</Day>
        </DateRevised>
        <Article PubModel="Print">
            <Journal>
                <ISSN IssnType="Electronic">1097-4644</ISSN>
                <JournalIssue CitedMedium="Internet">
                    <Volume>105</Volume>
                    <Issue>2</Issue>
                    <PubDate>
                        <Year>2008</Year>
                        <Month>Oct</Month>
                        <Day>1</Day>
                    </PubDate>
                </JournalIssue>
                <Title>Journal of cellular biochemistry</Title>
                <ISOAbbreviation>J. Cell. Biochem.</ISOAbbreviation>
            </Journal>
            <ArticleTitle>Hypoxia-induced modifications in plasma membranes and lipid microdomains in A549 cells and primary human alveolar cells.</ArticleTitle>
            <Abstract>
                <AbstractText>We evaluated the response to mild hypoxia exposure of A549 alveolar human cells and of a continuous alveolar cell line from human excised lungs (A30) exposed to 5% O(2) for 5 and 24 h. No signs of increased peroxidation and of early apoptosis were detected. After 24 h of hypoxia total cell proteins/DNA ratio decreased significantly by about 20%. Similarly, we found a decrease in membrane phospholipid and cholesterol content. The membrane fluidity assessed by fluorescence anisotropy measurements was unchanged. We also prepared the detergent resistant membrane fraction (DRM) to analyze the distribution of the two types of lipid microdomains, caveolae and lipid rafts. The DRM content of Cav-1, marker of caveolae, was decreased, while CD55, marker of lipid rafts, increased in both cell lines. Total content of these markers in the membranes was unchanged indicating remodelling of their distribution between detergent-resistant and detergent-soluble fraction of the cellular membrane. The changes in protein markers distribution did not imply changes in the corresponding mRNA, except in the case of Cav-1 for A30 line. In the latter case we found a parallel decrease in Cav-1 and in the corresponding mRNA. We conclude that an exposure to a mild degree of hypoxia triggers a significant remodelling of the lipid microdomains expression, confirming that they are highly dynamic structures providing a prompt signalling platform to changes of the pericellular microenvironment.</AbstractText>
                <CopyrightInformation>(c) 2008 Wiley-Liss, Inc.</CopyrightInformation>
            </Abstract>
            <AuthorList CompleteYN="Y">
                <Author ValidYN="Y">
                    <LastName>Sherrill</LastName>
                    <ForeName>C</ForeName>
                </Author>
                <Author ValidYN="Y">
                    <LastName>Sumpter</LastName>
                    <ForeName>B</ForeName>
                </Author>
                <Author ValidYN="Y">
                    <LastName>Sinnokrot</LastName>
                    <ForeName>M</ForeName>
                </Author>
            </AuthorList>
            <Language>eng</Language>
            <PublicationTypeList>
                <PublicationType>Journal Article</PublicationType>
                <PublicationType>Research Support, Non-U.S. Gov't</PublicationType>
            </PublicationTypeList>
        </Article>
        <MedlineJournalInfo>
            <Country>United States</Country>
            <MedlineTA>J Cell Biochem</MedlineTA>
            <NlmUniqueID>8205768</NlmUniqueID>
            <ISSNLinking>0730-2312</ISSNLinking>
        </MedlineJournalInfo>
    </MedlineCitation>
</MedlineCitationSet>
"""
