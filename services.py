import streamlit as st
from streamlit_extras.let_it_rain import rain

def load_content_txt(file):
    """
    Loads text from a TXT file as a string.
    """
    return file.getvalue().decode("utf-8")

def enable(btn):
    """
    Enable a Streamlit button by removing its disabled state.
    """
    st.session_state[f"{btn}_disabled"] = False

def disable(btn, b):
    """
    Set the disabled state of a Streamlit button to True/False.
    """
    st.session_state[f"{btn}_disabled"] = b

def check_answer(input_string):
    """
    Checks if the first line of AI feedback is 'correct' or 'incorrect'.
    """
    lines = input_string.split('\n')
    first_line = lines[0].lower() if lines else ""

    if 'incorrect' in first_line or 'inkorrekt' in first_line :
        return "student answered incorrectly"
    elif 'correct' in first_line or 'korrekt' in first_line:
        return "student answered correctly"
    else:
        return None

def celebration():
    """
    Displays a celebratory effect in Streamlit.
    """
    rain(
        emoji="🥳",
        font_size=54,
        falling_speed=5,
        animation_length=1,
    )