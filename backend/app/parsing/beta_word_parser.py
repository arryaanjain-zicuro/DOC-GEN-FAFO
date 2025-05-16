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
You are an AI system comparing an ALPHA document (base structure) to a BETA Word document.

ALPHA (structured fields):
{alpha_json}

BETA (extracted Word content):
{beta_json}

Your task:
Match ALPHA fields to BETA document content and describe how they are transformed or reused.

Return a JSON object with:
1. "field_mappings": list of mappings, where each item includes:
   - "alpha_field": name from ALPHA
   - "beta_occurrence": the corresponding field/value found in the BETA document
   - "transformation": description of formatting, rewriting, or other modification
   - "action": one of ["write", "append", "ignore"]
     - "write": direct insertion from ALPHA
     - "append": added to pre-existing text
     - "ignore": not used in generation
   - "explanation": a sentence explaining why this mapping and action makes sense

2. "unmatched_beta_fields": BETA content not clearly derived from ALPHA.

3. "transformation_notes": general observations about formatting, formulae, or templating patterns.

Return **valid JSON only** — no markdown, no commentary.
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
