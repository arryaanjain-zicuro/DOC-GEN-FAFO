import os, json, time, re
from docx import Document
from dotenv import load_dotenv

from typing import List, Dict, Any
import google.generativeai as genai

from app.core.gemini_rate_limiter import GeminiRateLimiter

load_dotenv()

# Initialize Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

# Document extraction functions
def extract_tables(doc: Document) -> List[List[Dict[str, str]]]:
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
    return tables

def extract_paragraphs(doc: Document) -> List[str]:
    return [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# Prompt builder
def build_prompt(data: Dict[str, Any]) -> str:
    data_str = json.dumps(data, indent=2)
    return f"""
You are a document analysis AI. Given the following data extracted from a Word document:

{data_str}

Please return a JSON object with:
1. "fields" - A list of extracted fields. Each field must have:
   - "name"
   - "type" (text, date, currency, number)
   - "source" (table or paragraph)
   - "value"
2. "relationships" - Logical relationships or hierarchies between fields.
3. "missing_fields" - Potentially useful fields that are missing but typically expected.

Return only the JSON.
"""

rate_limiter = GeminiRateLimiter(rate_limit_per_minute=60)

def send_to_gemini(prompt: str, retries: int = 5) -> str:
    for attempt in range(retries):
        try:
            rate_limiter.wait()  # throttle before request
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[Attempt {attempt+1}] Gemini error: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(2)  # fixed delay between retries

# Main document parser
def parse_alpha_document(docx_file_path: str) -> Dict[str, Any]:
    doc = Document(docx_file_path)
    extracted = {
        "tables": extract_tables(doc),
        "paragraphs": extract_paragraphs(doc),
    }
    prompt = build_prompt(extracted)
    gemini_response = send_to_gemini(prompt)
    cleaned_response = re.sub(r"^```json\s*|\s*```$", "", gemini_response.strip())

    # Now safely parse the JSON
    try:
        parsed_result = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in Gemini response: {e}")
    
    return {
        "raw_data": extracted,
        "gemini_analysis": parsed_result  # assuming valid JSON
    }

# Test route-compatible function
async def test_gemini():
    try:
        response = model.generate_content("Say hello.")
        return {"status": "success", "response": response.text}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# For CLI or script usage
# if __name__ == "__main__":
#     import sys
#     from pprint import pprint

#     if len(sys.argv) != 2:
#         print("Usage: python alpha_doc_parser.py path_to_document.docx")
#         sys.exit(1)

#     docx_path = sys.argv[1]
#     result = parse_alpha_document(docx_path)

#     print("\n=== Raw Extracted Data ===")
#     pprint(result["raw_data"])

#     print("\n=== GPT Structured Analysis ===")
#     pprint(result["gpt_analysis"])
