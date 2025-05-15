from fastapi import APIRouter, UploadFile, Form, File, Request
from app.services.document_generator import generate_document
from app.core.limiter import limiter  # You can remove this import if you don't need it anymore
from parser.alpha_doc_parser import parse_alpha_document, test_gemini
import os, uuid, shutil

from app.services.run_transformation import run_graph_async
from fastapi.responses import JSONResponse, FileResponse

from typing import List

from app.services.excel_generator import fill_excel_generic

from workflows.models.shared import TransformationState
from workflows.transformation_graph import transformation_graph

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "app/data/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/generate")
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
        gpt_fields = parsed_result["gemini_analysis"]["fields"]

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
async def run_transformation(
    alpha_doc: UploadFile = File(...),
    beta_word_doc: UploadFile = File(...),
    beta_excel_doc: UploadFile = File(...)
):
    temp_dir = "/tmp/documents"
    os.makedirs(temp_dir, exist_ok=True)

    def save_file(file: UploadFile) -> str:
        path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return path

    # Save all uploaded docs
    alpha_path = save_file(alpha_doc)
    beta_word_path = save_file(beta_word_doc)
    beta_excel_path = save_file(beta_excel_doc)

    # Initialize state
    initial_state = TransformationState(
        alpha_path=alpha_path,
        beta_word_path=beta_word_path,
        beta_excel_path=beta_excel_path
    )

    # Run LangGraph
    graph = transformation_graph()
    final_state = graph.invoke(initial_state)

    return final_state.dict()

#route for app in parsing mode
@router.post("/parsing-mode")
async def parsing_mode(request: Request, files: List[UploadFile] = File(...)):
    paths = []
    for file in files:
        path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        with open(path, "wb") as f:
            f.write(await file.read())
        paths.append(path)

    try:
        from parser.doc_parser_analysis import analyze_documents
        result = await analyze_documents(paths)
        return result
    finally:
        for path in paths:
            os.remove(path)



@router.get("/test-gemini")
async def run_test_openai():
    return await test_gemini()

@router.get("/")
async def root():
    return {"message": "Backend is up and running 🚀"}
