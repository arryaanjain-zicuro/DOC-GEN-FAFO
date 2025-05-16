from pydantic import BaseModel
from typing import Optional, Literal

class BetaExcelFieldMapping(BaseModel):
    alpha_field: str
    sheet: str
    cell: str
    value: Optional[str]
    transformation: Optional[str]
    action: Literal["write", "append", "calculate", "ignore"] = "write"
    explanation: Optional[str]  # e.g. "Field is copied directly", "Sum of Alpha fields A and B"
