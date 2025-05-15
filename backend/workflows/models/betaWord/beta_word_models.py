# workflows/models/betaWord/beta_word_models.py

from pydantic import BaseModel
from typing import List, Dict, Any
from shared.field_mapping import WordFieldMapping  # you'll define this

class ParsedBetaWordDocument(BaseModel):
    raw_data: Dict[str, Any]
    field_mappings: List[WordFieldMapping]
    unmatched_beta_fields: List[str]
    transformation_notes: str
