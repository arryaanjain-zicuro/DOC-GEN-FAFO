# models/inferred_field.py
from pydantic import BaseModel
from typing import Literal, Optional


class InferredField(BaseModel):
    name: str
    type: Literal["text", "number", "date", "currency"]
    value: Optional[str]
    source: Literal["paragraph", "table"]
    source_location: Optional[str] = None # e.g. "Paragraph 4", "Table 2 Row 3"

