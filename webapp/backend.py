
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from adaptive_trainer import TeachingAgent, QuizAgent, FeedbackAgent
from memory_store import store_learning_memory, retrieve_related_memory

app = Flask(__name__)
CORS(app)

@app.route('/api/lesson-quiz', methods=['POST'])
def lesson_quiz():
    data = request.json
    topic = data.get('topic', '')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    # Retrieve past feedback for weak points
    past_feedbacks = retrieve_related_memory(topic)
    past_weaknesses = ''
    if past_feedbacks and past_feedbacks[0]:
        past_weaknesses = extract_weak_points(' '.join(past_feedbacks[0]))
    # Generate lesson and quiz
    teacher = TeachingAgent(
        name="Teacher",
        role="Explains topics",
        goal="Help the user understand a topic clearly.",
        backstory="An expert tutor known for simplifying complex subjects."
    )
    lesson = teacher.run(topic, past_weaknesses)
    quizzer = QuizAgent(
        name="Quizzer",
        role="Creates quizzes",
        goal="Evaluate learning through MCQs.",
        backstory="A quiz master who loves to challenge students."
    )
    quiz = quizzer.run(topic)
    return jsonify({'lesson': lesson, 'quiz': quiz})

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    topic = data.get('topic', '')
    answers = data.get('answers', '')
    quiz = data.get('quiz', '')
    if not (topic and answers and quiz):
        return jsonify({'error': 'Missing data'}), 400
    evaluator = FeedbackAgent(
        name="Evaluator",
        role="Gives feedback",
        goal="Identify mistakes and improve learning.",
        backstory="A guide who helps clarify confusing answers."
    )
    feedback = evaluator.run(topic, answers, quiz)
    store_learning_memory(topic, feedback, answers)
    # Also return related memory
    memory = retrieve_related_memory(topic)
    return jsonify({'feedback': feedback, 'memory': memory})

def extract_weak_points(feedback_text):
    lines = feedback_text.split("\n")
    weak_points = [line for line in lines if "incorrect" in line.lower()]
    return "\n".join(weak_points)

if __name__ == '__main__':
    app.run(debug=True)
