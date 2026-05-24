from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from parser import ResumeParser
from search import ResumeSearch

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
UPLOAD_FOLDER = 'resumes'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('parsed_data', exist_ok=True)

# Initialize parser and searcher
parser = ResumeParser()
searcher = ResumeSearch()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    """Simple home endpoint"""
    return jsonify({
        "message": "Resume Parser API",
        "endpoints": {
            "upload": "POST /upload",
            "search": "GET /search?keyword=python",
            "search_skill": "GET /search/skill?skill=React",
            "search_experience": "GET /search/experience?years=3",
            "all_resumes": "GET /resumes",
            "open_resume": "GET /resume/<filename>"
        }
    })


@app.route('/upload', methods=['POST'])
def upload_resume():
    """
    Upload and parse a resume file.
    Accepts PDF or DOCX files.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and DOCX files are allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        parsed_data = parser.parse_resume(filepath)
        
        if not parsed_data:
            return jsonify({"error": "Failed to parse resume"}), 500
        
        parser.save_to_json(parsed_data)
        
        global searcher
        searcher = ResumeSearch()
        
        return jsonify({
            "message": "Resume uploaded and parsed successfully",
            "data": parsed_data
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ NEW ENDPOINT — Opens the original resume file in the browser
@app.route('/resume/<filename>', methods=['GET'])
def open_resume(filename):
    """
    Open and display the original resume file in the browser.
    Example: /resume/john_doe.pdf
    """
    try:
        return send_from_directory(
            os.path.abspath(app.config['UPLOAD_FOLDER']),
            filename
        )
    except Exception as e:
        return jsonify({"error": f"File not found: {filename}"}), 404


@app.route('/search', methods=['GET'])
def search_resumes():
    """Search resumes by keyword."""
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return jsonify({"error": "Please provide a keyword parameter"}), 400
    
    results = searcher.search_by_keyword(keyword)
    
    return jsonify({
        "keyword": keyword,
        "count": len(results),
        "results": results
    })


@app.route('/search/skill', methods=['GET'])
def search_by_skill():
    """Search resumes specifically by skill."""
    skill = request.args.get('skill', '')
    
    if not skill:
        return jsonify({"error": "Please provide a skill parameter"}), 400
    
    results = searcher.search_by_skill(skill)
    
    return jsonify({
        "skill": skill,
        "count": len(results),
        "results": results
    })


@app.route('/search/experience', methods=['GET'])
def search_by_experience():
    """Search resumes by minimum years of experience."""
    try:
        years = int(request.args.get('years', 0))
    except ValueError:
        return jsonify({"error": "Years must be a number"}), 400
    
    results = searcher.search_by_experience(years)
    
    return jsonify({
        "min_years": years,
        "count": len(results),
        "results": results
    })


@app.route('/resumes', methods=['GET'])
def get_all_resumes():
    """Get all parsed resumes."""
    resumes = searcher.get_all_resumes()
    
    return jsonify({
        "total": len(resumes),
        "resumes": resumes
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about parsed resumes."""
    resumes = searcher.get_all_resumes()
    
    all_skills = []
    for resume in resumes:
        all_skills.extend(resume.get('skills', []))
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    
    return jsonify({
        "total_resumes": len(resumes),
        "top_skills": dict(skill_counts.most_common(10)),
        "total_unique_skills": len(set(all_skills))
    })


if __name__ == '__main__':
    print("🚀 Resume Parser API is starting...")
    print("📁 Upload folder:", UPLOAD_FOLDER)
    print("💾 Data folder: parsed_data")
    print("\nAPI Endpoints:")
    print("  POST   /upload")
    print("  GET    /resume/<filename>  ← NEW: Opens original resume")
    print("  GET    /search?keyword=python")
    print("  GET    /search/skill?skill=React")
    print("  GET    /search/experience?years=3")
    print("  GET    /resumes")
    print("  GET    /stats")
    print("\n✅ Server running on http://127.0.0.1:5000\n")
    
    app.run(debug=True, port=5000)
