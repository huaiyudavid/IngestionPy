import web
import tempfile
import os
import subprocess
import shutil
from extraction.core import ExtractionRunner
from extraction.runnables import Extractor, RunnableError, Filter, ExtractorResult
import extractor.csxextract.extractors.grobid as grobid
import extractor.csxextract.extractors.pdfbox as pdfbox
import extractor.csxextract.extractors.parscit as pa

class StreamlineExtraction:
    """
    Class used to extract metadata from documents without outputting to file. Output
    is returned directly from methods
    """
    def __init__(self):
        self.runner = ExtractionRunner()
        self.runner.add_runnable(pdfbox.PDFBoxPlainTextExtractor)
        self.runner.add_runnable(filters.AcademicPaperFilter)
        self.runner.add_runnable(grobid.GrobidHeaderTEIExtractor)
        self.runner.add_runnable(parscit.ParsCitCitationExtractor)

    #Purpose: runs extactor on specified file
    #Parameters: path - path to pdf file
    #Returns: dictionary containing results from each extraction, get results using resultsToString in utilities.py
    def extract(self, path):
        results = self.runner.run_from_file_batch_no_output(path)
        return results