import os, io
import fitz, docx2txt
import json
from google import genai
from ai_providers import superiorise_with_fallback
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import init_db_pool, get_pool, get_user_by_email, create_user, create_job, get_job, update_job_result
from security import hash_password, verify_password, create_access_token
from templates import render_resume_pdf, TEMPLATES
from dependencies import get_optional_user
from exceptions import ResumeAppError, FileValidationError, NotAResumeError, JobNotFoundError, JobNotReadyError, AuthError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool() # runs once, before startup

    yield

    pool = await get_pool() # runs on shutdown
    await pool.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ResumeAppError)
async def resume_app_error_handler(request: Request, exc: ResumeAppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


class AuthInput(BaseModel):
    email: str
    password:str


def validate(file_bytes: bytes, filename: str) -> None:
    ext = filename.split(".")[-1].lower()

    if ext == "pdf":
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            raise FileValidationError(f"Corrupted or invalid PDF structure: {e}")

        if doc.is_encrypted:
            raise FileValidationError("PDF is password protected.")
        if len(doc) == 0:
            raise FileValidationError("PDF has no pages.")

        text_check = "".join(doc[i].get_text() for i in range(min(2, len(doc))))
        if not text_check.strip():
            raise FileValidationError("PDF has no readable text (likely a scanned image).")
        return

    elif ext == "docx":
        try:
            file_stream = io.BytesIO(file_bytes)
            text_check = docx2txt.process(file_stream)
        except Exception as e:
            raise FileValidationError(f"Corrupted or invalid DOCX structure: {e}")

        if not text_check.strip():
            raise FileValidationError("DOCX file is empty.")
        return

    raise FileValidationError(f"Unsupported file extension: .{ext}")

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
        data = await superiorise_with_fallback(resume_text, job_desc)

        if not data.get("is_valid_resume", False):
            reason = data.get("rejection_reason", "The uploaded file doesn't appear to be a resume.")
            raise NotAResumeError(reason)

        await update_job_result(job_id, status="done", result_text=json.dumps(data))

    except ResumeAppError as e:
        await update_job_result(job_id, status="failed", result_text=e.message)
    except Exception as e:
        await update_job_result(job_id, status="failed", result_text=f"Unexpected error: {e}")

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
    validate(file_bytes, resume_file.filename)

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