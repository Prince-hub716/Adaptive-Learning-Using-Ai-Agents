# 🎓 Adaptive Education Trainer  
**Agentic AI Meets Memory: Building Smarter Workflows That Learn Over Time**


This project showcases how to build an **adaptive AI learning assistant** using **CrewAI**, **Gemini (Google Generative AI)**, **ChromaDB**, and a custom **HTML/CSS/JS frontend** with a **Flask backend**. The trainer teaches a topic, quizzes the user, evaluates the responses, and adapts its future teaching strategy by storing contextual memory.

It’s designed for educational, productivity, or coaching workflows that require **agent-based reasoning and persistent memory**—now with a beautiful, animated web interface.

---


## 🚀 Features
- ✅ Multi-agent workflow using **CrewAI**
- ✅ Dynamic lesson and quiz generation using **Gemini (Google Generative AI)**
- ✅ Feedback evaluation with real-time personalization
- ✅ Long-term memory powered by **ChromaDB (Vector Store)**
- ✅ Modern HTML/CSS/JS web app with animated, study-themed UI
- ✅ Flask backend API for robust integration

---


## 🧰 Tech Stack

| Component     | Purpose                         |
|---------------|----------------------------------|
| `HTML/CSS/JS` | Frontend UI (webapp)            |
| `Flask`       | Backend API                     |
| `google-generativeai` | LLM for teaching, quizzes, feedback (Gemini) |
| `crewai`      | Agentic workflow management     |
| `chromadb`    | Persistent memory via vector DB |

---


## 📦 Requirements

- **Python**: >= 3.10 and < 3.13  
- **Node.js** (optional, for advanced frontend tooling)

### 🔧 Install Dependencies

```bash
pip install flask flask_cors
pip install google-generativeai
pip install chromadb
pip install crewai
```

---


## 🛠️ How to Run

1. **Set your Gemini API key**  
Edit `adaptive_trainer.py` and `memory_store.py` or set the environment variable:

```python
import os
os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
```

2. **Start the backend (Flask API)**

```bash
python webapp/backend.py
```

3. **Serve the frontend**

```bash
cd webapp
python -m http.server 8000
```

4. **Open your browser at** [http://localhost:8000/index.html](http://localhost:8000/index.html)

---

## 📁 Project Structure

```bash
.

├── adaptive_trainer.py    # Core agent logic (Gemini, CrewAI)
├── memory_store.py        # Handles ChromaDB integration
├── webapp/
│   ├── index.html         # Main web UI
│   ├── style.css          # UI styles (green, animated)
│   ├── app.js             # Frontend logic (AJAX, UI)
│   └── backend.py         # Flask backend API
├── chroma_storage/        # (auto-created) Persistent memory DB
└── README.md              # You're here
```

---

## 📚 Use Case

This project is ideal for:
- Personalized education apps
- Agentic AI research demos
- Adaptive productivity tools
- Use cases needing workflow + memory

---


## 🧠 Memory Flow

- Stores user responses, feedback, and weak areas
- Uses **Gemini embeddings** + **ChromaDB** to persist memory
- Recalls similar learning sessions to guide next steps

---

## 🧪 Example Topics to Try

- "Photosynthesis"
- "Basics of Python"
- "World War II history"
- "Introduction to Machine Learning"

---


## 📝 License

MIT License. Open for customization and integration into your own projects.
