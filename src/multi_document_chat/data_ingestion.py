import uuid
from pathlib import Path
import sys
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader


class DocumentIngestor:
    SUPPORTED_EXTENSIONS ={'.pdf','.docx','.md','.txt'}
    def __init__(self, temp_dir:str='data/multi_doc_chat', faiss_dir:str='faiss_index',session_id:str | None=None):
        try:
            self.log = CustomLogger(),get_logger(__name__)

            #base dir
            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            self.temp_dir = mkdir(

            )

        except Exception as e:
            self.log.error("Failed to initialize DocumentIngestor",error=str(e))

    
    def ingest_files(self,uploaded_files):
        try:
            documents=[]
            for uploaded_file in uploaded_files:
                ext = Path(uploaded_file.name).suffix.lower()
                if ext not in self.SUPPORTED_EXTENSIONS:
                    self.log.warning("Unsupported file skipped")
                    continue
                unique_filename = f"{uuid.uuid4().hex[:8]}"