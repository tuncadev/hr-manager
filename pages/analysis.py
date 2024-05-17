import streamlit as fw

# Tools
from tools.db_connect import DBConnect
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData
# Utils
from utils.globals import get_static_image
from utils.globals import get_sidebar


def run():
    fw.session_state["status"] = 80
    # Sidebar content
    get_sidebar(step=5)
    with DBConnect() as db:
        # Defaults
        responses = fw.session_state['responses']
        applicant_id = responses['applicant_id']
        db.update_table(table_name="applicants", applicant_id=applicant_id, columns={'last_page': 'analysis'})
        name = responses['name']
        agent_data = GetAgentData()
        task_data = GetTaskData()
        assistant_msg = fw.chat_message("assistant")
        with assistant_msg:
            assistant_msg.write(f"{name}, Human Resources Director is analyzing your answers.")
        with fw.spinner(f"Just a few things left..."):
            # Previous DB data
            vacancy = db.select_from_analysis(applicant_id=applicant_id, table_name="questions_answers")
            resume = db.select_from_resumes(applicant_id=applicant_id)
            first_analysis =  db.select_from_analysis(applicant_id=applicant_id, table_name="first_analysis")
            questions_answers = db.select_from_analysis(applicant_id=applicant_id, table_name="questions_answers")
            # Human Resources Director is working
            human_resources_director = agent_data.return_human_resources_director()
            human_resources_director_task = task_data.return_task("Human Resources Director",
                                                                  agent_instance=human_resources_director,
                                                                  vac=vacancy,
                                                                  res=resume,
                                                                  first_analysis=first_analysis,
                                                                  questions_answers=questions_answers)
            final_report = human_resources_director_task.execute()
            db.insert_into_reports(applicant_id=applicant_id, report_table="final_report", content=final_report)
            fw.session_state["analysis"] = True
            fw.switch_page("pages/success.py")


if __name__ == "__main__":
    if "responses" in fw.session_state and "analysis" not in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access or go back to this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
