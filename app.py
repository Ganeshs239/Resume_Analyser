from flask import Flask, render_template, request
import pandas as pd
import re
from PyPDF2 import PdfReader
import docx
from datetime import datetime
import os

app = Flask(__name__)

# Load job dataset
data_path = "dataset.csv"
jobs_df = pd.read_csv(data_path)

# Utility functions
def extract_skills(resume_text):
    """
    Extract skills from the resume text using a predefined skill list.
    Ensure extracted skills are returned in the original format from the dataset.
    """
    predefined_skills = {
        skill.strip(): skill.strip()  # Create a mapping of original skill to itself
        for skills in jobs_df["Required Skills"]
        for skill in skills.split(",")
    }
    extracted_skills = [
        predefined_skills[skill]  # Return the skill in its original format
        for skill in predefined_skills
        if re.search(skill, resume_text, re.IGNORECASE)
    ]
    return list(set(extracted_skills))  # Remove duplicates and return


def match_jobs(extracted_skills):
    """
    Match extracted skills with jobs in the dataset.
    Return the jobs sorted by the number of matching skills with proper percentages.
    """
    extracted_skills_set = set(extracted_skills)
    job_matches = []

    for _, row in jobs_df.iterrows():
        required_skills = [skill.strip() for skill in row["Required Skills"].split(",")]
        required_skills_set = set(required_skills)
        matching_skills = required_skills_set.intersection(extracted_skills_set)
        
        if matching_skills:
            match_count = len(matching_skills)
            total_required = len(required_skills)
            match_percentage = round((match_count / total_required) * 100) if total_required > 0 else 0
            
            job_matches.append({
                "Job Title": row["Job Title"],
                "Industry": row["Industry"],
                "Required Skills": required_skills,
                "Matching Skills": list(matching_skills),
                "Match Count": match_count,
                "Total Required": total_required,
                "Match Percentage": match_percentage
            })

    # Sort the job matches by match percentage (descending), then by match count
    return sorted(job_matches, key=lambda x: (x["Match Percentage"], x["Match Count"]), reverse=True)

def read_file_content(file):
    """
    Reads the content of the uploaded file. Supports TXT, PDF, and DOCX formats.
    """
    filename = file.filename.lower()
    if filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif filename.endswith('.pdf'):
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format. Please upload a TXT, PDF, or DOCX file.")

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files:
            return render_template('error.html', error_message="Please upload a resume file.")

        # Read uploaded resume
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return render_template('error.html', error_message="No file selected. Please choose a file to upload.")
        
        try:
            resume_text = read_file_content(resume_file)
        except Exception as e:
            return render_template('error.html', error_message=f"Error processing file: {str(e)}")

        # Check if resume text is empty
        if not resume_text.strip():
            return render_template('error.html', error_message="The uploaded file appears to be empty or unreadable.")

        # Extract skills and match jobs
        extracted_skills = extract_skills(resume_text)
        job_matches = match_jobs(extracted_skills)

        # Calculate statistics
        total_skills_found = len(extracted_skills)
        total_jobs_matched = len(job_matches)
        analysis_timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

        return render_template('result.html', 
                             job_matches=job_matches, 
                             skills=extracted_skills,
                             total_skills_found=total_skills_found,
                             total_jobs_matched=total_jobs_matched,
                             analysis_timestamp=analysis_timestamp)
    
    except Exception as e:
        return render_template('error.html', error_message=f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)