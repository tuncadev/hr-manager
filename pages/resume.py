import json
import os

import streamlit as fw
from dotenv import dotenv_values

# Tools
from tools.db_connect import DBConnect
from tools.encryption_manager import EncryptionManager
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData
# Utils
from utils.globals import get_static_image
from utils.globals import check_uploaded_file
from utils.globals import get_sidebar
from utils.globals import hide_key

def run():
    fw.session_state["status"] = 20
    # Sidebar content
    get_sidebar(step=2)
    start = fw.session_state['app_start']
    responses = fw.session_state['responses']
    continue_application = responses["continue"]
    applicant_key = responses["applicant_key"]
    if not continue_application:
        openaikey = openai_api = os.getenv("OPENAI_API_KEY")
        hiddenKey = hide_key(key=openaikey)
        fw.write(f"Type: {type(openaikey)} | | KEY: {hiddenKey}")
        with fw.spinner("Your resume is being analyzed. Please wait..."):
            with DBConnect() as db:
                name = responses["name"]
                email = responses["email"]
                uploaded_file = responses['uploaded_file']
                selected_vac_name = responses["selected_vacancy"]
                selected_vac_details = db.get_vac_details(selected_vac_name)
                selected_vac_details = json.dumps(selected_vac_details)
                applicant_id = db.create_applicant(applicant_key=applicant_key,
                                                   name=name,
                                                   email=email,
                                                   selected_vac_name=selected_vac_name,
                                                   selected_vac_details=selected_vac_details,
                                                   start=start,
                                                   last_page="resume")
                if applicant_id:
                    responses["applicant_id"] = applicant_id
                    if uploaded_file is not None:
                        agent_data = GetAgentData()
                        task_data = GetTaskData()
                        # Get cv contents
                        cv_contents = check_uploaded_file(uploaded_file)
                        # Reformat using agent
                        formatter = agent_data.return_document_expert()
                        if formatter:
                            formatter_task = task_data.return_task("Document Expert", agent_instance=formatter, res=cv_contents)
                            new_resume = formatter_task.execute()
                            # fw.write(new_resume)
                            # print(new_resume) - Debug new resume
                            db.insert_into_resumes(applicant_id=applicant_id, content=new_resume)
                            fw.switch_page("pages/hr-manager.py")
                        else:
                            fw.write("Oops, something went wrong")
    else:
        with DBConnect() as db:
            applicant_id = responses["applicant_id"]
            resume = db.select_from_resumes(applicant_id=applicant_id)
            if not resume:
                assistant = fw.chat_message("assistant")
                with assistant:
                    fw.write("Your resume details are missing, please re-upload your resume")
                with fw.form("user_information"):
                    uploaded_file = fw.file_uploader("Choose a file")
                    submit = fw.form_submit_button("Continue", use_container_width=True, type="secondary")
                if submit:
                    with fw.spinner("Your resume is being analyzed. Please wait..."):
                        if uploaded_file:
                            responses['uploaded_file'] = uploaded_file
                            agent_data = GetAgentData()
                            task_data = GetTaskData()
                            # Get cv contents
                            cv_contents = check_uploaded_file(uploaded_file)
                            # Reformat using agent
                            formatter = agent_data.return_document_expert()
                            formatter_task = task_data.return_task("Document Expert", agent_instance=formatter, res=cv_contents)
                            new_resume = formatter_task.execute()
                            env_vars = dotenv_values('env/.data')
                            key = env_vars.get(f'{applicant_id}')
                            encryption_manager = EncryptionManager(applicant_id=applicant_id, key=key)
                            encrypted_text = encryption_manager.encrypt_data(new_resume)
                            db.update_table(table_name="resumes", applicant_id=applicant_id, columns={'content': encrypted_text})
                            fw.session_state["resume"] = True
                            fw.switch_page("pages/hr-manager.py")




if __name__ == "__main__":
    if "responses" in fw.session_state and "resume" not in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access or go back to this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
