import json
import streamlit as fw

# Tools
from tools.db_connect import DBConnect
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData

# Utils
from utils.globals import get_assistant_avatar

def run():
    # Defaults
    responses = fw.session_state["responses"]
    name = responses["name"]
    applicant_key = responses["applicant_key"]
    agent_data = GetAgentData()
    task_data = GetTaskData()
    assistant = fw.chat_message("assistant")
    with fw.spinner(f"{name}, the Human Resources Department is analyzing your resume. Please stand by..."):
        with DBConnect() as db:
            vacancy = db.get_selected_vac_details(applicant_key=applicant_key)
            resume = db.select_from_resumes(applicant_key=applicant_key)
            with assistant:
                fw.write(f"*Human Resources Manager* is working")
            # Human Resources Manager is working
            human_resources_manager = agent_data.return_human_resources_manager()
            human_resources_manager_task = task_data.return_task('Human Resources Manager',
                                                                 agent_instance=human_resources_manager,
                                                                 vac=f"{vacancy}", res=f"{resume}")
            first_analysis = human_resources_manager_task.execute()
            db.insert_into_reports(applicant_key=applicant_key, report_table="first_analysis", content=first_analysis)
            assistant.empty()
            with assistant:
                fw.write(f"*Recruitment Manager* is working")
            # Recruitment Manager is working
            recruitment_manager = agent_data.return_recruitment_manager()
            recruitment_manager_task = task_data.return_task("Recruitment Manager", recruitment_manager, vac=vacancy, res=resume,
                                                             first_analysis=first_analysis)
            recruitment_manager_report = recruitment_manager_task.execute()
            db.insert_into_reports(applicant_key=applicant_key, report_table="questions", content=recruitment_manager_report)
            recruitment_manager_report_json = json.loads(recruitment_manager_report)
            questions = recruitment_manager_report_json.get('questions', [])
            fw.session_state['questions'] = questions
            fw.switch_page("pages/questions.py")

if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
