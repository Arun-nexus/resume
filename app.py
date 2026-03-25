from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

from src.groq_llm import model
from notebook.configuration_file import (
    extract_text_from_image,
    safe_parse,
    save_pickle,
    open_pickle
)
from src.recommendation import predicting
from logger import logging


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.getenv("groq_key"):
    raise Exception("GROQ_KEY not set")

os.makedirs("data", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("frontend/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h3>index.html not found</h3>"


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/resume_analysis")
async def resume_analyze(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
            raise HTTPException(status_code=400, detail="Invalid file type")

        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = f"data/{unique_name}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_image(file_path)
        save_pickle("data/text.pkl", text)

        prompt = """
        Extract:
        - Technical skills
        - Job role
        - Experience level

        Return JSON:
        {
          "skills": [],
          "role": "",
          "experience": ""
        }
        """

        response = model(resume_text=text, prompt=prompt)
        parsed = safe_parse(response)

        skills_str = ", ".join(parsed.get("skills", []))
        job_title = predicting(skills_str)

        return {
            "extracted": parsed,
            "recommended": job_title
        }

    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume_analysis/tell_me")
async def description():
    try:
        resume_data = open_pickle("data/text.pkl")

        response = model(resume_text=resume_data, prompt="Give summary, strengths, weaknesses, suggestions")

        return {"analysis": response}

    except Exception:
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/resume_analysis/percentage")
async def job_percentage(desired_job: str = Query(...)):
    try:
        resume_data = open_pickle("data/text.pkl")

        prompt = f"""
        Compare with role: {desired_job}

        Return JSON:
        {{
          "match_percentage": 0,
          "matching_skills": [],
          "missing_skills": [],
          "improvement_suggestions": []
        }}
        """

        response = model(resume_text=resume_data, prompt=prompt)
        parsed = safe_parse(response)

        return {
            "role": desired_job,
            "analysis": parsed
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Percentage failed")