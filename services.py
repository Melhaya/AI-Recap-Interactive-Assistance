import streamlit as st
from streamlit_extras.let_it_rain import rain

def load_content(file):
    return file.getvalue().decode("utf-8")

def enable(btn):
    st.session_state[f"{btn}_disabled"] = False

def disable(btn, b):
    st.session_state[f"{btn}_disabled"] = b

def celebration():
    rain(
        emoji="🥳",
        font_size=54,
        falling_speed=5,
        animation_length=1,
    )