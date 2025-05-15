# models/alpha_models.py
from pydantic import BaseModel
from typing import List, Dict
from workflows.models.alpha.inferred_field import InferredField
from workflows.models.alpha.relationship import FieldRelationship
from typing import Any


class ParsedAlphaDocument(BaseModel):
    doc_id: str  # e.g. "alpha_contract.docx"
    raw_data: Dict[str, Any]  # from document_utils
    inferred_fields: List[InferredField]
    relationships: List[FieldRelationship]
    missing_fields: List[str]
