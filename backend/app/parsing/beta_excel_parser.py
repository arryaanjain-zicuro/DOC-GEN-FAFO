# app/parsing/beta_excel_parser.py

from workflows.models.betaExcel.beta_excel_mapping import BetaExcelFieldMapping
from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument
from workflows.models.alpha.alpha_models import ParsedAlphaDocument

from app.parsing.base.excel_utils import extract_excel_content
from app.parsing.base.gemini_client import send_prompt
import json, re

def build_excel_comparison_prompt(alpha_fields, beta_excel_data):
    alpha_json = json.dumps(
        [field.model_dump() for field in alpha_fields], indent=2
    )   
    beta_json = json.dumps(beta_excel_data, indent=2)
    return f"""
You are an AI system comparing an ALPHA document (base structure) to a BETA Excel file.

ALPHA (structured fields):
{alpha_json}

BETA (Excel content):
{beta_json}

Please return a JSON object with:
1. "field_mappings": a list of matched fields between the ALPHA document and the Excel BETA file. Each item must include:
   - "alpha_field": the corresponding field name from the ALPHA document
   - "sheet": the name of the sheet where the match is found
   - "cell": the exact Excel cell reference (e.g., "B4")
   - "value": actual value in that cell
   - "transformation": a brief description of any formatting, calculation, or transformation applied from the ALPHA value to reach this value

2. "unmatched_beta_cells": a list of Excel cell references (with sheet names, e.g., "Sheet1!C5") that do not clearly correspond to any ALPHA field.

3. "transformation_notes": a single string summarizing any observed patterns, formulas, or formatting rules across multiple mappings. Do not return a dictionary or list here.

Return only valid JSON. No markdown or extra explanation.
"""

def parse_beta_excel(excel_path: str, alpha_data: ParsedAlphaDocument) -> ParsedBetaExcelDocument:
    beta_excel_data = extract_excel_content(excel_path)
    prompt = build_excel_comparison_prompt(alpha_data.inferred_fields, beta_excel_data)

    gemini_response = send_prompt(prompt)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Gemini in Excel parser: {e}")

    return ParsedBetaExcelDocument(
        raw_data=beta_excel_data,
        field_mappings=[BetaExcelFieldMapping(**f) for f in result.get("field_mappings", [])],
        unmatched_beta_cells=result.get("unmatched_beta_cells", []),
        transformation_notes=result.get("transformation_notes", "")
    )
