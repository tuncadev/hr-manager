import time
import streamlit as fw

if __name__ == "__main__":
    responses = {}
    with fw.spinner("Initializing..."):
        fw.session_state['responses'] = responses
        time.sleep(3)
        fw.switch_page("pages/homepage.py")
