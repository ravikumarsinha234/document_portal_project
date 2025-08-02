import os
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentComparatorLLM:

    def __init__(self, data_dir=None, session_id=None):
        pass

    def save_pdf(self, uploaded_file):
        pass

    def read_pdf(self, pdf_path: str) -> str:
        pass

