# models/beta_excel_mapping.py
from pydantic import BaseModel
from typing import Optional


class BetaExcelFieldMapping(BaseModel):
    alpha_field: str
    sheet: str
    cell: str
    value: Optional[str]
    transformation: Optional[str]
