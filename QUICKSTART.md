# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Verify Installation

```bash
python test_setup.py
```

You should see all tests passing ✓

## Usage

### Option 1: Use the Flask API (Recommended)

```bash
# Start the server
python app.py
```

Then use any of these methods to interact:

**Using curl (Terminal):**
```bash
# Upload a resume
curl -X POST -F "file=@resumes/sample.pdf" http://127.0.0.1:5000/upload

# Search for Python developers
curl "http://127.0.0.1:5000/search?keyword=python"

# Get all resumes
curl "http://127.0.0.1:5000/resumes"
```

**Using Postman:**
1. Open Postman
2. Create POST request to `http://127.0.0.1:5000/upload`
3. Body → form-data → Key: `file` (type: File) → Select resume
4. Send

### Option 2: Use Python Directly

```python
from parser import ResumeParser
from search import ResumeSearch

# Parse a resume
parser = ResumeParser()
data = parser.parse_resume("resumes/sample.pdf")
print(data)

# Save it
parser.save_to_json(data)

# Search
searcher = ResumeSearch()
results = searcher.search_by_keyword("python")
searcher.display_results(results)
```

## Testing Without Real Resumes

Create a simple text file and save as PDF:

```
John Doe
john@email.com | 123-456-7890

EXPERIENCE
Software Engineer at TechCorp
3 years of experience in backend development

SKILLS
Python, Django, Flask, PostgreSQL, Docker, React, JavaScript

EDUCATION
B.Tech Computer Science
XYZ University (2018-2022)
```

Save as `resumes/john_doe.pdf` and upload!

## Common Issues

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Port 5000 in use:**
Edit `app.py` and change port to 8000:
```python
app.run(debug=True, port=8000)
```

**No resumes showing:**
Make sure you've uploaded at least one resume via the `/upload` endpoint first.

## What to Show in Your Demo

1. **Upload** 2-3 sample resumes
2. **Search** for a skill: `curl "http://127.0.0.1:5000/search?keyword=python"`
3. **Filter** by experience: `curl "http://127.0.0.1:5000/search/experience?years=3"`
4. **Show stats**: `curl "http://127.0.0.1:5000/stats"`
5. **Explain** the code structure and how each module works

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: Resume Parser & Keyword Search System"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Good luck with your internship! 🚀
