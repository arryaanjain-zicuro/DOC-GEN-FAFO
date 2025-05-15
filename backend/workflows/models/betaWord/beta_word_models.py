# workflows/models/betaWord/beta_word_models.py

from pydantic import BaseModel
from typing import List, Dict, Any
from workflows.models.betaWord.shared.field_mapping import BetaWordFieldMapping  

class ParsedBetaWordDocument(BaseModel):
    raw_data: Dict[str, Any]
    field_mappings: List[BetaWordFieldMapping]
    unmatched_beta_fields: List[str]
    transformation_notes: str
