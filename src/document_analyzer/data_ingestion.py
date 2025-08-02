import os
import fitz
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
            self.log = CustomLogger().get_logger(__file__)
            self.data_dir = data_dir or os.getenv("DATA_STORAGE_PATH",os.path.join(os.getcwdd(),"data","document_analysis"))
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
            pass
        except Exception as e:
            self.log.error("Error saving PDF", error=str(e))
            raise DocumentPortalException(f"Failed to save PDF", sys)

    def read_pdf(self,pdf_path:str)-> str:
        try:
            text_chunks = []
            with fitz.open(self.data_dir) as doc:
                for page in doc:
                    text = page.get_text()
                    if text:
                        text_chunks.append(text)
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException(f"Failed to read PDF", sys)
        

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    handler =DocumentHandler()

    pdf_path = r"C:\\Users"

    class DummyFile:
        def __init__(self, path):
            self.name = Path(file_path).name
            self._file_path = file_path
        def getbuffer(self):
            return open(self._file_path, 'rb').read()
        


        def read(self):
            return b"%PDF-1.4\n%...dummy PDF content..."

    try:
        handler = DocumentHandler()
        # Simulate saving a PDF
        handler.save_pdf(pdf_data="Sample PDF data")
        # Simulate reading a PDF
        handler.read_pdf()
    except DocumentPortalException as e:
        handler.log.error(e)
        raise e
    except Exception as e:
        handler.log.error("An unexpected error occurred", error=str(e))
        raise DocumentPortalException(f"An unexpected error occurred", sys)