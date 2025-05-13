# app/api/routes.py
from fastapi import APIRouter, UploadFile, Form, Request
from app.services.document_generator import generate_document
from app.core.limiter import limiter
from app.services.excel_generator import fill_ncd_mis_excel
from backend.app.parser.alpha_doc_parser import extract_term_sheet_data
import os

router = APIRouter()

@router.post("/generate/")
@limiter.limit("5/minute")
async def generate(
    request: Request,
    term_sheet: UploadFile,
    template_name: str = Form(...),
    output_format: str = Form("excel")  # Can expand to "docx" in future
):
    # 1. Save uploaded term sheet to disk temporarily
    term_sheet_path = f"app/data/input/{term_sheet.filename}"
    with open(term_sheet_path, "wb") as f:
        f.write(await term_sheet.read())

    # 2. Extract data from .docx term sheet
    with open(term_sheet_path, "rb") as f:
        term_data = extract_term_sheet_data(f)

    # 3. Generate output file
    output_file_path = f"app/data/output/generated_{os.path.splitext(template_name)[0]}.xlsx"
    template_file_path = f"app/templates/{template_name}"

    if output_format == "excel":
        fill_ncd_mis_excel(term_data, template_file_path, output_file_path)
    else:
        return {"error": "Unsupported format"}

    return {
        "status": "success",
        "output_path": output_file_path,
        "data_used": term_data  # Optional, useful for debugging/testing
    }

@router.get("/")
async def root():
    return {"message": "Backend is up and running 🚀"}
