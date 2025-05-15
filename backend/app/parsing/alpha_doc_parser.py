# app/parsing/alpha_parser.py
import json, re
from app.parsing.base.document_utils import extract_from_docx
from app.parsing.base.gemini_client import send_prompt
from typing import Dict, Any


def build_analysis_prompt(data: Dict[str, Any]) -> str:
    data_str = json.dumps(data, indent=2)
    return f"""
You are a document analysis AI. Given the following extracted data from a Word document:

{data_str}

Return a JSON object with:
1. "inferred_fields": list of objects with:
   - "name": field name
   - "type": text | number | date | currency
   - "value": raw or example value
   - "source": "paragraph" or "table"
2. "relationships": list of logical links between fields (e.g., parent-child)
3. "missing_fields": list of commonly expected fields that are absent

Return only valid JSON. No markdown, no explanations.
"""

def parse_alpha_document(docx_path: str) -> Dict[str, Any]:
    raw_data = extract_from_docx(docx_path)
    prompt = build_analysis_prompt(raw_data)
    gemini_response = send_prompt(prompt)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_response.strip(), flags=re.IGNORECASE)

    try:
        structured = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid Gemini JSON: {e}")

    return {
        "raw_data": raw_data,
        "inferred_fields": structured.get("inferred_fields", []),
        "relationships": structured.get("relationships", []),
        "missing_fields": structured.get("missing_fields", [])
    }
    #optional change to test later, source traceability
    # return {
    # "doc_id": docx_path.split("/")[-1],
    # "raw_data": raw_data,
    # "inferred_fields": structured.get("inferred_fields", []),
    # "relationships": structured.get("relationships", []),
    # "missing_fields": structured.get("missing_fields", [])
    # }
