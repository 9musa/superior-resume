import os, io
import fitz, docx2txt
import json
from google import genai
from gemini import superiorise
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import Response
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import init_db_pool, get_pool, get_user_by_email, create_user, create_job, get_job, update_job_result
from security import hash_password, verify_password, create_access_token
from templates import render_resume_pdf, TEMPLATES
from dependencies import get_optional_user
import uuid


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool() # runs once, before startup

    yield

    pool = await get_pool() # runs on shutdown
    await pool.close()

app = FastAPI(lifespan=lifespan)


class AuthInput(BaseModel):
    email: str
    password:str


def validate(file_bytes: bytes, filename: str) -> tuple[bool, str]: # EXTENSION EXCEPTIONS
    ext = filename.split(".")[-1].lower()

    if ext == "pdf":
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            if doc.is_encrypted:
                return False, "PDF is password protected."
            if len(doc) == 0:
                return False, "PDF has no pages."

            text_check = "".join(doc[i].get_text() for i in range(min(2, len(doc))))
            if not text_check.strip():
                return False, "PDF has no readable text (likely a scanned image)."

            return True, "Valid PDF."
        except Exception as e:
            return False, f"Corrupted or invalid PDF structure, {str(e)}"

    elif ext == "docx":
        try:
            file_stream = io.BytesIO(file_bytes)
            text_check = docx2txt.process(file_stream)
            if not text_check.strip():
                return False, "DOCX file is empty."

            return True, "Valid DOCX."
        except Exception as e:
            return False, f"Corrupted or invalid DOCX structure: {str(e)}"

    return False, f"Unsupported file extension: .{ext}"

def extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.split(".")[-1].lower()

    if ext == "pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "".join([page.get_text() for page in doc]).strip()
        
    elif ext == "docx":
        file_stream = io.BytesIO(file_bytes)
        return docx2txt.process(file_stream).strip()
        
    return ""

async def superior_process(job_id: str, resume_text: str, job_desc: str):
    try:
        data = await superiorise(resume_text, job_desc)

        if not data.get("is_valid_resume", False):
            reason = data.get("rejection_reason", "The uploaded file doesn't appear to be a resume.")
            await update_job_result(job_id, status="failed", result_text=reason)
            return

        await update_job_result(job_id, status="done", result_text=json.dumps(data))
    except Exception as e:
        await update_job_result(job_id, status="failed", result_text=str(e))

@app.get("/")
def root():
    return {"status": "ok"} 

@app.post("/auth/signup")
async def signup(input: AuthInput):
    existing = await get_user_by_email(input.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.") # EMAIL EXCEPTION

    password_hash = hash_password(input.password)
    user_id = await create_user(input.email, password_hash)

    token = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login")
async def login(input: AuthInput):
    user = await get_user_by_email(input.email)
    if not user or not verify_password(input.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid email or password.") # EMAIL EXCEPTION

    token = create_access_token(str(user["id"]))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/superior")
async def superior_resume(
    background_tasks: BackgroundTasks,
    resume_file: UploadFile = File(),
    job_desc: str = Form(),
    user_id: Optional[str] = Depends(get_optional_user),
):
    file_bytes = await resume_file.read()
    is_valid, msg = validate(file_bytes, resume_file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg) # INVALID RESUME EXCEPTION

    parsed_text = extract_text(file_bytes, resume_file.filename)

    job_id = await create_job(job_desc, user_id, parsed_text) # optional user_id par

    background_tasks.add_task(superior_process, job_id, parsed_text, job_desc)
    
    return {"job_id": job_id, "status": "processing"}

@app.get("/superior/{job_id}")
async def get_superior_resume(job_id: str):
    job = await get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found") # JOB EXCEPTION

    job_dict = dict(job)
    job_dict.pop("result_pdf", None)
    return job_dict

@app.get("/superior/{job_id}/download")
async def download_resume(job_id: str, template: str = "classic"):
    job = await get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found") # JOB EXCEPTION
    if job["status"] != "done":
        raise HTTPException(status_code=400, detail=f"Job is not ready (status: {job['status']})") # JOB EXCEPTION
    if template not in TEMPLATES:
        raise HTTPException(status_code=400, detail=f"Unknown template. Choose from: {list(TEMPLATES.keys())}") # TEMPLATE EXCEPTION

    data = json.loads(job["result"])
    pdf_bytes = render_resume_pdf(data, template)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="resume_{template}.pdf"'},
    )