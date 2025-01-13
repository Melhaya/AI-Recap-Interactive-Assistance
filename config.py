######## GENERAL APP INFORMATION ##############

APP_TITLE = "AI-Powered Recap Interactive Assistant (ARIA)"
APP_INTRO = """This app assesses the user's understanding based on their responses to AI-generated questions from a course document. The AI models can provide detailed feedback and guide the user through learning concepts effectively."""

APP_HOW_IT_WORKS = """
This application uses AI to enhance learning through interactive Q&A sessions. 
It dynamically generates questions related to the course content and provides feedback based on the user's answers. 
The AI can simulate a tutoring environment, offering insights that help reinforce learning.
"""

SETUP_INSTRUCTIONS = """You are an AI Recap Interactive Assistant designed to help students review and understand educational content. 
Your tasks include generating questions (multiple-choice, code reviews, etc.), motivating students, reviewing their answers, 
and providing corrections and explanations when necessary. Always be positive and motivating.
"""

COMPLETION_MESSAGE = "You've reached the end! I hope you learned something!"
COMPLETION_CELEBRATION = True  # Optional, can be set to False if no celebration effect is desired.

DEBUG = False

####### AI CONFIGURATION #############

# Details for AI model usage
AI_MODELS = {
    "gpt-4o": {
        "model": "gpt-4o",
        "temperature": 0.2,
        "max_tokens": 150,
        "frequency_penalty": 0.4
    },
    "gpt-4o mini": {
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "max_tokens": 1000,
        "frequency_penalty": 0.4
    },
    "gpt-4-turbo": {
        "model": "gpt-4-turbo",
        "temperature": 0.5,
        "max_tokens": 150
    },
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 150
    }
}


####### COURSE CONFIGURATION #############
COURSES = {
    "Python – schnell und intensiv Programmieren lernen": {
        "PDF_FILE_PATH": "python_2024/PyMOOC.pdf",
        "CHUNKS_JSON_PATH": "python_2024/lecture_chunks.json",
        "EMBEDDINGS_NPY_PATH": "python_2024/lecture_embeddings.npy",
        "FAISS_INDEX_PATH": "python_2024/lecture.index",
        "OBJECTIVES": [
            "Variables and Data Types",
            "Control Flow",
            "Functions",
            "Object-Oriented Programming",
            "Error Handling"
        ]
    },
}