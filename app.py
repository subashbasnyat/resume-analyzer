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

# Store parsed resume data in memory (or use a more permanent solution)
analysis = {}

@app.route('/')
def index():
    """Render the main page with the upload form."""
    return render_template('index.html')


@app.route('/parsing-result', methods=['POST'])
def parse_resumes():
    """Handle multiple resumes and a single JD upload, parsing, and scoring."""
    if 'resumes' not in request.files or 'job_description' not in request.files:
        return 'Resumes or JD file is missing.', 400

    resumes = request.files.getlist('resumes')
    jd_file = request.files['job_description']

    if not jd_file or jd_file.filename == '':
        return 'No JD file selected.', 400
    if not resumes or len(resumes) == 0:
        return 'No resumes selected.', 400

    # Save the JD file temporarily
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
    jd_file.save(jd_path)

    try:
        for resume_file in resumes:
            if resume_file.filename == '':
                continue

            # Save each resume file temporarily
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(resume_path)

            # Process each resume against the JD
            scores = processor.process_resume(resume_path, jd_path)
            analysis[resume_file.filename] = scores

            # Clean up the uploaded resume file
            os.remove(resume_path)

        # Clean up the JD file
        os.remove(jd_path)

        sorted_results = dict(sorted(analysis.items(), key=lambda item: item[1]['total_score'], reverse=True))
        print("SORTED RESULTS", sorted_results)
        # Render results in the template
        return render_template('result.html', results=sorted_results)
    except Exception as e:
        return f"Error processing files: {e}", 500


@app.route('/details')
def resume_details():
    """Display detailed analysis for a specific resume."""
    resume_name = request.args.get('resume')

    if not resume_name:
        return "Resume not specified.", 400
    print("ANALYSIS", analysis)
    resume_data = analysis.get(resume_name)

    if not resume_data:
        return "Resume details not found.", 404

    # Pass data to the template
    return render_template('detail.html', data=resume_data)


if __name__ == '__main__':
    app.run(debug=True)
