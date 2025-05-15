# app/parsing/beta_excel_parser.py

from workflows.models.betaExcel.beta_excel_mapping import BetaExcelFieldMapping
from workflows.models.betaExcel.beta_excel_models import ParsedBetaExcelDocument
from workflows.models.alpha.alpha_models import ParsedAlphaDocument

from app.parsing.base.excel_utils import extract_excel_content
from app.parsing.base.gemini_client import send_prompt
import json, re

def build_excel_comparison_prompt(alpha_fields, beta_excel_data):
    alpha_json = json.dumps(alpha_fields, indent=2)
    beta_json = json.dumps(beta_excel_data, indent=2)
    return f"""
You are an AI system comparing an ALPHA document (base structure) to a BETA Excel file.

ALPHA (structured fields):
{alpha_json}

BETA (Excel content):
{beta_json}

Please return a JSON object with:
1. "field_mappings": list of mappings, each with:
   - "alpha_field": name from ALPHA
   - "sheet": sheet name
   - "cell": Excel cell reference (e.g., A1)
   - "value": actual value in that cell
   - "transformation": transformation logic or formatting

2. "unmatched_beta_cells": list of cell references that do not match ALPHA fields

3. "transformation_notes": patterns/formulas observed in transformations

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
