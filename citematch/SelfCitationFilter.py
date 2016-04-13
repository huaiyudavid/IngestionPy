#!/usr/bin/python
# Author: Dr. Jian Wu
# Year: 2016

from domain.Document import Document
from domain.Author import Author
from domain.Citation import Citation
from utility.SafeText import SafeText
import logging

class SelfCitationFilter(object):
    """
    mark all self citations within a Document object.
    @param doc
    """
    def filterCitations(self,doc):
        logger = logging.getLogger("citematch.SelfCitationFilter.SelfCitationFilter.filterCitations")
        authorKeys = set()
        for author in doc.getAuthors():
            key = self.buildNameKey(author.getDatum("name"))
            logger.debug("paper authorkey : %s" % key)
            if key: authorKeys.add(key) 

        for citation in doc.getCitations():
            citation.setSelf(False)
            for name in citation.getAuthorNames():
                citation_authorkey = self.buildNameKey(name)
                if citation_authorkey in authorKeys:
                    logging.debug("citation authorkey : %s"%citation_authorkey)
                    citation.setSelf(True)
                    break


    """
    build a name key using a name
    """
    def buildNameKey(self,name):
        # remove leading and trailing white spaces, and split it by spaces
        tokens = name.strip().split()
        key = None
        # use the entire name string or first_initial+last_name as the key
        if len(tokens) == 1:
            key = tokens[0]
        elif len(tokens) > 1:
            key = tokens[0][0] + tokens[-1]

        if key:
            key = SafeText.normalizeText(key).lower()

        return key
        
 
# test module
if __name__ == "__main__":
    doc = Document()
    
                
      
