import json, re
from typing import Dict, Any
from app.parsing.base.document_utils import extract_from_docx
from app.parsing.base.gemini_client import send_prompt


def build_comparison_prompt(alpha_fields: Any, beta_raw_data: Dict[str, Any]) -> str:
    alpha_json = json.dumps(alpha_fields, indent=2)
    beta_json = json.dumps(beta_raw_data, indent=2)
    return f"""
You are an AI tasked with comparing an ALPHA template (base document fields) to a BETA Word document.

ALPHA (structured fields):
{alpha_json}

BETA (raw extracted Word content):
{beta_json}

Your output should be a JSON object with:
1. "field_mappings": list of objects, each with:
   - "alpha_field": name from ALPHA
   - "beta_occurrence": actual occurrence in BETA
   - "transformation": description of formatting or transformation applied

2. "unmatched_beta_fields": any values in BETA not clearly derived from ALPHA.

3. "transformation_notes": general notes about patterns or formulas used.

Return **only valid JSON**. Do not include markdown or commentary.
"""


def parse_beta_word(beta_path: str, alpha_data: Dict[str, Any]) -> Dict[str, Any]:
    beta_raw_data = extract_from_docx(beta_path)
    prompt = build_comparison_prompt(alpha_data["inferred_fields"], beta_raw_data)
    gemini_response = send_prompt(prompt)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        mapping_result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Gemini: {e}")

    return {
        "beta_raw": beta_raw_data,
        "mapping_result": mapping_result
    }
