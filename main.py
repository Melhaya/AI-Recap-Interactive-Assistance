from openai_client import *
from config import *
from services import *

def main():
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    # Initialize session variables if they don't exist
    if 'questions_answered' not in st.session_state:
        st.session_state.questions_answered = 0
    if 'content' not in st.session_state:
        st.session_state.content = None
    if 'question' not in st.session_state:
        st.session_state.question = None
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = []
    if 'received_feedback' not in st.session_state:
        st.session_state.received_feedback = []

    # Choice of Model
    model_choice = st.selectbox("Choose an AI model for generating questions and feedback", options=list(AI_MODELS.keys()))

    # AI Client Initialization
    ai_client = OpenAIClient(AI_MODELS[model_choice]['model'], SETUP_INSTRUCTIONS)

    # Number of Questions to be asked
    number_of_questions = st.number_input("How many questions would you like to answer?", min_value=1, max_value=10, value=2)

    # Type of Question
    question_type = st.selectbox("Choose the type of questions you prefer", options=["Multiple-Choice Questions", "Code Tracing and Correction", "Code Completion"])

    # Difficulty Level Selection
    difficulty_level = st.selectbox("Choose the difficulty level of the questions", options=["Easy", "Medium", "Hard"])

    # File upload
    uploaded_file = st.file_uploader("Upload your learning materials here", type=['txt'])

    # File upload and content loading
    if uploaded_file is not None and st.session_state.content is None:
        st.session_state.content = load_content(uploaded_file)

    # Generate new question based on reset state or if no question is present
    if st.session_state.content is not None and st.session_state.question is None:
        st.session_state.question = ai_client.question_generator(st.session_state.content, question_type, difficulty_level)

    # Display the progress and current question
    if st.session_state.question is not None:
        progress_value = (st.session_state.questions_answered+1) / number_of_questions
        st.progress(progress_value)
        st.write(st.session_state.question)

        # Handle answer submission
        char_limit = 500
        user_answer = st.text_area("Provide your Answer here", key=f"answer_{st.session_state.questions_answered}", height=200, placeholder="Write your answer here...")

        if len(user_answer) > char_limit:
            st.warning(f"Your answer exceeds the character limit of {char_limit} characters. Please shorten your response.")


        submit_btn = st.button('Submit Answer', on_click=disable, args=('submit', True), disabled=st.session_state.get("submit_disabled", False))
        if submit_btn:
            st.session_state.user_answer = user_answer
            st.session_state.feedback = ai_client.get_model_feedback(st.session_state.question, user_answer)
            st.session_state.questions_answered += 1
            st.write("AI Feedback:", st.session_state.feedback)
            st.session_state.questions_asked.append(st.session_state.question)
            st.session_state.received_feedback.append(st.session_state.feedback)
        # Handle skip question logic
        #else:
        #    skip_btn = st.button('Skip Question')
        #    if skip_btn:
        #        st.session_state.pop('question', None)
        #        st.rerun()

        # Handle next question logic
        if st.session_state.questions_answered < number_of_questions:
            next_btn = st.button('Next Question',on_click=enable, args=('submit',))
            if next_btn:
                st.session_state.pop('question', None)
                st.session_state.pop('feedback', None)
                st.rerun()

        # Check completion
        if st.session_state.questions_answered >= number_of_questions:
            #st.success(COMPLETION_MESSAGE)
            st.success(ai_client.completion_message(st.session_state.content, st.session_state.questions_asked, st.session_state.feedback))
            if COMPLETION_CELEBRATION:
                celebration()
            st.session_state.clear()

        if st.button('End Recap'):
            st.session_state.clear()
            st.success(COMPLETION_MESSAGE)
            if COMPLETION_CELEBRATION:
                celebration()

        # Handle restart button
        if st.button('Restart Recap'):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()