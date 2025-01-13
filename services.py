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

# Function to add a rotating spinner in the center
def show_spinner():
    spinner_css = """
    <style>
    /* Spinner Container */
    .center-spinner {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
    }

    /* Spinner Animation */
    .spinner {
        border: 16px solid #f3f3f3;  /* Light gray */
        border-top: 16px solid #F7A800;  /* Orange */
        border-right: 16px solid #E03C31;  /* Red/Maroon */
        border-bottom: 16px solid #8A1538;  /* Darker Maroon */
        border-left: 16px solid #FFCC00;  /* Gold */
        border-radius: 50%;
        width: 140px;
        height: 140px;
        animation: spin 1.5s linear infinite;
    }

    /* Spin Keyframes */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>

    <div class="center-spinner">
        <div class="spinner"></div>
    </div>
    """
    st.markdown(spinner_css, unsafe_allow_html=True)

# Function to remove the spinner
def hide_spinner():
    remove_spinner = """
    <script>
        const spinner = window.parent.document.querySelector('.center-spinner');
        if (spinner) {
            spinner.remove();
        }
    </script>
    """
    st.markdown(remove_spinner, unsafe_allow_html=True)
