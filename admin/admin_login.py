import streamlit as fw
from utils.globals import get_static_image

def admin_login():
    css_placeholder = fw.empty()
    css = """
        <style>
            [data-testid="stImage"] {
                margin: auto;
            }
            h2#administration-dashboard {
                text-align:center;
            }

            button[kind="primary"] div p
            {
                font-size: 0.9rem;
            }
            button[kind="secondary"] div p {
                font-size: 0.9rem;
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
    # Login form
    main_container = fw.container(border=True)
    with css_placeholder:
        fw.markdown(css, unsafe_allow_html=True)
    with main_container:
        fw.image(image=get_static_image(folder="images/hys", filename="hys-logo-mono-colored.webp"), width=200)
        fw.header(divider="blue", anchor=False, body=":orange[Administration Dashboard] ")
        with fw.form("admin_login"):
            username = fw.text_input(label="Username", key="username")
            passwrd = fw.text_input(label="Password", type="password", key="passwrd")
            submit = fw.form_submit_button("GO!")
        if submit:
            fw.switch_page("pages/admin-dashboard.py")


if __name__ == "__main__":
    # """    if "admin" in fw.session_state:"""
    admin_login()
    #  """ else:
    #       msg = fw.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
    #       with msg:
    #           fw.write("You cannot access this page directly....")
    #       fw.page_link("app.py", label="Home", icon="🏠")"""
