import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
load_dotenv()

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__file__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain =  self.prompt |self.llm | self.parser|self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized successfully")


    def compare_documents(self):
        """
        Formats the response from the LLM into a structured format.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in compare_document:{e}")
            raise DocumentPortalException("Error in document comparison", sys) from e

    def _format_response(self):
        """
        Formats the response from the LLM into a structured format.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error formatting response into DataFrame", error=str(e))
            raise DocumentPortalException("Error formatting response", sys)

