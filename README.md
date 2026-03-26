# 📄 AI Resume Analyzer & Job Recommendation System

An end-to-end AI system that extracts information from resumes, analyzes skills using LLMs, and recommends relevant jobs with performance insights.

---

## 🚀 Overview

This project allows users to upload their resume via a web interface. The system:

1. Extracts text from the resume using OCR (Tesseract)
2. Uses LLM (Groq API) to identify skills and key sections
3. Applies a recommendation system to suggest relevant jobs
4. Generates professional insights and job-match analysis

---

## ✨ Features

* 📄 Resume upload via web interface
* 🔍 OCR-based text extraction (PyTesseract)
* 🧠 Skill & section extraction using LLM (Groq)
* 🎯 Job recommendation system
* 📊 AI-generated professional insights
* ⚡ FastAPI backend
* 🐳 Docker support

---

## 🏗️ Architecture

```text
User (Web UI)
        ↓
Resume Upload
        ↓
OCR (PyTesseract)
        ↓
Text Extraction
        ↓
Groq LLM (Skill + Section Parsing)
        ↓
Recommendation System
        ↓
Insights + Job Match Output
```

---

## ⚙️ Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: FastAPI
* **ML/NLP**:

  * PyTesseract (OCR)
  * Custom Recommendation System
  * LLM (Groq API)
* **Data**: CSV + embeddings (pickle files)
* **Database**: MongoDB
* **Deployment**: Docker

---

## 📦 Project Structure

```bash
.
├── app.py
├── dockerfile
├── requirement.txt
├── data/
│   ├── dataset.csv
│   ├── embedded_skills.pkl
│   └── label.pkl
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── src/
│   ├── data_access.py
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── data_validation.py
│   ├── groq_llm.py
│   └── recommendation.py
├── mongodb/
├── logs/
└── notebook/
```

---

## 🧪 How It Works

1. User uploads resume (PDF/Image)
2. PyTesseract extracts raw text
3. Groq LLM processes text:

   * Extracts skills
   * Identifies sections (education, experience, etc.)
4. Recommendation system:

   * Matches skills with job dataset
   * Suggests relevant roles
5. Groq generates:

   * Professional insights
   * Job performance match

---

## 🔧 Setup & Installation

### 1. Clone repository

```bash
git clone https://github.com/Arun-nexus/resume.git
cd resume
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Install Tesseract (IMPORTANT)

```bash
sudo apt install tesseract-ocr
```

### 5. Run backend

```bash
uvicorn app:app --reload
```

---

## 🐳 Docker Setup

```bash
docker build -t resume-analyzer .
docker run -p 8000:8000 resume-analyzer
```

---

## 🔑 Environment Variables

```env
groq_api_key=YOUR_API_KEY
```

---

## ⚠️ Known Issues & Limitations

* OCR accuracy depends on resume quality
* LLM output may vary slightly
* Recommendation quality depends on dataset
* Requires Tesseract installation on system

---

## 🔐 Security Considerations

* Do not expose API keys
* Use environment variables
* Avoid uploading sensitive resumes in production

---

## 📈 Future Improvements

* Replace OCR with better document parser (PDF-native)
* Improve recommendation model (semantic matching)
* Add user dashboard & history
* Deploy with scalable architecture
* Add authentication system

---

## 🎯 Learning Outcomes

* Built an end-to-end AI pipeline
* Integrated OCR + LLM + Recommendation system
* Designed full-stack ML application
* Worked with real-world deployment challenges

---

## 🧑‍💻 Author

Arun
Aspiring AI/ML Engineer

---
