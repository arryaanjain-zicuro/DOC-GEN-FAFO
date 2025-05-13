import os
import openpyxl
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key"))
import json
from typing import Dict, Any, List
from ratelimit import limits, sleep_and_retry

# Set OpenAI key

CALLS = 20
RATE_LIMIT = 60  # seconds

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def call_gpt(prompt: str) -> Dict[str, Any]:
    response = client.chat.completions.create(model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1200,
    temperature=0.3)
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise ValueError("Could not parse GPT response:\n" + response.choices[0].message.content)

def extract_excel_content(excel_file: str) -> Dict[str, List[List[str]]]:
    """Extract content from all sheets of an Excel file."""
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    content = {}
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        rows = []
        for row in ws.iter_rows(values_only=True):
            if any(cell is not None for cell in row):
                rows.append([str(cell).strip() if cell is not None else "" for cell in row])
        content[sheet] = rows
    return content

def analyze_excel_against_alpha(alpha_analysis: Dict[str, Any], beta_excel_data: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
You are an AI system comparing ALPHA fields with a BETA Excel sheet.

Alpha (base template) fields:
{json.dumps(alpha_analysis['fields'], indent=2)}

Beta (Excel) content:
{json.dumps(beta_excel_data, indent=2)}

Your tasks:
1. Identify which ALPHA fields are reused in BETA Excel.
2. Explain any transformations (math, formatting, references).
3. Detect new fields in BETA.
4. Output JSON:
    - "field_mappings": List of mappings {{"alpha_field": ..., "sheet": ..., "cell": ..., "value": ..., "transformation": ...}}
    - "unmatched_beta_cells": List of unlinked cells
    - "transformation_notes": Summary of any formulas or logic
"""
    return call_gpt(prompt)

def parse_beta_excel(excel_path: str, alpha_analysis: Dict[str, Any]) -> Dict[str, Any]:
    beta_data = extract_excel_content(excel_path)
    mapping_result = analyze_excel_against_alpha(alpha_analysis, beta_data)

    return {
        "beta_raw": beta_data,
        "mapping_result": mapping_result
    }

# Example usage
# if __name__ == "__main__":
#     import sys
#     from backend.app.parser.alpha_doc_parser import parse_alpha_document

#     if len(sys.argv) != 3:
#         print("Usage: python beta_excel_parser.py alpha.docx beta.xlsx")
#         sys.exit(1)

#     alpha_path = sys.argv[1]
#     beta_excel_path = sys.argv[2]

#     alpha = parse_alpha_document(alpha_path)["gpt_analysis"]
#     result = parse_beta_excel(beta_excel_path, alpha)

#     print("\n=== Excel Mappings ===")
#     print(json.dumps(result["mapping_result"], indent=2))
