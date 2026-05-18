import pdfplumber
from docx import Document
import spacy
import re
import json
import os

# Load spaCy model for name extraction
nlp = spacy.load("en_core_web_sm")


class ResumeParser:
    """
    Main class for parsing resumes and extracting information.
    Handles both PDF and DOCX formats.
    """
    
    def __init__(self):
        # Common skills to look for - you can expand this list
        self.skills_list = [
            'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue',
            'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
            'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
            'Git', 'CI/CD', 'Jenkins', 'Linux', 'Bash',
            'HTML', 'CSS', 'TypeScript', 'Spring Boot', 'Hibernate',
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
            'Machine Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy',
            'C++', 'C#', 'Go', 'Rust', 'Ruby', 'PHP',
            'Swift', 'Kotlin', 'Android', 'iOS', 'Flutter', 'React Native'
        ]
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF using pdfplumber.
        Returns all text as a single string.
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def extract_text_from_docx(self, docx_path):
        """
        Extract text from DOCX using python-docx.
        Returns all text as a single string.
        """
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def extract_name(self, text):
        """
        Extract name using spaCy's NER (Named Entity Recognition).
        Usually the first PERSON entity found is the candidate's name.
        """
        doc = nlp(text[:1000])  # Check first 1000 chars (name is usually at the top)
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        
        # Fallback: Try to find name in first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            # Simple heuristic: name is usually 2-4 words, capitalized
            words = line.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                return line
        
        return "Unknown"
    
    def extract_skills(self, text):
        """
        Match skills from predefined list.
        Case-insensitive matching.
        """
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_list:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def extract_education(self, text):
        """
        Extract education information using pattern matching.
        Looks for degree keywords.
        """
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'B\.?Tech',
            r'B\.?E\.?',
            r'Bachelor',
            r'M\.?Tech',
            r'M\.?E\.?',
            r'Master',
            r'B\.?S\.?',
            r'M\.?S\.?',
            r'PhD',
            r'MBA'
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get surrounding context (about 50 chars after match)
                start = match.start()
                end = min(match.end() + 50, len(text))
                education.append(text[start:end].strip().split('\n')[0])
        
        return list(set(education))  # Remove duplicates
    
    def extract_experience(self, text):
        """
        Extract years of experience using regex patterns.
        Looks for patterns like "3 years", "5+ years experience", etc.
        """
        # Patterns to match experience
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'experience\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = match.group(1)
                return f"{years} years"
        
        # If no explicit years mentioned, check if "experience" section exists
        if re.search(r'experience', text, re.IGNORECASE):
            return "Experience mentioned (duration not specified)"
        
        return "Not specified"
    
    def parse_resume(self, file_path):
        """
        Main method to parse a resume file.
        Detects file type and extracts all information.
        """
        # Determine file type
        if file_path.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            return None
        
        if not text.strip():
            print(f"No text extracted from {file_path}")
            return None
        
        # Extract all information
        resume_data = {
            "filename": os.path.basename(file_path),
            "name": self.extract_name(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "keywords": self.extract_skills(text)  # For now, keywords = skills
        }
        
        return resume_data
    
    def save_to_json(self, data, output_file='parsed_data/resumes.json'):
        """
        Save parsed resume data to JSON file.
        Appends to existing data if file exists.
        """
        existing_data = []
        
        # Load existing data if file exists
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        
        # Append new data
        existing_data.append(data)
        
        # Save back to file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        print(f"Data saved to {output_file}")


# Example usage (for testing)
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with a resume file
    # resume_path = "resumes/sample_resume.pdf"
    # data = parser.parse_resume(resume_path)
    # 
    # if data:
    #     print("\nParsed Resume Data:")
    #     print(json.dumps(data, indent=2))
    #     parser.save_to_json(data)
    
    print("Parser module loaded successfully!")
    print("Use: parser.parse_resume('path/to/resume.pdf')")
