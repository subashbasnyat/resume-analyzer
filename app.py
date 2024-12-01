from flask import Flask, render_template, request
import os
from process import ResumeProcessor
import pandas as pd

# Flask app initialization
app = Flask(__name__)

# Initialize the ResumeProcessor
processor = ResumeProcessor()

# Configure file upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Render the main page with the upload form."""
    return render_template('index.html')


@app.route('/parsing-result', methods=['POST'])
def parse_resume():
    """Handle resume and JD upload, parsing, and scoring."""
    if 'file' not in request.files or 'file2' not in request.files:
        return 'Resume or JD file is missing.', 400

    resume_file = request.files['file']
    jd_file = request.files['file2']

    if not resume_file or resume_file.filename == '':
        return 'No resume file selected.', 400
    if not jd_file or jd_file.filename == '':
        return 'No JD file selected.', 400

    # Save the uploaded files temporarily
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
    resume_file.save(resume_path)
    jd_file.save(jd_path)

    try:
        # Process the resume and JD
        scores = processor.process_resume(resume_path, jd_path)

        # Clean up the uploaded files
        os.remove(resume_path)
        os.remove(jd_path)

        # Render results in the template
        return render_template('result.html', data=scores)
    except Exception as e:
        return f"Error processing files: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
