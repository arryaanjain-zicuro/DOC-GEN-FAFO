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

Your task:
Match fields from ALPHA to cells in the Excel BETA file and infer their relationship.

Return a JSON object with:
1. "field_mappings": a list of mappings, where each item includes:
   - "alpha_field": the corresponding field name from ALPHA
   - "sheet": the Excel sheet name
   - "cell": the exact Excel cell reference (e.g., "B4")
   - "value": the actual value in that cell
   - "transformation": short description of formatting or transformation applied
   - "action": one of ["write", "append", "calculate", "ignore"]
     - "write": the alpha value is directly inserted
     - "append": the alpha value is added to existing cell content
     - "calculate": the value is derived using a formula or rule
     - "ignore": do not use this field for generation
   - "explanation": a sentence explaining why this action and transformation was chosen

2. "unmatched_beta_cells": a list of Excel cells with no clear ALPHA source, e.g., ["Sheet1!C5"]

3. "transformation_notes": overall notes about patterns, transformations, or calculations observed across multiple fields.

Return only **valid JSON** without markdown or extra commentary.
"""

def parse_beta_excel(excel_path: str, alpha_data: ParsedAlphaDocument) -> ParsedBetaExcelDocument:
    beta_excel_data = extract_excel_content(excel_path)
    prompt = build_excel_comparison_prompt(alpha_data.inferred_fields, beta_excel_data)

    gemini_response = send_prompt(prompt, usage_key="beta_word_parser")
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
         print("Raw Gemini response that caused JSON error:", cleaned, flush=True)
         print(gemini_response[:1000])  # Truncate to avoid flooding logs
         raise ValueError(f"Invalid JSON from Gemini in Excel parser: {e}")

    return ParsedBetaExcelDocument(
        raw_data=beta_excel_data,
        field_mappings=[BetaExcelFieldMapping(**f) for f in result.get("field_mappings", [])],
        unmatched_beta_cells=result.get("unmatched_beta_cells", []),
        transformation_notes=result.get("transformation_notes", "")
    )
