import streamlit as st
from tools.db_connect import DBConnect

with DBConnect() as db:
    all_applicants = db.get_all_applicants()
    resumes_df = db.get_resumes_with_names()

    if resumes_df is not None:
        st.dataframe(resumes_df.style.set_table_styles([{
            'selector': 'tr:hover',
            'props': [('background-color', '#f2f2f2')]
        }]).set_properties(**{
            'text-align': 'left',
            'font-size': '12pt'
        }))

with open('env/.data', 'r') as file:
    data = file.read()
    st.write(data)

