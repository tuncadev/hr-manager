import streamlit as fw

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
    with assistant_msg:
        assistant_msg.write(f"{name}, Wrapping things up...")
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
        with assistant_msg:
            fw.write("Your interview is over. You will be contacted shortly")


if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")