import os
import fitz
import sys
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """
    Handles PDF saving and reading operations.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self, data_dir=None,session_id=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH",os.path.join(os.getcwd(),"data","document_analysis"))
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

            # Create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info("PDF Handler initialized",session_id=self.session_id, session_path=self.session_path)
            
        except Exception as e:
            self.log.error("Error initializing DocumentHandler: {e}")
            raise DocumentPortalException(f"Failed to initialize DocumentHandler", e) from e


    def save_pdf(self,uploaded_file):
        try:
            filename = os.path.basename(uploaded_file.name)

            if not filename.lower().endswith('.pdf'):
                raise DocumentPortalException("Invalid file type. Only PDFs are allowed", sys)
            save_path = os.path.join(self.session_path, filename)

            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            self.log.info("PDF saved successfully", filename=filename, save_path=save_path,session_id=self.session_id)
            return save_path
        
        except Exception as e:
            self.log.error("Error saving PDF", error=str(e))
            raise DocumentPortalException(f"Failed to save PDF", sys)

    def read_pdf(self,pdf_path:str)-> str:
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num,page in enumerate(doc,start=1):
                    text_chunks.append(f"\n--- Page {page_num} ---\n{page.get_text()}")
            text = "\n".join(text_chunks)

            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id,pages=len(text_chunks))
            return text
        except Exception as e:
            self.log.error("Error reading PDF: {e}")
            raise DocumentPortalException(f"Failed to read PDF", e) from e
        

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    handler =DocumentHandler()

    pdf_path = r"D:\portfolio projects details\LLMOPs_Projects\document_portal_project\data\document_analysis\sample.pdf"

    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, 'rb').read()
    
    dummy_pdf = DummyFile(pdf_path)

    handler = DocumentHandler()

    try:
        saved_path = handler.save_pdf(dummy_pdf)
        print(saved_path)

        content = handler.read_pdf(saved_path)
        print("PDF Content:")
        print(content[:500])  # Print first 500 characters for brevity
    
    except Exception as e:
        print(f"Error:{e}")