from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from src.groq_llm import model
from notebook.configuration_file import (
    extract_text,
    safe_parse,
    setup_tesseract
)
from src.recommendation import predicting
from logger import logging


app = FastAPI()
setup_tesseract()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not os.getenv("groq_api_key"):
    raise Exception("GROQ_API_KEY not set")

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
        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
            raise HTTPException(status_code=400, detail="Invalid file type")

        contents = await file.read()


        text = extract_text(contents, file.filename)

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
        raise HTTPException(status_code=500, detail="Processing failed")


@app.post("/resume_analysis/tell_me")
async def description(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text(contents, file.filename)

        response = model(
            resume_text=text,
            prompt="Give summary, strengths, weaknesses, suggestions"
        )

        return {"analysis": response}

    except Exception:
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/resume_analysis/percentage")
async def job_percentage(
    file: UploadFile = File(...),
    desired_job: str = Query(...)
):
    try:
        contents = await file.read()
        text = extract_text(contents, file.filename)

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

        response = model(resume_text=text, prompt=prompt)
        parsed = safe_parse(response)

        return {
            "role": desired_job,
            "analysis": parsed
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Percentage failed")