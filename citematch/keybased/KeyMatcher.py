from citematch.SelfCitationFilter import SelfCitationFilter
from domain.Author import Author
from domain.Citation import Citation
from citematch.keybased.KeyGenerator import KeyGenerator

"""
This citation clusterer implmentation uses a hash key approach to 
cluster citations and documents in an online manner. A KeyGenerator
is used to create the hash keys and mappings are managed within a 
persistent storage backend.
@author Jian Wu, Isaac Councill
"""
class KeyMatcher:
    def clusterDocument(doc):
       # label self-citations in doc
       sfo = SelfCitationFilter()
       sfo.filterCitations(doc)
       # generate document keys
       keys = processDocument(doc)
       # cluster document
       clusterDocument(keys,doc)

    def processsDocument(doc):
        title = doc.getDatum(Document.TITLE_KEY)

        authorBufs = []
        for author in doc.getAuthors():
            authorBufs.append(author.getDatum(Author.NAME_KEY))
        authorStr = ",".join(authorBufs)
        # create keys for all citations
        for citation in doc.getCitations():
            processCitation(citation)

        keys = keyGenerator.getKeys(title, authStr)

    """
    create keys for a given citation and store them within the citation object
    """
    def processCitation(citation):
        title = citation.getDatum(Citation.TITLE_KEY)

        authorBufs = citation.getAuthorNames()
        authorStr = ",".join(authorBufs)
        
        if (not title) or (not authorBufs): return
        
        keys = keyGenerator.getKeys(title,authorStr)
        citation.setKeys(keys)


