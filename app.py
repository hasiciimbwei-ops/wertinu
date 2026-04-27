from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os, json, uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load questions from questions_database.json
with open('questions_database.json') as f:
    questions = json.load(f)

# Store quiz sessions in memory
quiz_sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/quiz/create', methods=['POST'])
def create_quiz():
    quiz_id = str(uuid.uuid4())
    quiz_sessions[quiz_id] = {'questions': [], 'answers': {}}
    return jsonify({'quiz_id': quiz_id}), 201

@app.route('/api/quiz/<quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    if quiz_id in quiz_sessions:
        return jsonify(questions), 200
    return jsonify({'error': 'Quiz not found'}), 404

@app.route('/api/quiz/<quiz_id>/submit', methods=['POST'])
def submit_answers(quiz_id):
    if quiz_id not in quiz_sessions:
        return jsonify({'error': 'Quiz not found'}), 404
    user_answers = request.json.get('answers')
    quiz_sessions[quiz_id]['answers'] = user_answers
    return jsonify({'message': 'Answers submitted successfully'}), 200

@app.route('/api/quiz/<quiz_id>/results', methods=['GET'])
def get_results(quiz_id):
    if quiz_id not in quiz_sessions:
        return jsonify({'error': 'Quiz not found'}), 404
    correct_answers = 0
    for question in questions:
        if question['id'] in quiz_sessions[quiz_id]['answers']:
            if quiz_sessions[quiz_id]['answers'][question['id']] == question['correct_answer']:
                correct_answers += 1
    score = (correct_answers / len(questions)) * 100
    return jsonify({'score': score}), 200

if __name__ == '__main__':
    app.run(debug=True)
