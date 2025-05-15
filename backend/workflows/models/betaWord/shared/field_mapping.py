# workflows/models/shared/field_mapping.py

from pydantic import BaseModel

class WordFieldMapping(BaseModel):
    alpha_field: str
    beta_occurrence: str
    transformation: str
