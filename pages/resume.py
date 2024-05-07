import json
import streamlit as fw

# Tools
from tools.db_connect import DBConnect
from tools.encryption_manager import EncryptionManager
from tools.read_file import ReadFileContents
from tools.get_tasks import GetTaskData
from tools.get_agents import GetAgentData
# Utils
from utils.globals import get_assistant_avatar

def run():
    def check_uploaded_file(file):
        file_name = file.name
        file_content = file.getvalue()
        if file_name.endswith('.doc'):
            readfile = ReadFileContents(file_name, file_content)
            cv_content = readfile.read_doc_file()
        elif file_name.endswith('.docx'):
            readfile = ReadFileContents(file_name, file_content)
            cv_content = readfile.read_docx_file()
        elif file_name.endswith('.txt'):
            readfile = ReadFileContents(file_name, file_content)
            cv_content = readfile.read_txt_file()
        elif file_name.endswith('.pdf'):
            readfile = ReadFileContents(file_name, file_content)
            cv_content = readfile.read_pdf_file()
        else:
            cv_content = "Unsupported file type"
        return cv_content

    responses = fw.session_state['responses']
    uploaded_file = responses['uploaded_file']
    with fw.spinner("Your resume is being analyzed. Please wait..."):
        with DBConnect() as db:
            name = responses["name"]
            email = responses["email"]
            selected_vac_name = responses["selected_vacancy"]
            selected_vac_details = db.get_vac_details(selected_vac_name)
            selected_vac_details = json.dumps(selected_vac_details)
            applicant_key = db.create_temp(name=name,
                                           email=email,
                                           selected_vac_name=selected_vac_name,
                                           selected_vac_details=selected_vac_details)
            responses["applicant_key"] = applicant_key
            if uploaded_file is not None:
                agent_data = GetAgentData()
                task_data = GetTaskData()
                # Get cv contents
                cv_contents = check_uploaded_file(uploaded_file)
                # Reformat using agent
                formatter = agent_data.return_document_expert()
                formatter_task = task_data.return_task("Document Expert", agent_instance=formatter, res=cv_contents)
                new_resume = formatter_task.execute()
                db.insert_into_resumes(applicant_key, content=new_resume)
                fw.switch_page("pages/hr-manager.py")

if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
