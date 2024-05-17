import streamlit as fw
from tools.db_connect import DBConnect

with DBConnect() as db:
    resume = db.select_from_resumes(applicant_id=32)
    print(resume)
    fw.markdown(resume)