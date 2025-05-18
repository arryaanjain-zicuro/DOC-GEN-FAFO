# app/parsing/beta_word_parser.py

import json, re
from typing import Dict, Any
from app.parsing.base.document_utils import extract_from_docx
from app.parsing.base.gemini_client import send_prompt
from workflows.models.betaWord.beta_word_models import ParsedBetaWordDocument
from workflows.models.betaWord.shared.field_mapping import BetaWordFieldMapping
from workflows.models.alpha.alpha_models import ParsedAlphaDocument

def build_comparison_prompt(alpha_fields: Any, beta_raw_data: Dict[str, Any]) -> str:
    from textwrap import dedent
    alpha_json = json.dumps([f.model_dump() for f in alpha_fields], indent=2, ensure_ascii=False)
    beta_json  = json.dumps(beta_raw_data,               indent=2, ensure_ascii=False)

    schema_block = """
    ---SCHEMA---
    {
    "field_mappings":[
        {
        "alpha_field":"str",
        "beta_occurrence":"str",   // MUST be verbatim text from BETA, else ""
        "transformation":"str",
        "action":"write | append | ignore",
        "explanation":"str"
        }
    ],
    "unmatched_beta_fields":["str"],
    "transformation_notes":"str"
    }
    ---END_SCHEMA---
    """

    rules = """
    **Rules for `action`:**
    • Use `"write"` **only if** the `beta_occurrence` string matches the Alpha value
    *exactly* (case-insensitive, whitespace-normalised).  
    • Use `"append"` when the Alpha value appears **inside** a longer Beta string.  
    • Otherwise return `"ignore"` and leave `beta_occurrence` as an empty string.

    If a field is ignored, say why in `explanation` (“value not found”).
    Return valid JSON only.
    """
    prompt = f"{schema_block}\n{rules}\n\nALPHA ↓\n{alpha_json}\n\nBETA ↓\n{beta_json}"


    return f"""{prompt}

You are an AI system comparing an **ALPHA** document (structured) to a **BETA** Word document.

ALPHA fields ↓
{alpha_json}

BETA extracted content ↓
{beta_json}

Output **exactly** one JSON object that conforms to the schema above.
Nothing else – no Markdown, no comments.
"""



def parse_beta_word(beta_path: str, alpha_data: ParsedAlphaDocument) -> ParsedBetaWordDocument:
    beta_raw_data = extract_from_docx(beta_path)
    prompt = build_comparison_prompt(alpha_data.inferred_fields, beta_raw_data)
    gemini_response = send_prompt(prompt,usage_key="beta_excel_parser")
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("Error even after clean response: ",cleaned, flush=True)
        raise ValueError(f"Invalid JSON from Gemini in Word parser: {e}")

    return ParsedBetaWordDocument(
        raw_data=beta_raw_data,
        field_mappings=[BetaWordFieldMapping(**f) for f in result.get("field_mappings", [])],
        unmatched_beta_fields=result.get("unmatched_beta_fields", []),
        transformation_notes=result.get("transformation_notes", "")
    )
