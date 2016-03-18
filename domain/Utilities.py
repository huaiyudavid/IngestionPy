import web
import tempfile
import os
import subprocess
import xmltodict
import json
import cgi
import shutil
import magic
import xml.etree.ElementTree as ET
from extraction.runnables import Extractor, RunnableError, Filter, ExtractorResult

class Utilities:
    """
    Some utility methods for input and output
    Errors are caught in the calling classes
    """

    #Purpose: reads text result in a results dict
    #Parameters: results - dictionary of results mapped by runnables
    #            runnable - the given runnable to find results for
    #Returns: text result for the given runnable
    def resultsToString(self, results, runnable):
        result = results[runnable]

        if isinstance(result, RunnableError):
            error = result.msg
            return error
        elif isinstance(result, ExtractorResult):
            files_dict = result.files

            if result.xml_result is not None:
               return ET.tostring(result.xml_result, encoding='UTF-8')

            if files_dict:
                data = ''
                for file_name, file_data in files_dict.items():
                    data = data + file_data
                return data

