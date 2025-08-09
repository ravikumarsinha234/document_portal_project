from pydantic import BaseModel, Field, RootModel
from typing import Optional, List, Any, Union
from enum import Enum

class Metadata(BaseModel):
    Summary: List[str] = Field(default_factory=list, description="Summary of the document")
    Title: str
    Author: str
    DateCreated: str
    lastModifiedDate:str
    Publisher: str
    Language: str
    PageCount:Union[int, str] #Can be not available
    SentimentTone: str


class ChangeFormat(BaseModel):
    Page:str
    changes:str

class SummaryResponse(RootModel[List[ChangeFormat]]):
    pass

class PromptType(str,Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"