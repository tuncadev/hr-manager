import streamlit as st
from tools.db_connect import DBConnect
from utils.globals import get_static_image

def run():

    read_env = 'env/.data'

    def read_db(table_name=None):
        with DBConnect() as db:
            return db.select_from(table_name)

    def clear_data_file(file_path):
        try:
            with open(file_path, 'w') as file:
                pass
            st.success(f"Cleared all data in {file_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    def read_and_format_data_file(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                data_dict = {}
                for line in lines:
                    key, value = line.split('=', 1)
                    data_dict[key.strip()] = value.strip()

                formatted_output = "\n".join(f"{key} = {value}" for key, value in data_dict.items())
                return formatted_output
        except Exception as e:
            return f"An error occurred: {e}"

    def display_session_state():
        st.write("Current st.session_state values:")
        for key, value in st.session_state.items():
            st.write(f"{key}: {value}")

    # Initialize session state if not already set
    if 'selected_table' not in st.session_state:
        st.session_state.selected_table = None

    with st.sidebar:
        st.button("Go Home Yankee", key="home")
        clear_data = st.button("Clear .DATA")
        read_data = st.button("Read .DATA")
        view_db = st.button("View Database")

    if clear_data:
        clear_data_file(read_env)

    if read_data:
        st.session_state.selected_table = None
        st.session_state.show_tables = False
        formatted_data = read_and_format_data_file(read_env)
        st.title("Data Output")
        st.text(formatted_data)

    if view_db:
        st.session_state.selected_table = None
        st.session_state.show_tables = True
        st.rerun()

    if 'show_tables' in st.session_state and st.session_state.show_tables:
        st.subheader("What to view huh?")
        with DBConnect() as db:
            formatted_table_names = db.get_formatted_table_names()
            if formatted_table_names:
                table_names = [formatted_name for formatted_name, original_name in formatted_table_names]
                original_names_dict = {formatted_name: original_name for formatted_name, original_name in formatted_table_names}

        with st.form("Choose Table to View"):
            table_name = st.selectbox(label="Select Table", options=table_names)
            submit = st.form_submit_button("View")

            if submit:
                st.session_state.selected_table = original_names_dict[table_name]
                st.session_state.show_tables = False
                st.experimental_rerun()

    if st.session_state.selected_table:
        st.subheader(f"Contents of {st.session_state.selected_table.replace('_', ' ').title()}")
        df = read_db(st.session_state.selected_table)
        if df is not None:
            st.dataframe(df)


if __name__ == "__main__":
    if "responses" in st.session_state and "hr-manager" not in st.session_state:
        run()
    else:
        msg = st.chat_message("assistant", avatar=get_static_image(folder="avatar", filename="error.png"))
        with msg:
            st.write("You cannot access or go back to this page directly....")
        st.page_link("app.py", label="Home", icon="🏠")
