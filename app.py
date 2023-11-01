import requests
from flask_cors import CORS  
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(500), nullable=False)
    interests = db.Column(db.String(200), nullable=False)
    draft_essay = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"Student('{self.resume}', '{self.interests}', '{self.draft_essay}')"

def create_student(data):
    resume = data['resume']
    interests = data['interests']
    draft_essay = data['draft_essay']

    student = Student(resume=resume, interests=interests, draft_essay=draft_essay)
    db.session.add(student)
    db.session.commit()
    return student

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    student = create_student(data)
    return {"message": "Data saved successfully", "student_id": student.id}, 200

@app.route('/submit_and_generate', methods=['POST'])
def submit_and_generate():
    data = request.json
    student = create_student(data)
    prompt = prepare_gpt3_prompt(student.id)
    generated_essay = call_gpt3(prompt)
    return {"message": "Success", "generated_essay": generated_essay}, 200

@app.route('/')
def index():
    return render_template('index.html')

def prepare_gpt3_prompt(student_id):
    student = Student.query.get_or_404(student_id)
    prompt = f"Student Resume: {student.resume}\n"
    prompt += f"Interests: {student.interests}\n"
    prompt += f"Draft Essay: {student.draft_essay}\n\n"
    prompt += "Please provide personalized recommendations for clubs, classes, and research areas."
    return prompt

def call_gpt3(prompt):
    api_key = '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'  # Hardcoded API key
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text'].strip()

if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(500)
def internal_error(error):
    print(f"Server Error: {error}")
    return "Internal Server Error", 500