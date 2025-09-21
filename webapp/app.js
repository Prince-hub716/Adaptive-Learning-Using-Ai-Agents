document.addEventListener('DOMContentLoaded', function() {
    const topicSection = document.getElementById('topic-section');
    const lessonSection = document.getElementById('lesson-section');
    const quizSection = document.getElementById('quiz-section');
    const feedbackSection = document.getElementById('feedback-section');
    const memorySection = document.getElementById('memory-section');

    const topicInput = document.getElementById('topic-input');
    const startBtn = document.getElementById('start-btn');
    const lessonContent = document.getElementById('lesson-content');
    const quizContent = document.getElementById('quiz-content');
    const answersInput = document.getElementById('answers-input');
    const submitAnswersBtn = document.getElementById('submit-answers-btn');
    const feedbackContent = document.getElementById('feedback-content');
    const retryBtn = document.getElementById('retry-btn');
    const memoryContent = document.getElementById('memory-content');

    // UI state
    let topic = '';
    let quiz = '';
    let lesson = '';
    let feedback = '';
    let memory = [];

    // Show/hide helpers
    function showSection(section) { section.classList.remove('hidden'); }
    function hideSection(section) { section.classList.add('hidden'); }

    // Start Learning
    startBtn.addEventListener('click', function() {
        topic = topicInput.value.trim();
        if (!topic) {
            alert('Please enter a topic.');
            return;
        }
        lessonContent.textContent = 'Loading lesson...';
        quizContent.textContent = 'Loading quiz...';
        showSection(lessonSection);
        showSection(quizSection);
        hideSection(feedbackSection);
        hideSection(memorySection);
        fetch('http://localhost:5000/api/lesson-quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic })
        })
        .then(res => res.json())
        .then(data => {
            lesson = data.lesson;
            quiz = data.quiz;
            lessonContent.innerHTML = marked.parse(lesson);
            quizContent.innerHTML = marked.parse(quiz);
        })
        .catch(err => {
            lessonContent.textContent = 'Error loading lesson.';
            quizContent.textContent = '';
        });
    });

    // Submit Answers
    submitAnswersBtn.addEventListener('click', function() {
        const answers = answersInput.value.trim();
        if (!answers) {
            alert('Please write your answers before submitting.');
            return;
        }
        feedbackContent.textContent = 'Evaluating your answers...';
        showSection(feedbackSection);
        fetch('http://localhost:5000/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, answers, quiz })
        })
        .then(res => res.json())
        .then(data => {
            feedback = data.feedback;
            memory = data.memory || [];
            feedbackContent.innerHTML = marked.parse(feedback);
            if (memory.length && memory[0].length) {
                showSection(memorySection);
                memoryContent.innerHTML = '';
                memory[0].forEach((mem, i) => {
                    memoryContent.innerHTML += `<div><b>${i+1}.</b> ${marked.parse(mem)}</div>`;
                });
            } else {
                hideSection(memorySection);
            }
        })
        .catch(err => {
            feedbackContent.textContent = 'Error evaluating answers.';
            hideSection(memorySection);
        });
    });

    // Retry
    retryBtn.addEventListener('click', function() {
        answersInput.value = '';
        hideSection(feedbackSection);
        hideSection(memorySection);
        showSection(lessonSection);
        showSection(quizSection);
    });
});
