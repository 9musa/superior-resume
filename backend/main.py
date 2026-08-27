import os, io
import fitz, docx2txt
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from database import init_db_pool, get_pool, get_user_by_email, create_user
from security import hash_password, verify_password, create_access_token
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


def validate(file_bytes: bytes, filename: str) -> tuple[bool, str]:
    ext = filename.split(".")[-1].lower()

    if ext == "pdf":
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            if doc.is_encrypted:
                return False, "PDF is password protected."
            if len(doc) == 0:
                return False, "PDF has no pages."

            text_check = "".join([page.get_text() for page in doc[:2]])
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


@app.get("/")
def root():
    return {"status": "ok"} 

@app.post("/auth/signup")
async def signup(input: AuthInput):
    existing = await get_user_by_email(input.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    password_hash = hash_password(input.password)
    user_id = await create_user(input.email, password_hash)

    token = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login")
async def login(input: AuthInput):
    user = await get_user_by_email(input.email)
    if not user or not verify_password(input.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    token = create_access_token(str(user["id"]))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/superior")
async def enhanceResume(
    resume_file: UploadFile = File(),
    job_title: str = Form(),
):
    file_bytes = await resume_file.read()
    is_valid, msg = validate(file_bytes, resume_file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    parsed_text = extract_text(file_bytes, resume_file.filename)
    

    job_id = str(uuid.uuid4()) # temporary uuid for guests, will be saved on DB
    
    return {"job_id": job_id, "status": "processing"}

@app.get("/superior/{job_id}")
def get_superior_resume():
    return