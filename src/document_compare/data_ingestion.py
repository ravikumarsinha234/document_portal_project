import os
import fitz
import uuid
import sys
from datetime import datetime
from pathlib import Path
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentIngestion:

    def __init__(self, base_dir:str="data\\document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_exisiting_file(self):
        """
        Deletes existing files in the specified paths.
        """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted",path = str(file))
                self.log.info("Directory cleaned", directory=str(self.base_dir))
        except Exception as e:
            self.log.error("Error deleting existing files: {e}")
            raise DocumentPortalException(f"An error occurred while deleting exisiting files.", sys) from e

    def save_uploaded_files(self, reference_file, actual_file):
        """
        Saves the uploaded file to specific directory.
        """
        try:
            self.delete_existing_files()
            self.log.info("Exisitng files deleted successfully")
            ref_path = self.base_dir/ reference_file.name
            act_path = self.base_dir/ actual_file.name

            if not reference_file.name.endswith('.pdf') or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed")
            
            with open(ref_path, 'wb') as f:
                f.write(reference_file.getbuffer())
            
            with open(act_path, 'wb') as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files saved", reference=str(ref_path), actual = str(act_path))
            return ref_path, act_path

        except Exception as e:
            self.log.error("Error saving uploaded file: {e}")
            raise DocumentPortalException(f"Failed to save uploaded file", sys)

    def read_pdf(self, pdf_path: str) -> str:
        """
        Reads the text from a PDF file and returns it as a string.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted : {pdf_path.name}")
                all_text=[]
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    
                    if text.strip():
                        all_text.append(f"\n ---page {page_num + 1}--- \n{text}")
                self.log.info("PDF read successfully", file =str(pdf_path), page_count=len(all_text))

                return "\n".join(all_text)
        
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException(f"Failed to read PDF", sys) from e

