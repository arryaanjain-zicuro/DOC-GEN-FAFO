# app/models/mapper_model.py

from pydantic import BaseModel
from typing import Dict, Any, Literal, Optional


class MapperState(BaseModel):
    alpha_data: Dict[str, Any]
    beta_word_data: Optional[Dict[str, Any]] = None
    beta_excel_data: Optional[Dict[str, Any]] = None
    beta_type: Literal["word", "excel"]
    mapper_output: Optional[Dict[str, Any]] = None
