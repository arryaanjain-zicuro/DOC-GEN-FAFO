import json
import re
from typing import List, Dict, Any
from app.parsing.base.gemini_client import send_prompt


def build_universal_mapping_prompt(
    alpha_fields: List[Dict[str, Any]],
    beta_sources: Dict[str, Any],  # sheet_name -> [[...]], or "paragraphs"/"tables" -> [...]
    beta_type: str
) -> str:
    alpha_str = json.dumps(alpha_fields, indent=2)
    beta_str = json.dumps(beta_sources, indent=2)

    return f"""
You are an AI system performing document mapping between ALPHA fields and a BETA document ({beta_type.upper()}).

ALPHA fields (structured):
{alpha_str}

BETA ({beta_type}) extracted content:
{beta_str}

Please return a JSON object with:
1. "field_mappings": list of:
    - "alpha_field": name from ALPHA
    - "beta_location": where the value is found (e.g., "Sheet1!A1" or "Table 2: Row 4" or "Paragraph 3")
    - "value": actual value found in BETA
    - "transformation": how it was derived or modified from ALPHA

2. "unmatched_beta_fields": raw values or cells not linked to ALPHA

3. "transformation_notes": formulaic or formatting patterns observed

Only return valid JSON. No markdown or extra explanation.
"""


def run_mapper_agent(
    alpha_data: Dict[str, Any],
    beta_data: Dict[str, Any],
    beta_type: str  # "word" or "excel"
) -> Dict[str, Any]:
    """
    Run mapping analysis across Alpha and Beta document.
    Assumes:
    - alpha_data includes `inferred_fields`
    - beta_data includes `beta_raw`
    """
    prompt = build_universal_mapping_prompt(
        alpha_fields=alpha_data["inferred_fields"],
        beta_sources=beta_data["beta_raw"],
        beta_type=beta_type
    )

    gemini_response = send_prompt(prompt)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        parsed_result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Gemini in mapper agent: {e}")

    return {
        "field_mappings": parsed_result.get("field_mappings", []),
        "unmatched_beta_fields": parsed_result.get("unmatched_beta_fields", []),
        "transformation_notes": parsed_result.get("transformation_notes", "")
    }
