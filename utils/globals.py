import os
import string
import random
import bcrypt
import streamlit as fw
from tools.read_file import ReadFileContents

def get_static_image(folder, filename):
    avatar_path = f"static/media/{folder}/{filename}"
    return avatar_path

def are_all_fields_filled(responses):
    for key, value in responses.items():
        if not value:
            return False
    return True


def check_and_delete_temp_files():
    temp_dir = "static/temp"
    for file_name in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file_name)
        os.remove(file_path)


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


# Generate a random key for each applicant
def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def hash_value(applicant_key):
    hashed_value = bcrypt.hashpw(applicant_key.encode(), bcrypt.gensalt())
    return hashed_value

def get_sidebar(step):
    applicant_key = fw.session_state["applicant_key"]
    with fw.sidebar:
        fw.markdown(
            f'<div style="display: flex; align-items: center; justify-content: space-between; flex-direction: '
            f'column; padding: 0px 10px 10px 10px; row-gap: 10px;">'
            f'<div>'
            f'<img src="app/static/hys-logo-mono-colored.webp" style="width: 200px;">'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        fw.divider()
        fw.markdown(f'Your appointment number is:')
        fw.error(f':orange[{applicant_key}]')
        fw.markdown(
            f'<span style="font-size:13px;">:red[Please write it down and do not share it!]</span>',
            unsafe_allow_html=True)
        fw.divider()
        if "status" in fw.session_state:
            percent_complete = fw.session_state["status"]
            progress_text = f"Appointment progress ({percent_complete}%)"
        else:
            percent_complete = 0
            progress_text = f"Appointment progress ({percent_complete}%)"
        my_bar = fw.progress(0, text=progress_text)
        my_bar.progress(percent_complete, text=progress_text)
        if step == 1:
            fw.page_link("pages/homepage.py", label="Step 1) Application Form")
        else:
            fw.page_link("pages/homepage.py", label="Step 1) Application Form", disabled=True)
        if step == 2:
            fw.page_link("pages/resume.py", label="Step 2) Resume Analysis")
        else:
            fw.page_link("pages/resume.py", label="Step 2) Resume Analysis", disabled=True)
        if step == 3:
            fw.page_link("pages/hr-manager.py", label="Step 3) HR Department Analysis")
        else:
            fw.page_link("pages/hr-manager.py", label="Step 3) HR Department Analysis", disabled=True)
        if step == 4:
            fw.page_link("pages/questions.py", label="Step 4) Interview (questions-answers)")
        else:
            fw.page_link("pages/questions.py", label="Step 4) Interview (questions-answers)", disabled=True)
        if step == 5:
            fw.page_link("pages/analysis.py", label="Step 5) Final Analysis")
        else:
            fw.page_link("pages/analysis.py", label="Step 5) Final Analysis", disabled=True)
        if step == 6:
            fw.page_link("pages/success.py", label="Step 6) Results")
        else:
            fw.page_link("pages/success.py", label="Step 6) Results", disabled=True)
        fw.divider()
        fw.page_link("pages/privacy_policy.py", label="Privacy Policy", disabled=False)
        fw.page_link("pages/terms.py", label="Terms and Conditions", disabled=False)


def set_page_config(page_title, page_icon=None, layout=None, initial_sidebar_state=None, menu_items=None):
    if not layout:
        layout = "centered"
    if not initial_sidebar_state:
        initial_sidebar_state = "auto"
    if not menu_items:
        menu_items = {}
    fw.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
        menu_items=menu_items
    )