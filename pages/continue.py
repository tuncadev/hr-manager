import streamlit as fw
from utils.globals import check_and_delete_temp_files
from tools.db_connect import DBConnect
from datetime import datetime

app_start = datetime.now()
with fw.form("continue"):
    back_btn = fw.page_link("app.py", label=":blue-background[Back to home]", icon="🏠")
    applicant_key = fw.text_input(label="Please enter your secret key:", type="password")
    next_btn = fw.form_submit_button("Continue")
    if next_btn:
        if applicant_key:
            responses = {}
            with DBConnect() as db:
                applicant_details = db.get_applicant_continue_details(applicant_key=applicant_key)
                if applicant_details:
                    responses["applicant_key"] = applicant_key
                    fw.session_state['app_start'] = app_start
                    last_page = db.get_lastpage(applicant_key=applicant_key)
                    success = applicant_details["success"]
                    applicant_id = applicant_details["id"]
                    responses["applicant_id"] = applicant_id
                    if success == 1:
                        error = "You have already completed your application."
                    elif not last_page:
                        error = "Your secret key seems to be wrong. Please check and try again"
                    else:
                        responses["continue"] = True
                        responses["name"] = applicant_details["name"]
                        responses["applicant_id"] = applicant_id
                        fw.switch_page(f"pages/{last_page[0]}.py")
                else:
                    error = "Your secret key seems to be wrong. Please check and try again"
                fw.error(error)
        else:
            fw.error("Please enter your applicant key")