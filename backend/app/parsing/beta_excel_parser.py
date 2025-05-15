# app/parsing/beta_excel_parser.py
import json, re
from app.parsing.base.excel_utils import extract_excel_content
from app.parsing.base.gemini_client import send_prompt

def build_excel_prompt(alpha_fields, beta_data):
    return f"""
Compare ALPHA fields to BETA Excel content.

Alpha:
{json.dumps(alpha_fields, indent=2)}

Beta:
{json.dumps(beta_data, indent=2)}

Return JSON with:
- field_mappings
- unmatched_beta_cells
- transformation_notes
"""

def parse_beta_excel(path: str, alpha_analysis: dict):
    beta_data = extract_excel_content(path)
    prompt = build_excel_prompt(alpha_analysis["fields"], beta_data)
    raw_response = send_prompt(prompt)
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_response.strip())

    return {
        "beta_raw": beta_data,
        "mapping_result": json.loads(cleaned)
    }
