# app/workflow/models/shared.py
from pydantic import BaseModel
from typing import Optional, Literal, Union
from workflows.models.alpha.alpha_models import ParsedAlphaDocument
from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument
from workflows.models.betaWord.beta_word_models import ParsedBetaWordDocument

class TransformationState(BaseModel):
    # Input paths
    alpha_path: Optional[str]
    beta_word_path: Optional[str]
    beta_excel_path: Optional[str]
    
    # Type of beta document to route to correct agent
    beta_type: Optional[Literal["word", "excel"]]

    # Parsed outputs
    alpha_data: Optional[ParsedAlphaDocument]
    beta_excel_data: Optional[ParsedBetaExcelDocument]
    beta_word_data: Optional[ParsedBetaWordDocument]
