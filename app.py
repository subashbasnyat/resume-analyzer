from flask import Flask, render_template, request
import os
from resume_analyzer.document_parsing import DocumentParser # Import your custom DocumentParser class
import pandas as pd

# Flask app initialization
app = Flask(__name__)

# Load skills list from a CSV file
skills_df = pd.read_csv("data/skills_list.csv")  # Ensure the path to your CSV is correct
skills_list = skills_df['skill_name'].dropna().tolist()

# Initialize the DocumentParser with the skills list
parser = DocumentParser(skills_list)

# Configure file upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Render the main page with the upload form."""
    return render_template('index.html')


@app.route('/parse', methods=['POST'])
def parse_resume():
    """Handle resume upload, parsing, and skill analysis."""
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Save the uploaded file temporarily
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Parse the document and analyze skills
            similarity_scores = parser.analyze_resume(file_path)

            # Clean up the uploaded file
            os.remove(file_path)

            # Render results in the template
            return render_template('result.html', data=similarity_scores.to_dict(orient='records'))
        except Exception as e:
            return f"Error processing file: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)
