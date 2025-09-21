import streamlit as st
from crewai import Agent
from memory_store import store_learning_memory, retrieve_related_memory

# Gemini model configuration
import os
import google.generativeai as genai
GEMINI_API_KEY =  "AIzaSyCL2sH4zH8H191xqYuRdzgwzRh8vix2Kw0"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Agent Definitions
class TeachingAgent(Agent):
    def run(self, topic, memory_points=None):
        if memory_points:
            prompt = (
                f"Teach the topic '{topic}' with a focus on helping the learner understand the following weak points:\n"
                f"{memory_points}\nMake it clear and beginner-friendly."
            )
        else:
            prompt = f"Teach the topic '{topic}' in a clear and beginner-friendly way."
        return self.query_llm(prompt)

    def query_llm(self, prompt):
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)


class QuizAgent(Agent):
    def run(self, topic):
        prompt = (
            f"Generate 2 multiple-choice questions (MCQs) for the topic '{topic}'. "
            f"Each question must have 4 options (A, B, C, D) formatted clearly:\n\n"
            f"1. Question?\nA. ...\nB. ...\nC. ...\nD. ...\n\n"
            f"2. Question?\nA. ...\nB. ...\nC. ...\nD. ..."
        )
        return self.query_llm(prompt)

    def query_llm(self, prompt):
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)


class FeedbackAgent(Agent):
    def run(self, topic, answers, quiz):
        prompt = (
            f"Topic: {topic}\n\n"
            f"Here are the quiz questions:\n{quiz}\n\n"
            f"User's answers:\n{answers}\n\n"
            f"Please evaluate each answer. If incorrect, explain why and include the correct concept briefly."
        )
        return self.query_llm(prompt)

    def query_llm(self, prompt):
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)

# --- Streamlit App ---

st.set_page_config(page_title="Adaptive Education Trainer", layout="centered")
st.title("🎓 Adaptive Education Trainer")
st.caption("Powered by CrewAI + OpenAI + ChromaDB")

if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""
if "retry_mode" not in st.session_state:
    st.session_state.retry_mode = False

def extract_weak_points(feedback_text):
    # Naive extraction: extract all incorrect explanations
    lines = feedback_text.split("\n")
    weak_points = [line for line in lines if "incorrect" in line.lower()]
    return "\n".join(weak_points)

# First input screen
if not st.session_state.show_quiz and not st.session_state.retry_mode:
    topic = st.text_input("Enter a topic to learn:", value="", key="topic_input")
    if st.button("Start Learning"):
        st.session_state.topic = topic.strip()
        st.session_state.show_quiz = True
        st.rerun()

# Learning phase (with or without retry)
if st.session_state.show_quiz or st.session_state.retry_mode:
    topic = st.session_state.topic

    past_feedbacks = retrieve_related_memory(topic)
    past_weaknesses = ""
    if past_feedbacks and past_feedbacks[0]:
        past_weaknesses = extract_weak_points(" ".join(past_feedbacks[0]))

    with st.spinner("Generating lesson and quiz..."):
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
        st.session_state.quiz_content = quiz

    st.subheader("📘 Lesson")
    st.write(lesson)

    st.subheader("❓ Quiz (MCQs Only)")
    st.markdown(quiz)
    st.markdown("💡 *Write your answers like:*\n- `1. C`\n- `2. A`")

    answers = st.text_area("✍️ Your Answers", height=150, key="answers_input")

    if st.button("Submit Answers"):
        if answers.strip():
            with st.spinner("Evaluating your answers..."):
                evaluator = FeedbackAgent(
                    name="Evaluator",
                    role="Gives feedback",
                    goal="Identify mistakes and improve learning.",
                    backstory="A guide who helps clarify confusing answers."
                )
                feedback = evaluator.run(topic, answers, st.session_state.quiz_content)

            st.subheader("✅ Feedback")
            st.write(feedback)

            st.session_state.last_feedback = feedback
            store_learning_memory(topic, feedback, answers)

            # Show prior memory
            memory = retrieve_related_memory(topic)
            if memory and memory[0]:
                st.subheader("🧠 Related Past Feedback")
                for i, mem in enumerate(memory[0]):
                    st.markdown(f"**{i+1}.** {mem}")

            # Toggle retry mode
            st.session_state.show_quiz = False
            st.session_state.retry_mode = True
        else:
            st.warning("Please write your answers before submitting.")

# Offer retry after feedback
if st.session_state.retry_mode and not st.session_state.show_quiz:
    if st.button("📚 Learn Again with Emphasis on Weak Areas"):
        st.session_state.show_quiz = True
        st.session_state.retry_mode = False
        st.rerun()
