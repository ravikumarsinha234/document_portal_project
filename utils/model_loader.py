import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
log = CustomLogger().get_logger(__name__)

class ModelLoader:
    """
    Class to load models and configurations for the Document Portal project.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config =load_config()
        log.info("Configuration loaded successfully",config_keys=list(self.config.keys()))

    def _validate_env(self):
        """
        Validate necesary environment variables.
        Ensure API keys exist.
        """
        required_vars =["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing =[k for k,v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing environment variables",missing_vars=missing)
            raise DocumentPortalException(f"Missing environment variables", sys)
        log.info("Environment variables ")

    def load_embeddings(self):
        """
        Load and return the embeddings model."""

        try:
            log.info("Loading embeddings model...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)
        except Exception as e:
            log.error("Error loading embeddings model", error=str(e))
            raise DocumentPortalException(f"Failed to load embedding model", sys)

    def load_llm(self):
        """
        Load and return the LLM model.
        Load LLM dynamically based on the configuration.
        """
        llm_block = self.config["llm"]
        log.info("Loading LLM...")

        provider_key = os.getenv("LLM_PROVIDER_KEY", "groq")
        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider_key=provider_key)
            raise ValueError(f"LLM provider {provider_key} not found in config")
        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model_name=model_name,temperature=temperature, max_tokens=max_tokens)

        if provider =="google":
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            return llm
        
        elif provider =="groq":
            llm = ChatGroq(
                model=model_name,
                api_key=self.api_keys["GROQ_API_KEY"],
                temperature=temperature
            )
            return llm
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")
        

if __name__ == "__main__":
    loader = ModelLoader()

    #Test Embedding model loading
    embeddings = loader.load_embeddings()
    print(f"Embeddings model loaded: {embeddings}")

    #Test LLM loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM loaded: {llm}")

    #Test the Modelloader
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")