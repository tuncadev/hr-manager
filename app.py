import os
import time
import streamlit as fw
from utils.globals import check_and_delete_temp_files
from datetime import datetime

app_start = datetime.now()

if __name__ == "__main__":
    responses = {}
    with fw.spinner("Initializing..."):
        check_and_delete_temp_files()
        fw.session_state['responses'] = responses
        fw.session_state['app_start'] = app_start
        time.sleep(3)
        fw.switch_page("pages/homepage.py")
