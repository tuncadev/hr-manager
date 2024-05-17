import os
import time
import streamlit as fw

# Tools

# Utils
from utils.globals import get_static_image
from utils.globals import check_and_delete_temp_files


def run():
    # Defaults
    with fw.spinner("Retrieving results..."):
        app_base_path = os.getcwd()
        temp_dir = os.path.join(app_base_path, "static/temp")
        with open(os.path.join(temp_dir, "first_analysis.txt"), "r") as fa, \
             open(os.path.join(temp_dir, "questions_answers.txt"), "r") as qa, \
             open(os.path.join(temp_dir, "final_report.txt"), "r") as fr, \
             open(os.path.join(temp_dir, "chief_report.txt"), "r") as cr:
            first_analysis_contents = fa.read()
            questions_answers_contents = qa.read()
            final_report_contents = fr.read()
            chief_report_contents = cr.read()

    fw.download_button(label="Download: First Analysis", data=first_analysis_contents, file_name="first_analysis.txt", mime="text/plain")
    fw.download_button(label="Download: Questions & Answers", data=questions_answers_contents, file_name="questions_answers.txt",
                       mime="text/plain")
    fw.download_button(label="Download: Final Report", data=final_report_contents, file_name="final_report.txt", mime="text/plain")
    fw.download_button(label="Download: Chief Director Report", data=chief_report_contents, file_name="chief_report.txt", mime="text/plain")
    # Create a temporary link

    # Display links
    countdown_running = True

    # Create a placeholder for the countdown timer
    timer_placeholder = fw.empty()
    # Countdown from 60 to 0
    while countdown_running:
        for i in range(60, -1, -1):
            timer_placeholder.write(f"The temp files will be deleted after: {i} seconds")
            time.sleep(1)
            countdown_running = False
    if not countdown_running:
        check_and_delete_temp_files()
        fw.write("The temp files deleted!")
        # Clear the links from the UI
        timer_placeholder.empty()
        fw.empty()
        fw.page_link("app.py", label="Home", icon="🏠")


if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
