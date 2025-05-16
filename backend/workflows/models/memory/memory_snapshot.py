# workflows/models/memory/memory_snapshot.py

from pydantic import BaseModel
from typing import Optional
from workflows.models.alpha.alpha_models import ParsedAlphaDocument
from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument
from workflows.models.betaWord.beta_word_models import ParsedBetaWordDocument


class MemorySnapshot(BaseModel):
    session_id: str  # unique ID per transformation run
    alpha_data: Optional[ParsedAlphaDocument]
    beta_word_data: Optional[ParsedBetaWordDocument]
    beta_excel_data: Optional[ParsedBetaExcelDocument]
