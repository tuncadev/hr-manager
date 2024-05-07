import os
import time
import streamlit as fw
from datetime import datetime





start = datetime.now().replace(microsecond=0)

# Assuming temp_dir is the directory where the file is located



count = 0

app_base_path = os.getcwd()
temp_dir = os.path.join(app_base_path, "temp")
with open(os.path.join(temp_dir, "first_analysis.txt"), "r") as fa, \
     open(os.path.join(temp_dir, "questions_answers.txt"), "r") as qa, \
     open(os.path.join(temp_dir, "final_report.txt"), "r") as fr, \
     open(os.path.join(temp_dir, "chief_report.txt"), "r") as cr:
    first_analysis_contents = fa.read()
    questions_answers_contents = qa.read()
    final_report_contents = fr.read()
    chief_report_contents = cr.read()

fw.download_button(label="Download: First Analysis", data=first_analysis_contents, file_name="first_analysis.txt", mime="text/plain")
fw.download_button(label="Download: Questions & Answers", data=questions_answers_contents, file_name="questions_answers.txt", mime="text/plain")
fw.download_button(label="Download: Final Report", data=final_report_contents, file_name="final_report.txt", mime="text/plain")
fw.download_button(label="Download: Chief Director Report", data=chief_report_contents, file_name="chief_report.txt", mime="text/plain")
    # Display a download link for the file


with fw.container(border=True):
    col_left, col_right = fw.columns([4, 1])  # Use columns(2) to create two columns
    start_time = start.strftime('%d-%m-%Y')
    with col_left:
        fw.write(f"Your interview started at:")
        fw.write(start)  # Use start_time instead of start
    with col_right:
        fw.write(f"Time elapsed:")
        placeholder = fw.empty()
        while True:
            minutes = count // 60
            seconds = count % 60
            placeholder.text(f" {minutes:02d}:{seconds:02d}")
            time.sleep(1)
            count += 1

