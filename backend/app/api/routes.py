# app/api/routes.py
from fastapi import APIRouter, UploadFile, Form, Request
from app.services.document_generator import generate_document
from app.core.limiter import limiter
from app.services.excel_generator import fill_ncd_mis_excel
from backend.app.parser.alpha_doc_parser import extract_term_sheet_data
import os

from app.services.run_transformation import run_graph_async
import uuid
from slowapi.util import get_remote_address
from fastapi import File
from fastapi.responses import FileResponse


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

#langgraph transformed to an async api
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/run-transformation")
@limiter.limit("10/minute")
async def run_transformation(alpha: UploadFile = File(...), beta_word: UploadFile = File(...), beta_excel: UploadFile = File(...)):
    # Save uploaded files temporarily
    def save_temp_file(file: UploadFile) -> str:
        path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(path, "wb") as f:
            f.write(file.file.read())
        return path

    alpha_path = save_temp_file(alpha)
    beta_word_path = save_temp_file(beta_word)
    beta_excel_path = save_temp_file(beta_excel)

    try:
        result = await run_graph_async(alpha_path, beta_word_path, beta_excel_path)
        return JSONResponse(content=result)
    finally:
        # Optional cleanup
        for path in [alpha_path, beta_word_path, beta_excel_path]:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Warning: failed to delete {path}: {e}")


@router.get("/")
async def root():
    return {"message": "Backend is up and running 🚀"}
