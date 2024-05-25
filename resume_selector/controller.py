import io
import re
from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from PyPDF2 import PdfReader

resume = APIRouter()

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        pdf_text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return pdf_text
    except Exception:
        raise HTTPException(status_code=500, detail="Error extracting text from PDF")

def extract_skills_section(pdf_text):
    try:
        skills_section_match = re.search(r'Technical Skills \s*([\s\S]*?)(?=\n[A-Z]|\Z)', pdf_text, re.DOTALL | re.IGNORECASE)
        if skills_section_match:
            return skills_section_match.group(1).strip()
        else:
            raise Exception("Skills section not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Error extracting skills section")

def process_skills(skills_section):
    try:
        return {"SKILLS": skills_section}
    except Exception:
        raise HTTPException(status_code=500, detail="Error processing skills section")

@resume.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        pdf_file = io.BytesIO(pdf_bytes)

        pdf_text = extract_text_from_pdf(pdf_file)
        skills_section = extract_skills_section(pdf_text)
        skills_dict = process_skills(skills_section)

        return skills_dict
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")