import os
import time
import streamlit as fw
from datetime import datetime
# Tools
from tools.db_connect import DBConnect
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData
# Utils
from utils.globals import get_assistant_avatar


def run():
    # Defaults
    responses = fw.session_state['responses']
    name = responses['name']
    applicant_key = responses['applicant_key']
    agent_data = GetAgentData()
    task_data = GetTaskData()
    assistant_msg = fw.chat_message("assistant")
    with fw.spinner("Finalizing the interview..."):
        with DBConnect() as db:
            # Defaults
            vacancy = db.select_from_analysis(applicant_key=applicant_key, table_name="questions_answers")
            resume = db.select_from_resumes(applicant_key=applicant_key)
            first_analysis = db.select_from_analysis(applicant_key=applicant_key, table_name="first_analysis")
            questions_answers = db.select_from_analysis(applicant_key=applicant_key, table_name="questions_answers")
            final_report = db.select_from_analysis(applicant_key=applicant_key, table_name="final_report")
            chief_of_hr = agent_data.return_chief_of_hr()
            chief_of_hr_task = task_data.return_task(
                'Chief of Human Resources Officer',
                agent_instance=chief_of_hr,
                vac=vacancy,
                res=resume,
                first_analysis=first_analysis,
                questions_answers=questions_answers,
                final_report=final_report
            )
            chief_of_hr_report = chief_of_hr_task.execute()
            db.insert_into_reports(applicant_key=applicant_key, report_table="chief_report", content=chief_of_hr_report)
            # Create temp files
            app_base_path = os.getcwd()
            temp_dir = os.path.join(app_base_path, "temp")
            with open(os.path.join(temp_dir, "first_analysis.txt"), "w") as fa, \
                 open(os.path.join(temp_dir, "questions_answers.txt"), "w") as qa, \
                 open(os.path.join(temp_dir, "final_report.txt"), "w") as fr, \
                 open(os.path.join(temp_dir, "chief_report.txt"), "w") as cr:
                fa.write(first_analysis)
                qa.write(questions_answers)
                fr.write(final_report)
                cr.write(chief_of_hr_report)
    # Time container
    start = fw.session_state['app_start']
    passed = datetime.now() - start
    with fw.container(border=True):
        col_left, col_right = fw.columns([4, 1])  # Use columns(2) to create two columns
        with col_left:
            fw.write(f"Your interview started at:")
            fw.write(start)  # Use start_time instead of start
        with col_right:
            fw.write(f"Total time spent in interview:")
            fw.write(passed)  # Use start_time instead of start
    with assistant_msg:
        assistant_msg.write(f"The interview is over...")
        assistant_msg.write(f"You are being redirected to results page...")
        time.sleep(5)
        fw.switch_page("pages/results.py")


if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")

