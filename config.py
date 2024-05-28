######## GENERAL APP INFORMATION ##############

APP_TITLE = "AI Recap Interactive Assistant (ARIA)"
APP_INTRO = """This app assesses the user's understanding based on their responses to AI-generated questions from a case study document. The AI models can provide detailed feedback and guide the user through learning concepts effectively."""

APP_HOW_IT_WORKS = """
This application uses AI to enhance learning through interactive Q&A sessions. It dynamically generates questions related to the course content and provides feedback based on the user's answers. The AI can simulate a tutoring environment, offering insights that help reinforce learning.
"""

SETUP_INSTRUCTIONS = "You are an AI Recap Interactive Assistant designed to help students review and understand educational content. Your tasks include generating questions (multiple-choice, code reviews, etc.), motivating students, reviewing their answers, and providing corrections and explanations when necessary. Always be positive and motivating\n"



COMPLETION_MESSAGE = "You've reached the end! I hope you learned something!"
COMPLETION_CELEBRATION = True  # Optional, can be set to False if no celebration effect is desired.

####### AI CONFIGURATION #############

# Details for AI model usage
AI_MODELS = {
    "gpt-4-turbo": {
        "model": "gpt-4-turbo",
        "temperature": 0.5,
        "max_tokens": 150
    },
    "gpt-4o": {
        "model": "gpt-4o",
        "temperature": 0.5,
        "max_tokens": 150
    },
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 150
    }
}

# Cost calculation settings (Optional and can be adjusted based on your budget or pricing structure)
COST_SETTINGS = {
    "gpt-4-turbo": {"prompt_tokens": 0.01, "completion_tokens": 0.03},
    "gpt-4o": {"prompt_tokens": 0.005, "completion_tokens": 0.015},
    "gpt-3.5-turbo": {"prompt_tokens": 0.0005, "completion_tokens": 0.0015}
}
