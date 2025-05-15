# models/relationship.py
from pydantic import BaseModel


class FieldRelationship(BaseModel):
    parent: str  # name of parent field
    child: str   # name of child field
    relation_type: str  # e.g., "belongs_to", "derived_from", etc.
