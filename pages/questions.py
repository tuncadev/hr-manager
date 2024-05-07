import streamlit as fw
from datetime import datetime
# Tools
from tools.db_connect import DBConnect
# Utils
from utils.globals import get_assistant_avatar


def run():
    # Defaults
    responses = fw.session_state['responses']
    questions = fw.session_state['questions']
    applicant_key = responses['applicant_key']
    name = responses['name']
    # Time container
    start = fw.session_state['app_start']
    passed = datetime.now() - start
    with fw.container(border=True):
        col_left, col_right = fw.columns([4, 1])  # Use columns(2) to create two columns
        with col_left:
            fw.write(f"Your interview started at:")
            fw.write(start)  # Use start_time instead of start
        with col_right:
            fw.write(f"Time spent in interview so far:")
            fw.write(passed)  # Use start_time instead of start
    # The rest
    num_questions = len(questions)
    answers = fw.session_state.get('answers', [''] * num_questions)
    assistant_msg = fw.chat_message("assistant")
    with assistant_msg:
        assistant_msg.write(f"{name}, please answer these question for better analyzing your resume")
        with fw.form("Questions"):
            if len(questions) <= 5:
                for i, question in enumerate(questions):
                    answers[i] = fw.text_input(question, key=f"q_{i}")
                submit = fw.form_submit_button("Continue", use_container_width=True, type="secondary")
            elif len(questions) > 5:
                fw.markdown(
                    """
                    <style>
                    [data-testid="stAppViewBlockContainer"] {
                        max-width: 1200px;
                        margin:auto;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )
                col1, col2 = fw.columns(2, gap="medium")  # Create two columns
                for i, question in enumerate(questions):
                    if i < len(questions) // 2:  # Distribute questions between columns
                        answers[i] = col1.text_input(question, key=f"q_{i}")
                    else:
                        answers[i] = col2.text_input(question, key=f"q_{i}")
                submit = fw.form_submit_button("Continue", use_container_width=True, type="secondary")
            if submit:
                if all(answers):
                    with DBConnect() as db:
                        fw.session_state['answers'] = answers
                        questions_answers = []
                        for q, a in zip(questions, answers):
                            qa = f"Question: {q}\nAnswer: {a}\n"
                            questions_answers.append(qa)
                        responses["questions_answers"] = questions_answers
                        db.insert_into_reports(applicant_key=applicant_key, report_table="questions_answers", content="\n".join(questions_answers))
                        fw.switch_page("pages/analysis.py")
                else:
                    fw.warning("Please the answer all questions before proceeding.")


if __name__ == "__main__":
    if "responses" in fw.session_state:
        run()
    else:
        msg = fw.chat_message("assistant", avatar=get_assistant_avatar("error.png"))
        with msg:
            fw.write("You cannot access this page directly....")
        fw.page_link("app.py", label="Home", icon="🏠")
