from flask import Flask, request, render_template
import os
import fitz  # pymupdf
from analyse_pdf import analyse_resume_gemini

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to extract text from resume
def extract_text_from_resume(pdf_path):
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get uploaded file
        file = request.files.get("resume")
        job_description = request.form.get("jobdesc", "")

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            resume_text = extract_text_from_resume(file_path)

            # Analyse resume
            result = analyse_resume_gemini(resume_text, job_description)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
