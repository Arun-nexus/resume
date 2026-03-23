from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

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

os.makedirs("data", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("frontend/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h3>index.html not found in 'frontend' folder</h3>"


@app.get("/health")
def health():
    return {"status": "running"}


@app.post("/resume_analysis")
async def resume_analyze(file: UploadFile = File(...)):
    try:
        logging.info(f"starting resume analyzer for {file.filename}")

        file_path = f"data/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_image(file_path)

        save_pickle("data/text.pkl", text)

        prompt = """
        You are an expert resume parser.

        Extract:
        - Technical skills
        - Job role
        - Experience level

        Return ONLY JSON:
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
        logging.error(f"Error in resume_analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resume_analysis/tell_me")
async def description():
    try:
        resume_data = open_pickle("data/text.pkl")

        prompt = """
        You are an expert career advisor.

        Based on the resume, provide:
        1. Professional summary (2-3 lines)
        2. Key strengths
        3. Weaknesses
        4. Career suggestions

        Rules:
        - Be concise
        - Use bullet points
        - No hallucination
        """

        response = model(resume_text=resume_data, prompt=prompt)

        return {"analysis": response}

    except Exception as e:
        logging.error(f"Error in tell_me: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.post("/resume_analysis/percentage")
async def job_percentage(desired_job: str):
    try:
        logging.info(f"percentage calculation started for {desired_job}")

        resume_data = open_pickle("data/text.pkl")

        prompt = f"""
        You are an expert resume evaluator.

        Compare candidate skills with role: {desired_job}

        Return STRICT JSON:
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

    except Exception as e:
        logging.error(f"Error in percentage analysis: {e}")
        raise HTTPException(status_code=500, detail="Percentage calculation failed")