import os
import time
import streamlit as fw
from datetime import datetime
# Tools
from tools.db_connect import DBConnect
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData
# UtilsNgoTbABRnD
from utils.globals import get_static_image
from utils.globals import get_sidebar


def run():
    fw.session_state["status"] = 100
    # Sidebar content
    get_sidebar(step=6)
    # Defaults
    responses = fw.session_state['responses']
    applicant_id = responses['applicant_id']
    with DBConnect() as db:
        db.update_table(table_name="applicants", applicant_id=applicant_id, columns={'last_page': 'success'})
        agent_data = GetAgentData()
        task_data = GetTaskData()
        start = fw.session_state['app_start']
        end = datetime.now()
        passed = end - start
        with fw.spinner("Finalizing the interview..."):
            # Defaults
            vacancy = db.select_from_analysis(applicant_id=applicant_id, table_name="questions_answers")
            resume = db.select_from_resumes(applicant_id=applicant_id)
            first_analysis = db.select_from_analysis(applicant_id=applicant_id, table_name="first_analysis")
            questions_answers = db.select_from_analysis(applicant_id=applicant_id, table_name="questions_answers")
            final_report = db.select_from_analysis(applicant_id=applicant_id, table_name="final_report")
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
            db.insert_into_reports(applicant_id=applicant_id, report_table="chief_report", content=chief_of_hr_report)
            # Create temp files
            app_base_path = os.getcwd()
            temp_dir = os.path.join(app_base_path, "static/temp")
            with open(os.path.join(temp_dir, "first_analysis.txt"), "w") as fa, \
                 open(os.path.join(temp_dir, "questions_answers.txt"), "w") as qa, \
                 open(os.path.join(temp_dir, "final_report.txt"), "w") as fr, \
                 open(os.path.join(temp_dir, "chief_report.txt"), "w") as cr:
                fa.write(first_analysis)
                qa.write(questions_answers)
                fr.write(final_report)
                cr.write(chief_of_hr_report)
            applicant_key = db.get_applicant_details(applicant_id=applicant_id)
            hashed_applicant_key = applicant_key['applicant_key']
            db.update_table(table_name='applicants', applicant_id=applicant_id, columns={'applicant_key': hashed_applicant_key, 'start': f'{start}', 'end': f'{end}', 'success': 1})

    # Time container
    with fw.container(border=True):
        col_left, col_right = fw.columns([4, 1])  # Use columns(2) to create two columns
        with col_left:
            fw.write(f"Your interview started at:")
            fw.write(start)  # Use start_time instead of start
        with col_right:
            fw.write(f"Total time spent in interview:")
            fw.write(passed)  # Use start_time instead of start
    assistant_msg = fw.chat_message("assistant")
    with assistant_msg:
        unique_key = fw.session_state["unique_key"]
        assistant_msg.write(f"The interview is over...")
        assistant_msg.write(f"Your unique secret key is: :orange[{unique_key}]. Please save this key for future use, and do not share it with anyone.")
        # Create a placeholder for the message
        message_placeholder = fw.empty()

        countdown_seconds = 10
        for i in range(countdown_seconds, 0, -1):
            # Update the message in the placeholder
            message_placeholder.write(f":white[**Admin,**] You are being redirected to results page in :orange[00:{i:02d}] seconds...")
            time.sleep(1)
            # Clear the previous message
            message_placeholder.empty()

        # Show the final message
        message_placeholder.write(":white[**Admin,**] You are being redirected to results page in :orange[00:00] seconds...")
        fw.session_state["success"] = True
        fw.switch_page("pages/results.py")

if __name__ == "__main__":
    if "responses" in fw.session_state and "success" not in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access or go back to this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")

