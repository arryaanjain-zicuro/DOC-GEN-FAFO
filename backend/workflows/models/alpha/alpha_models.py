# models/alpha_models.py
from pydantic import BaseModel
from typing import List, Dict
from alpha.inferred_field import InferredField
from alpha.relationship import FieldRelationship


class ParsedAlphaDocument(BaseModel):
    doc_id: str  # e.g. "alpha_contract.docx"
    raw_data: Dict[str, any]  # from document_utils
    inferred_fields: List[InferredField]
    relationships: List[FieldRelationship]
    missing_fields: List[str]
