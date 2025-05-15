# app/parsing/beta_word_parser.py

import json, re
from typing import Dict, Any
from app.parsing.base.document_utils import extract_from_docx
from app.parsing.base.gemini_client import send_prompt
from workflows.models.betaWord.beta_word_models import ParsedBetaWordDocument
from workflows.models.betaWord.shared.field_mapping import BetaWordFieldMapping
from workflows.models.alpha.alpha_models import ParsedAlphaDocument

def build_comparison_prompt(alpha_fields: Any, beta_raw_data: Dict[str, Any]) -> str:
    alpha_json = json.dumps(
        [field.model_dump() for field in alpha_fields], indent=2
    )    
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

def parse_beta_word(beta_path: str, alpha_data: ParsedAlphaDocument) -> ParsedBetaWordDocument:
    beta_raw_data = extract_from_docx(beta_path)
    prompt = build_comparison_prompt(alpha_data.inferred_fields, beta_raw_data)
    gemini_response = send_prompt(prompt)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from Gemini in Word parser: {e}")

    return ParsedBetaWordDocument(
        raw_data=beta_raw_data,
        field_mappings=[BetaWordFieldMapping(**f) for f in result.get("field_mappings", [])],
        unmatched_beta_fields=result.get("unmatched_beta_fields", []),
        transformation_notes=result.get("transformation_notes", "")
    )
