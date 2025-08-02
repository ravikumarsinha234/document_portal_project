import os
import fitz
import uuid
from datetime import datetime
from pathlib import Path
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentComparatorLLM:

    def __init__(self, base_dir=None, session_id=None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_exisiting_file():
        pass

    def save_uploaded_files(self, uploaded_file):
        """
        Saves the uploaded file to specific directory.
        """
        try:
            pass
        except Exception as e:
            self.log.error("Error saving uploaded file", error=str(e))
            raise DocumentPortalException(f"Failed to save uploaded file", sys) from e

    def read_pdf(self, pdf_path: str) -> str:
        """
        Reads the text from a PDF file and returns it as a string.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted and cannot be read")
                all_text=[]
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    if text.strip():
                        all_text.append(f"\n ---page {page_num + 1}--- \n{text}")
                self.log.info("PDF read successfully", file =str(pdf_path), page_count=len(all_text))
        
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException(f"Failed to read PDF", sys) from e

