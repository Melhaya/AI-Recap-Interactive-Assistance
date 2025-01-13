import os
import streamlit as st
from openai_client import OpenAIClient
from services import (
    enable,
    disable,
    check_answer,
    celebration
)
from config import *

from pdf_rag import (
    process_pdf_for_rag,
    save_chunks_to_json,
    load_chunks_from_json,
    embed_chunks_openai,
    create_faiss_index,
    save_faiss_index,
    load_faiss_index,
    save_embeddings_to_npy,
    load_embeddings_from_npy
)

def main():
    # Page title and intro
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    # ---------------- Session State Initialization ----------------
    if 'recap_in_progress' not in st.session_state:
        st.session_state.recap_in_progress = False
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
    if 'chunks' not in st.session_state:
        st.session_state.chunks = None
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = None
    if 'faiss_index' not in st.session_state:
        st.session_state.faiss_index = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = ""

    # ---------------- Course & Model Selection ----------------
    # 1) Select Course
    course_name = st.selectbox(
        "Choose a course:",
        options=list(COURSES.keys())
    )
    # 2) Retrieve course data from config
    course_info = COURSES[course_name]

    # Display learning objectives if available
    course_objectives = course_info.get("OBJECTIVES", [])
    if course_objectives:
        selected_objectives = st.multiselect("Pick one or more learning objectives to focus on:", course_objectives)
    else:
        selected_objectives = None  # No objectives for this course

    # 3) Choose AI model
    if DEBUG:
        model_choice = st.selectbox(
            "Choose an AI model for generating questions and feedback",
            options=list(AI_MODELS.keys())
        )
    chosen_model_dict = AI_MODELS["gpt-4o mini"]
    chosen_model = chosen_model_dict.get("model", "gpt-3.5-turbo")
    temperature = chosen_model_dict.get("temperature", 0.7)
    max_tokens = chosen_model_dict.get("max_tokens", 150)
    frequency_penalty = chosen_model_dict.get("frequency_penalty", 0.0)

    number_of_questions = st.number_input(
        "How many questions would you like to answer?",
        min_value=5,
        max_value=10,
        value=5
    )

    question_type = st.selectbox(
        "Choose the type of questions you prefer",
        ["Multiple-Choice Questions", "Code Tracing and Correction", "Code Completion"]
    )

    difficulty_level = st.selectbox(
        "Choose the difficulty level of the questions",
        ["Easy", "Medium", "Hard"]
    )

    # ---------------- AI Client ----------------
    ai_client = OpenAIClient(
        model=chosen_model,
        setup_instructions=SETUP_INSTRUCTIONS
    )

    # ---------------- Start Recap ----------------
    if not st.session_state.recap_in_progress:
        if st.button("Start Recap"):
            # Mark recap as started
            st.session_state.recap_in_progress = True

            # 1. Load or process PDF -> chunks
            if os.path.isfile(course_info.get("CHUNKS_JSON_PATH")):
                chunks = load_chunks_from_json(course_info.get("CHUNKS_JSON_PATH"))
            else:
                chunks = process_pdf_for_rag(pdf_path=course_info.get("PDF_FILE_PATH"), chunk_size=1000)
                save_chunks_to_json(chunks, course_info.get("CHUNKS_JSON_PATH"))

            st.session_state.chunks = chunks
            st.session_state.content = "\n".join(chunks)  # Combined text

            # 2. Load or create embeddings + FAISS index
            if os.path.isfile(course_info.get("EMBEDDINGS_NPY_PATH")) and os.path.isfile(course_info.get("FAISS_INDEX_PATH")):
                embeddings = load_embeddings_from_npy(course_info.get("EMBEDDINGS_NPY_PATH"))
                faiss_index = load_faiss_index(course_info.get("FAISS_INDEX_PATH"))
            else:
                embeddings = embed_chunks_openai(chunks, model="text-embedding-ada-002")
                save_embeddings_to_npy(embeddings, course_info.get("EMBEDDINGS_NPY_PATH"))
                faiss_index = create_faiss_index(embeddings)
                save_faiss_index(faiss_index, course_info.get("FAISS_INDEX_PATH"))

            st.session_state.embeddings = embeddings
            st.session_state.faiss_index = faiss_index

            # 3. Generate first question
            st.session_state.question = ai_client.question_generator(
                st.session_state.content,
                question_type,
                difficulty_level,
                st.session_state.questions_asked,
                course_objectives,
                selected_objectives,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            st.rerun()  # Refresh the UI to show the question

    # ---------------- Q&A Section (Recap In Progress) ----------------
    if st.session_state.recap_in_progress and st.session_state.question:
        # Display progress
        progress_value = (st.session_state.questions_answered + 1) / number_of_questions
        st.progress(progress_value)

        # Show the question
        st.write(st.session_state.question)

        # Answer input
        user_answer = st.text_area(
            "Provide your Answer here",
            key=f"answer_{st.session_state.questions_answered}",
            height=200,
            placeholder="Write your answer here..."
        )

        # Submit button
        submit_btn = st.button(
            "Submit Answer",
            on_click=disable,
            args=('submit', True),
            disabled=st.session_state.get("submit_disabled", False)
        )
        if submit_btn:
            st.session_state.user_answer = user_answer
            feedback = ai_client.get_model_feedback(
                st.session_state.question,
                user_answer,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            st.session_state.feedback = feedback
            st.session_state.questions_answered += 1

            # Display feedback

            st.write("AI Feedback:", feedback)

            # Record question & correctness
            st.session_state.questions_asked.append(st.session_state.question)
            correctness = check_answer(feedback)
            st.session_state.received_feedback.append(correctness or "No definite correctness found")
            if DEBUG:
                st.write("DEBUG:", dict(zip(st.session_state.questions_asked, st.session_state.received_feedback)))


        # ---------------- Next Question Logic ----------------
        if st.session_state.questions_answered < number_of_questions:
            # If we haven't reached the total number, allow Next
            next_btn = st.button("Next Question", on_click=enable, args=('submit',))
            if next_btn:
                # Clear old question, but keep recap state
                st.session_state.question = None
                st.session_state.feedback = None
                st.session_state.user_answer = ""

                # Generate the NEXT question
                new_question = ai_client.question_generator(
                    st.session_state.content,
                    question_type,
                    difficulty_level,
                    st.session_state.questions_asked,
                    course_objectives,
                    selected_objectives,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    frequency_penalty=frequency_penalty
                )
                st.session_state.question = new_question

                st.rerun()  #needed; the UI will refresh automatically
        else:
            # ---------------- Completion ----------------
            if 'feedback' in st.session_state:
                completion_text = ai_client.completion_message(
                    st.session_state.content,
                    st.session_state.questions_asked,
                    st.session_state.received_feedback,
                    course_objectives,
                    selected_objectives,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    frequency_penalty=frequency_penalty
                )
                st.success(completion_text)
                if COMPLETION_CELEBRATION:
                    celebration()

            # Clear everything
            st.session_state.clear()
            st.session_state.recap_in_progress = False
            st.success(COMPLETION_MESSAGE)

        # ---------------- End Recap ----------------
        if st.button('End Recap'):
            completion_text = ai_client.completion_message(
                st.session_state.content,
                st.session_state.questions_asked,
                st.session_state.received_feedback,
                course_objectives,
                selected_objectives,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            st.success(completion_text)
            if COMPLETION_CELEBRATION:
                celebration()

            # Clear everything
            st.session_state.clear()
            st.session_state.recap_in_progress = False

        # ---------------- Restart ----------------
        #if st.button("Restart Recap"):
        #    st.session_state.clear()
        #    st.session_state.recap_in_progress = False
        #    st.experimental_rerun()


if __name__ == "__main__":
    main()