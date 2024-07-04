import json
import streamlit as fw

# Tools
from tools.db_connect import DBConnect
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData

# Utils
from utils.globals import get_static_image
from utils.globals import get_sidebar


def run():
    fw.session_state["status"] = 40
    # Sidebar content
    get_sidebar(step=3)
    # Defaults
    responses = fw.session_state["responses"]
    applicant_id = responses["applicant_id"]
    with DBConnect() as db:
        db.update_table(table_name="applicants", applicant_id=applicant_id, columns={'last_page': 'hr-manager'})
        name = responses["name"]
        agent_data = GetAgentData()
        task_data = GetTaskData()
        with fw.status(f"{name}, the Human Resources Department is analyzing your resume. Please stand by...", expanded=True) as status:
            vacancy = db.get_selected_vac_details(applicant_id=applicant_id)
            resume = db.select_from_resumes(applicant_id=applicant_id)
            fw.write(f"*Human Resources Manager* is working")
            # Human Resources Manager is working
            human_resources_manager = agent_data.return_human_resources_manager()
            # fw.write(resume) - Debug the resume output after re-write
            human_resources_manager_task = task_data.return_task('Human Resources Manager',
                                                                 agent_instance=human_resources_manager,
                                                                 vac=f"{vacancy}", res=f"{resume}")
            first_analysis = human_resources_manager_task.execute()
            db.insert_into_reports(applicant_id=applicant_id, report_table="first_analysis", content=first_analysis)
            fw.write(f"*Recruitment Manager* is working")
            # Recruitment Manager is working
            recruitment_manager = agent_data.return_recruitment_manager()
            recruitment_manager_task = task_data.return_task("Recruitment Manager", recruitment_manager, vac=vacancy, res=resume,
                                                             first_analysis=first_analysis)
            recruitment_manager_report = recruitment_manager_task.execute()
            db.insert_into_reports(applicant_id=applicant_id, report_table="questions", content=recruitment_manager_report)
            fw.session_state["hr-manager"] = True
            fw.switch_page("pages/questions.py")

if __name__ == "__main__":
    if "responses" in fw.session_state and "hr-manager" not in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access or go back to this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
