# backend/models/state.py

from typing import Optional, Dict, Any
from pydantic import BaseModel

class State(BaseModel):
    alpha_path: Optional[str] = None
    beta_word_path: Optional[str] = None
    beta_excel_path: Optional[str] = None

    alpha_data: Optional[Dict[str, Any]] = None
    alpha_raw: Optional[Dict[str, Any]] = None

    beta_word_mapping: Optional[Dict[str, Any]] = None
    beta_raw: Optional[Dict[str, Any]] = None

    beta_excel_mapping: Optional[Dict[str, Any]] = None
    beta_excel_raw: Optional[Dict[str, Any]] = None
