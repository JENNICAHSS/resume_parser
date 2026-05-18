# Resume Parser & Keyword Search System

A Python-based ATS (Applicant Tracking System) style resume parser that extracts structured information from resumes and provides keyword-based search functionality.

## Features

- 📄 Parse PDF and DOCX resumes
- 🔍 Extract key information (Name, Skills, Experience, Education)
- 💾 Store parsed data in JSON format
- 🔎 Keyword-based search across all resumes
- 🎯 Skill-specific search
- ⏱️ Experience-based filtering
- 🚀 REST API built with Flask
- 📊 Resume statistics dashboard

## Tech Stack

- **Python 3.8+**
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX parsing
- **spaCy** - NLP for name extraction
- **Flask** - REST API framework
- **JSON** - Data storage

## Project Structure

```
resume-parser/
│
├── resumes/              # Upload your resume files here
├── parsed_data/          # Parsed JSON data stored here
│   └── resumes.json
├── parser.py             # Core parsing logic
├── search.py             # Search functionality
├── app.py                # Flask API
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── sample_output.json    # Example output format
```

## Installation

### 1. Clone or download this project

```bash
cd resume-parser
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Running the Flask API

Start the server:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

### API Endpoints

#### 1. Upload Resume

**Endpoint:** `POST /upload`

Upload a PDF or DOCX resume file.

**Using curl:**
```bash
curl -X POST -F "file=@resumes/sample_resume.pdf" http://127.0.0.1:5000/upload
```

**Using Postman:**
- Method: POST
- URL: http://127.0.0.1:5000/upload
- Body: form-data
- Key: file (type: File)
- Value: Select your resume file

**Response:**
```json
{
  "message": "Resume uploaded and parsed successfully",
  "data": {
    "filename": "sample_resume.pdf",
    "name": "John Doe",
    "skills": ["Python", "React", "Django"],
    "education": ["B.Tech Computer Science"],
    "experience": "3 years",
    "keywords": ["Python", "React", "Django"]
  }
}
```

#### 2. Search by Keyword

**Endpoint:** `GET /search?keyword=python`

Search across all resume fields.

```bash
curl "http://127.0.0.1:5000/search?keyword=python"
```

**Response:**
```json
{
  "keyword": "python",
  "count": 2,
  "results": [...]
}
```

#### 3. Search by Skill

**Endpoint:** `GET /search/skill?skill=React`

Search specifically in the skills field.

```bash
curl "http://127.0.0.1:5000/search/skill?skill=React"
```

#### 4. Search by Experience

**Endpoint:** `GET /search/experience?years=3`

Filter resumes by minimum years of experience.

```bash
curl "http://127.0.0.1:5000/search/experience?years=3"
```

#### 5. Get All Resumes

**Endpoint:** `GET /resumes`

Retrieve all parsed resumes.

```bash
curl "http://127.0.0.1:5000/resumes"
```

#### 6. Get Statistics

**Endpoint:** `GET /stats`

Get insights about parsed resumes.

```bash
curl "http://127.0.0.1:5000/stats"
```

**Response:**
```json
{
  "total_resumes": 5,
  "top_skills": {
    "Python": 3,
    "React": 2,
    "Docker": 2
  },
  "total_unique_skills": 25
}
```

### Using as a Python Module

You can also use the parser and search modules directly in Python:

```python
from parser import ResumeParser
from search import ResumeSearch

# Parse a resume
parser = ResumeParser()
data = parser.parse_resume("resumes/sample_resume.pdf")
parser.save_to_json(data)

# Search resumes
searcher = ResumeSearch()
results = searcher.search_by_keyword("python")
searcher.display_results(results)
```

## Example Workflow

1. **Upload resumes:**
   ```bash
   curl -X POST -F "file=@resumes/john_doe.pdf" http://127.0.0.1:5000/upload
   curl -X POST -F "file=@resumes/jane_smith.docx" http://127.0.0.1:5000/upload
   ```

2. **Search for Python developers:**
   ```bash
   curl "http://127.0.0.1:5000/search?keyword=python"
   ```

3. **Find candidates with React skills:**
   ```bash
   curl "http://127.0.0.1:5000/search/skill?skill=React"
   ```

4. **Filter by experience:**
   ```bash
   curl "http://127.0.0.1:5000/search/experience?years=3"
   ```

## How It Works

### 1. Resume Parsing (`parser.py`)

- **Text Extraction:** Reads PDF/DOCX files and extracts raw text
- **Name Extraction:** Uses spaCy's NER to identify person names
- **Skills Matching:** Compares against a predefined skills list
- **Education Parsing:** Regex patterns to find degree information
- **Experience Extraction:** Regex to find years of experience
- **JSON Storage:** Saves structured data for later searching

### 2. Search Functionality (`search.py`)

- **Keyword Search:** Case-insensitive search across all fields
- **Skill Search:** Targeted search in skills array
- **Experience Filter:** Numeric filtering by years
- **Multiple Keywords:** AND logic for complex queries

### 3. API Layer (`app.py`)

- **File Upload:** Handles resume uploads with validation
- **REST Endpoints:** Exposes search functionality via HTTP
- **Error Handling:** Returns appropriate status codes
- **CORS Support:** Enables frontend integration

## Customization

### Adding More Skills

Edit the `skills_list` in `parser.py`:

```python
self.skills_list = [
    'Python', 'Java', 'JavaScript',
    # Add your skills here
    'YourSkill1', 'YourSkill2'
]
```

### Improving Name Extraction

Modify `extract_name()` in `parser.py` to use different heuristics or more advanced NLP.

### Custom Search Logic

Add new search methods in `search.py` for specialized queries.

## Limitations & Future Improvements

**Current Limitations:**
- Skills matching is based on predefined list
- Experience extraction relies on specific patterns
- No fuzzy matching (exact keyword matches only)
- Single-threaded processing

**Potential Improvements:**
- Add ML-based skill extraction
- Implement fuzzy search (Levenshtein distance)
- Add database support (SQLite/PostgreSQL)
- Support for more file formats
- Batch processing for multiple resumes
- Web frontend dashboard
- Email extraction
- Phone number extraction
- Location/Address parsing

## Testing

### Manual Testing

1. Place sample resumes in `resumes/` folder
2. Run the Flask app
3. Use Postman or curl to test endpoints
4. Check `parsed_data/resumes.json` for results

### Sample Test Resume

Create a simple text file saved as PDF with this content:

```
John Doe
Software Engineer

Experience: 3 years of experience in full-stack development

Skills:
Python, Django, Flask, React, JavaScript, PostgreSQL, Docker, Git

Education:
B.Tech Computer Science, XYZ University (2018-2022)
```

## Troubleshooting

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: PDF not parsing correctly**
- Check if PDF is text-based (not scanned image)
- Try converting to DOCX format

**Issue: Skills not detected**
- Verify skills are in the predefined list
- Check spelling and capitalization

**Issue: Port 5000 already in use**
```python
# In app.py, change the port:
app.run(debug=True, port=8000)
```

## Contributing

Feel free to fork this project and submit pull requests. Some areas that need work:
- Better name extraction algorithms
- Support for more resume formats
- ML-based information extraction
- Frontend UI

## License

This project is open-source and available for educational purposes.

## Author

Built as an internship project to demonstrate backend development skills with Python, NLP, and REST APIs.

---

**Note:** This is a learning project. For production use, consider adding authentication, database integration, better error handling, and comprehensive testing.
