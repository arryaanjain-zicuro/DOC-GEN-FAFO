import os
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key"))
import json
import time
from typing import Dict, Any, List
from ratelimit import limits, sleep_and_retry

# Set OpenAI key

# gpt-3.5-turbo rate limit (e.g., 20 requests per minute)
CALLS = 20
RATE_LIMIT = 60  # seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_gpt(prompt: str) -> Dict[str, Any]:
    """Send request to GPT with rate limiting."""
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1200,
    temperature=0.3)
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise ValueError("Could not parse GPT response:\n" + response.choices[0].message.content)

def extract_beta_word(docx_file: str) -> Dict[str, Any]:
    """Extract tables and paragraphs from a beta Word document."""
    doc = Document(docx_file)
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            if len(row.cells) >= 2:
                key = row.cells[0].text.strip()
                value = row.cells[1].text.strip()
                if key or value:
                    table_data.append({"key": key, "value": value})
        if table_data:
            tables.append(table_data)

    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

    return {
        "tables": tables,
        "paragraphs": paragraphs,
    }

def analyze_beta_against_alpha(alpha_analysis: Dict[str, Any], beta_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send GPT prompt with alpha fields and beta data to analyze patterns."""
    prompt = f"""
You are an AI system that compares an ALPHA document to a BETA document.

Alpha (base template) fields:
{json.dumps(alpha_analysis['fields'], indent=2)}

Beta (transformed version) raw content:
{json.dumps(beta_data, indent=2)}

Your tasks:
1. Identify which ALPHA fields are reused in BETA.
2. Explain how each reused field is transformed or formatted (e.g., casing, math operation, string template).
3. Detect any new fields in BETA not derived from ALPHA.
4. Return a JSON with:
    - "field_mappings": List of mappings {{"alpha_field": ..., "beta_occurrence": ..., "transformation": ...}}
    - "unmatched_beta_fields": List of raw beta values not linked to alpha
    - "transformation_notes": Any pattern notes (e.g., formulas, formatting)
"""

    return call_gpt(prompt)

def parse_beta_document(beta_path: str, alpha_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """End-to-end parse of beta document and comparison with alpha."""
    beta_data = extract_beta_word(beta_path)
    mapping_result = analyze_beta_against_alpha(alpha_analysis, beta_data)

    return {
        "beta_raw": beta_data,
        "mapping_result": mapping_result
    }

# Usage example
# if __name__ == "__main__":
#     import sys
#     from backend.app.parser.alpha_doc_parser import parse_alpha_document

#     if len(sys.argv) != 3:
#         print("Usage: python beta_doc_parser.py alpha.docx beta.docx")
#         sys.exit(1)

#     alpha_path = sys.argv[1]
#     beta_path = sys.argv[2]

#     alpha = parse_alpha_document(alpha_path)["gpt_analysis"]
#     result = parse_beta_document(beta_path, alpha)

#     print("\n=== Beta Mappings ===")
#     print(json.dumps(result["mapping_result"], indent=2))
