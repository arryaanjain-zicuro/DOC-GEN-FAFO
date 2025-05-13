# app/api/routes.py
from fastapi import APIRouter, UploadFile, Form, File, Request
from app.services.document_generator import generate_document
from app.core.limiter import limiter
from parser.alpha_doc_parser import parse_alpha_document, test_openai
import os, uuid

from app.services.run_transformation import run_graph_async
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse, FileResponse

from app.services.excel_generator import fill_excel_generic
router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "app/data/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/generate")
@limiter.limit("5/minute")
async def generate_document(
    request: Request,
    alpha_doc: UploadFile = File(...),
    beta_template: UploadFile = File(...),
):
    def save_temp_file(file: UploadFile) -> str:
        path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(path, "wb") as f:
            f.write(file.file.read())
        return path

    # Save uploaded files
    alpha_path = save_temp_file(alpha_doc)
    beta_path = save_temp_file(beta_template)

    try:
        # Parse alpha document (Word)
        parsed_result = parse_alpha_document(alpha_path)
        gpt_fields = parsed_result["gpt_analysis"]["fields"]

        # Fill Excel template
        output_file_path = os.path.join(
            OUTPUT_DIR, f"filled_{uuid.uuid4()}.xlsx"
        )
        fill_excel_generic(gpt_fields, beta_path, output_file_path)

        return {
            "status": "success",
            "output_file": output_file_path,
            "fields": gpt_fields,
        }

    finally:
        os.remove(alpha_path)
        os.remove(beta_path)


#langgraph transformed to an async api
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/run-transformation")
@limiter.limit("10/minute")
async def run_transformation(request: Request, alpha: UploadFile = File(...), beta_word: UploadFile = File(...), beta_excel: UploadFile = File(...)):
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

@router.get("/test-openai")
async def run_test_openai():
    return await test_openai()

@router.get("/")
async def root():
    return {"message": "Backend is up and running 🚀"}
