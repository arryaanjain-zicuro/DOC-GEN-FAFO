# models/beta_excel_document.py
from pydantic import BaseModel
from typing import List, Dict
from workflows.models.betaExcel.beta_excel_mapping import BetaExcelFieldMapping


class ParsedBetaExcelDocument(BaseModel):
    raw_data: Dict[str, List[List[str]]]  # sheet_name -> 2D table
    field_mappings: List[BetaExcelFieldMapping]
    unmatched_beta_cells: List[str]  # e.g. ["Sheet1!B3", "Sheet2!A4"]
    transformation_notes: str
