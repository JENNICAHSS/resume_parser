import json
import os


class ResumeSearch:
    """
    Search through parsed resumes using keywords.
    Supports case-insensitive matching across all fields.
    """
    
    def __init__(self, data_file='parsed_data/resumes.json'):
        self.data_file = data_file
        self.resumes = self.load_resumes()
    
    def load_resumes(self):
        """
        Load all parsed resumes from JSON file.
        """
        if not os.path.exists(self.data_file):
            print(f"No data file found at {self.data_file}")
            return []
        
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error reading JSON file")
            return []
    
    def search_by_keyword(self, keyword):
        """
        Search resumes by keyword.
        Looks in: name, skills, education, experience, keywords
        Case-insensitive matching.
        """
        keyword = keyword.lower()
        results = []
        
        for resume in self.resumes:
            # Check in all text fields
            name = resume.get('name', '').lower()
            skills = ' '.join(resume.get('skills', [])).lower()
            education = ' '.join(resume.get('education', [])).lower()
            experience = resume.get('experience', '').lower()
            keywords = ' '.join(resume.get('keywords', [])).lower()
            
            # Combine all searchable text
            searchable_text = f"{name} {skills} {education} {experience} {keywords}"
            
            if keyword in searchable_text:
                results.append(resume)
        
        return results
    
    def search_by_skill(self, skill):
        """
        Search specifically in skills field.
        More precise than general keyword search.
        """
        skill = skill.lower()
        results = []
        
        for resume in self.resumes:
            skills = [s.lower() for s in resume.get('skills', [])]
            if skill in skills or any(skill in s for s in skills):
                results.append(resume)
        
        return results
    
    def search_by_experience(self, min_years):
        """
        Filter resumes by minimum years of experience.
        """
        results = []
        
        for resume in self.resumes:
            exp_text = resume.get('experience', '')
            
            # Try to extract number from experience string
            import re
            match = re.search(r'(\d+)', exp_text)
            
            if match:
                years = int(match.group(1))
                if years >= min_years:
                    results.append(resume)
        
        return results
    
    def search_multiple_keywords(self, keywords):
        """
        Search for multiple keywords (AND logic).
        Resume must match ALL keywords to be returned.
        """
        if not keywords:
            return []
        
        # Start with results from first keyword
        results = set(range(len(self.resumes)))
        
        for keyword in keywords:
            keyword_results = self.search_by_keyword(keyword)
            keyword_indices = {self.resumes.index(r) for r in keyword_results}
            results &= keyword_indices  # Intersection
        
        return [self.resumes[i] for i in results]
    
    def get_all_resumes(self):
        """
        Return all parsed resumes.
        """
        return self.resumes
    
    def get_resume_count(self):
        """
        Return total number of resumes.
        """
        return len(self.resumes)
    
    def display_results(self, results):
        """
        Pretty print search results.
        """
        if not results:
            print("\nNo resumes found matching your criteria.")
            return
        
        print(f"\n✓ Found {len(results)} matching resume(s):\n")
        
        for i, resume in enumerate(results, 1):
            print(f"{i}. {resume.get('name', 'Unknown')}")
            print(f"   Skills: {', '.join(resume.get('skills', [])[:5])}")  # Show first 5
            print(f"   Experience: {resume.get('experience', 'Not specified')}")
            print(f"   Education: {', '.join(resume.get('education', [])[:2])}")  # Show first 2
            print(f"   File: {resume.get('filename', 'Unknown')}")
            print()


# Example usage (for testing)
if __name__ == "__main__":
    searcher = ResumeSearch()
    
    print(f"Loaded {searcher.get_resume_count()} resumes")
    
    # Example searches
    # results = searcher.search_by_keyword("python")
    # searcher.display_results(results)
    
    # results = searcher.search_by_skill("React")
    # searcher.display_results(results)
    
    # results = searcher.search_by_experience(3)
    # searcher.display_results(results)
    
    print("\nSearch module loaded successfully!")
    print("Use: searcher.search_by_keyword('python')")
