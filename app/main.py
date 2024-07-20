from flask import Blueprint, request, jsonify, render_template
from .parser import parse_resume

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        extracted_data = parse_resume(resume)
        if 'error' in extracted_data:
            return render_template('index.html', error=extracted_data['error'])
        return render_template('index.html', data=extracted_data)
    return render_template('index.html')

@main.route('/api/parse_resume', methods=['POST'])
def api_parse_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    resume = request.files['resume']
    
    if resume.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    extracted_data = parse_resume(resume)
    
    return jsonify(extracted_data)

