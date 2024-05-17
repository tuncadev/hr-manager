import streamlit as fw
from utils.globals import check_and_delete_temp_files
from utils.globals import get_static_image
from utils.globals import hash_value
from datetime import datetime

if __name__ == "__main__":

    css_placeholder = fw.empty()
    css = """
<style>
    body, p, a, button {
        font-size: 12px;
    }
    [data-testid="stHorizontalBlock"] {
        align-items:center;
    }
    [data-testid="stImage"] {
        margin: auto;
    }
    #human-resources-assistant {
        text-align:center;
    }
    button[kind="primary"] {
        background-color: #0f9900;
        border-color: #fafafa33;
        min-height: auto;
    }
    button[kind="primary"]:hover {
        color: #ffffff;
        background-color: #01034c;
        border-color: #ffffff;
    }
    button[kind="secondary"] {
        background-color: #ffffff;
        border-color: #fafafa33;
        color:#01034c;
        min-height: auto;
    }
    button[kind="secondary"]:hover {
        background-color: #01034c;
        border-color: #ffffff;
        color: #ffffff;
    }      

</style>
"""
    app_start = datetime.now()
    # Display the CSS using st.markdown
    with css_placeholder:
        fw.markdown(css, unsafe_allow_html=True)
    with fw.spinner("Initializing..."):
        check_and_delete_temp_files()
        header = fw.container(border=True)
        with header:
            fw.image(image=get_static_image(folder="images/hys", filename="hys-logo-mono-colored.webp"), width=200)
            fw.header(divider="blue", anchor=False, body="Human Resources Assistant")
        container = fw.container(border=True)
        with container:

            col_left, col_center, col_right = fw.columns([1.5, 1.2, 2],  gap="small")
            with col_left:
                assistant = fw.chat_message("assistant")
                with assistant:
                    msg = fw.write("What would you like to do ?")
            with col_center:
                new_application = fw.button(key="start", type="primary", label="Start a new application")
            with col_right:
                continue_application = fw.button(key="continue", type="secondary", label="Continue my application", )
        if new_application:
            responses = {}
            fw.session_state['responses'] = responses
            fw.session_state['app_start'] = app_start
            css_placeholder.empty()
            fw.switch_page("pages/homepage.py")
        if continue_application:
            css_placeholder.empty()
            fw.switch_page("pages/continue.py")
