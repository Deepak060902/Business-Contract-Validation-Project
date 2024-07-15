import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from src.backend.services.pdf_parser import parse_pdf
from src.backend.services.text_classifier import classify_text
from src.backend.services.deviation_detector import detect_deviations
from src.backend.services.pdf_highlighter import generate_pdf
from src.backend.services.summarizer import summarize_contract
import base64


router = APIRouter()

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...), file1: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    if not file1.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    contract = await file.read()
    template = await file1.read()
    try:
        contract_text = parse_pdf(contract)
        template_text = parse_pdf(template)
        contract_clauses = classify_text(contract_text)
        template_clauses = classify_text(template_text )
        deviations = detect_deviations(contract_clauses, template_clauses)
        pdf_path = generate_pdf(contract_clauses, deviations)
        summary = summarize_contract(contract_text)
    
        if os.path.exists(pdf_path):

            with open(pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()
            
            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            return JSONResponse(content={
                "pdf": pdf_base64,
                "summary": summary
            })

        else:
            raise HTTPException(status_code=500, detail="Generated PDF not found")

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
