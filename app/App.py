from flask import Flask, request, jsonify
from s3_utils import upload_to_s3, list_resumes_in_s3, download_resume_from_s3
from resume_parser import extract_text_from_pdf_bytes
from Matcher import get_resume_score
import json

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file found"}), 400

    file = request.files['resume']
    upload_to_s3(file, file.filename)
    return jsonify({"message": f"{file.filename} uploaded successfully"})

@app.route('/match-all', methods=['POST'])
def match_all_resumes():
    job_description = request.form.get('job')
    if not job_description:
        return jsonify({"error": "Missing job description"}), 400

    results = []
    for key in list_resumes_in_s3():
        pdf_bytes = download_resume_from_s3(key)
        resume_text = extract_text_from_pdf_bytes(pdf_bytes)

        try:
            result = get_resume_score(resume_text, job_description)  # FIXED: no json.loads
        except Exception as e:
            result = {"score": 0, "reasoning": f"Failed to score: {str(e)}"}

        results.append({
            "filename": key,
            "score": result.get("score", 0),
            "reasoning": result.get("reasoning", "")
        })

    best_resume = max(results, key=lambda r: r['score'])
    return jsonify({"best_match": best_resume, "all_results": results})

if __name__ == '__main__':
    app.run(debug=True)