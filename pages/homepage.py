import streamlit as fw
from datetime import datetime
# Tools
from tools.getvacancies import GetVacData
from tools.db_connect import DBConnect

# Utils
from utils.globals import *


def app():
    start = fw.session_state['app_start']
    css_placeholder = fw.empty()
    css = """
    <style>
    body, p, ol, ul, dl {
        font-size: 14px;
    }
        [data-testid="stAppViewBlockContainer"] {
            padding: 3rem 1rem 10rem !important;
        }
        .applicant_inform {
            padding: 16px;
            border-radius: 8px;
            background-color: rgba(255, 108, 108, 0.2);
            margin-bottom: 16px;
        }
    </style>
    """

    with css_placeholder:
        fw.markdown(css, unsafe_allow_html=True)
    # Sidebar content
    with fw.form("user_information"):
        responses = fw.session_state['responses']
        assistant_one = fw.chat_message("assistant")
        with assistant_one:
            assistant_one.html("<b>HR-Assistant</b>: <i>Please fill in the form to  continue with your application.</i>")
            assistant_one.html("<span style='color:#DB005F; font-weight:600;'><i>* All fields are required</i></span>")

        # Welcome
        responses['name'] = fw.text_input("Name")
        responses['email'] = fw.text_input("E-mail")
        responses["selected_vacancy"] = fw.selectbox('Select a vacancy', vacancy_names, index=index, key="selected_vacancy")
        uploaded_file = fw.file_uploader("Choose a file")
        responses['uploaded_file'] = uploaded_file
        submit = fw.form_submit_button("Continue", use_container_width=True, type="secondary")
    if submit:
        if are_all_fields_filled(responses) and uploaded_file:
            responses["applicant_key"] = hash_value(applicant_key)
            fw.session_state["unique_key"] = applicant_key
            responses["continue"] = False
            fw.session_state["responses"] = responses
            now = datetime.now()
            passed = now - start
            fw.session_state['passed'] = passed
            fw.session_state["homepage"] = True
            fw.switch_page("pages/resume.py")
        else:
            fw.warning("All fields are required. Please check the fields for errors.")

# Check if the script is being accessed directly
if __name__ == "__main__":
    if "responses" in fw.session_state and "homepage" not in fw.session_state:
        set_page_config(page_title="HYS Entnerprise | Human Resources Job Application")
        if "applicant_key" not in fw.session_state:
            applicant_key = get_random_string(10)  # Generate a 10-character random string
            fw.session_state["applicant_key"] = applicant_key
        else:
            applicant_key = fw.session_state["applicant_key"]
        get_sidebar(step=1)
        # Defaults
        vacancy_data = GetVacData()
        selected_vacancy_value = ""
        with DBConnect() as db:
            if 'init_vacancies' in locals() or (init_vacancies := vacancy_data.init_vacancies()):
                vacancy_names = db.get_vacancy_names()
        index = None if not selected_vacancy_value or selected_vacancy_value not in vacancy_names else vacancy_names.index(
            selected_vacancy_value)
        app()
    else:
        msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            fw.write("You cannot access or go back to this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")


