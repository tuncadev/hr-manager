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
    questions = fw.session_state['questions']
    applicant_key = responses['applicant_key']
    name = responses['name']
    agent_data = GetAgentData()
    task_data = GetTaskData()
    assistant_msg = fw.chat_message("assistant")
    with assistant_msg:
        assistant_msg.write(f"{name}, Human Resources Director is analyzing your answers.")
    with fw.spinner(f"Just a few things left..."):
        with DBConnect() as db:
            # Previous DB data
            vacancy = db.select_from_analysis(applicant_key=applicant_key, table_name="questions_answers")
            resume = db.select_from_resumes(applicant_key=applicant_key)
            first_analysis =  db.select_from_analysis(applicant_key=applicant_key, table_name="first_analysis")
            questions_answers = db.select_from_analysis(applicant_key=applicant_key, table_name="questions_answers")
            # Human Resources Director is working
            human_resources_director = agent_data.return_human_resources_director()
            human_resources_director_task = task_data.return_task("Human Resources Director",
                                                                  agent_instance=human_resources_director,
                                                                  vac=vacancy,
                                                                  res=resume,
                                                                  first_analysis=first_analysis,
                                                                  questions_answers=questions_answers)
            final_report = human_resources_director_task.execute()
            db.insert_into_reports(applicant_key=applicant_key, report_table="final_report", content=final_report)
            fw.switch_page("pages/success.py")


if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
