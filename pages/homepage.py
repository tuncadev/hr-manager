import streamlit as fw
from datetime import datetime
# Tools
from tools.getvacancies import GetVacData
from tools.db_connect import DBConnect

# Utils
from utils.globals import get_assistant_avatar
from utils.globals import are_all_fields_filled



def app():

    start = fw.session_state['app_start']
    count = 0
    with fw.container(border=True):
        col_left, col_right = fw.columns([4, 1])  # Use columns(2) to create two columns
        start_time = start.strftime('%d-%m-%Y')
        with col_left:
            fw.write(f"Your interview started at:")
            fw.write(start)  # Use start_time instead of start

    with fw.form("user_information"):
        responses = fw.session_state['responses']
        assistant_one = fw.chat_message("assistant")
        with assistant_one:
            assistant_one.html("<b>HYS-Assistant</b>: <i>Please fill in the form to  continue with your application.</i>")
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
            now = datetime.now()
            passed = now - start
            fw.session_state['passed'] = passed
            fw.switch_page("pages/resume.py")
        else:
            fw.warning("All fields are required. Please check the fields for errors.")

# Check if the script is being accessed directly
if __name__ == "__main__":
    if "responses" in fw.session_state:
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
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
