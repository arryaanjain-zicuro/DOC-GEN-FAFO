# models/alpha_models.py
from pydantic import BaseModel
from typing import List, Dict
from workflows.models.alpha.inferred_field import InferredField
from workflows.models.alpha.relationship import FieldRelationship
from typing import Any, Optional


class ParsedAlphaDocument(BaseModel):
    doc_id: Optional[str] = None    
    raw_data: Dict[str, Any]  # from document_utils
    inferred_fields: List[InferredField]
    relationships: List[FieldRelationship]
    missing_fields: List[str]
