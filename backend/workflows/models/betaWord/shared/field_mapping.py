from pydantic import BaseModel
from typing import Literal, Optional

class BetaWordFieldMapping(BaseModel):
    alpha_field: str
    beta_occurrence: str
    transformation: str
    action: Literal["write", "append", "ignore"] = "write"
    explanation: Optional[str]  # e.g. "Field is copied directly", "Sum of Alpha fields A and B"
