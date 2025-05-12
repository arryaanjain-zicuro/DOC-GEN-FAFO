from fastapi import APIRouter, UploadFile, Form
from app.services.document_generator import generate_document

router = APIRouter()

@router.post("/generate/")
async def generate(term_sheet: UploadFile, template_name: str = Form(...)):
    output_path = generate_document(term_sheet.file, template_name)
    return {"status": "success", "path": output_path}
