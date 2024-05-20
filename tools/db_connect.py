import os
import sqlite3
import streamlit as st
from IPython.display import display
from dotenv import dotenv_values
from tools.encryption_manager import EncryptionManager
import pandas as pd


class DBConnect:

    def __init__(self, db_name='hmdbq.sqlite', db_folder='db'):
        current_dir = os.path.dirname(
            os.path.abspath(__file__))  # Get the directory of the current
        project_dir = os.path.dirname(current_dir)  # Get the parent app directory
        db_path = os.path.join(project_dir, db_folder, db_name)
        self.db_path = db_path
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    # Connections for Vacancies
    def is_vacancies_table_empty(self):
        self.c.execute("SELECT COUNT(*) FROM vacancies")
        result = self.c.fetchone()
        return result[0] == 0

    def update_vacancy(self, vacancy):
        vacancy_name = vacancy['Vacancy Name']
        self.c.execute("UPDATE vacancies SET Vacancy_Requirements=?, Vacancy_Requirements_Affect=?, "
                       "Vacancy_Would_Be_Plus=?, Vacancy_Would_Be_Plus_Affect=?, date_updated=CURRENT_TIMESTAMP "
                       "WHERE Vacancy_Name=?", (vacancy['Vacancy Requirements'], vacancy['Vacancy Requirements affect'],
                                                vacancy['Vacancy Would be Plus'], vacancy['Vacancy Would be Plus Affect'],
                                                vacancy_name))
        self.conn.commit()

    def delete_vacancy(self, vacancy_name):
        self.c.execute("DELETE FROM vacancies WHERE Vacancy_Name = ?", (vacancy_name,))
        self.conn.commit()

    def insert_into_vacancies(self, vacancy):
        self.c.execute("INSERT INTO vacancies (Vacancy_Name, Vacancy_Requirements, Vacancy_Requirements_Affect, "
                       "Vacancy_Would_Be_Plus, Vacancy_Would_Be_Plus_Affect, date_created, date_updated) "
                       "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                       (vacancy['Vacancy Name'], vacancy['Vacancy Requirements'], vacancy['Vacancy Requirements affect'],
                        vacancy['Vacancy Would be Plus'], vacancy['Vacancy Would be Plus Affect']))
        self.conn.commit()

    def insert_or_update_vacancies(self, vacancies):
        for vacancy in vacancies:
            vacancy_name = vacancy['Vacancy Name']
            self.c.execute("SELECT * FROM vacancies WHERE Vacancy_Name=?", (vacancy_name,))
            existing_vacancy = self.c.fetchone()
            if existing_vacancy:
                self.update_vacancy(vacancy)
            else:
                self.insert_into_vacancies(vacancy)

    def get_vacancy_names(self):
        self.c.execute("SELECT Vacancy_Name FROM vacancies")
        vacancy_names = self.c.fetchall()
        return [name[0] for name in vacancy_names]

    def get_vac_details(self, vacancy_name):
        self.c.execute("SELECT * FROM vacancies WHERE Vacancy_Name=?", (vacancy_name,))
        vacancy_details = self.c.fetchone()
        headers = self.get_vacancy_headers()
        formatted_details = {}
        if vacancy_details:
            for header, value in zip(headers[1:], vacancy_details[1:]):
                formatted_details[header] = value
        return formatted_details

    def get_vacancy_headers(self):
        self.c.execute("PRAGMA table_info(vacancies)")
        headers = self.c.fetchall()
        column_names = [header[1] for header in headers]
        return column_names

    # App connections for applicants

    def select_from(self, table_name=None):
        """Fetches data from a table as a pandas DataFrame."""
        try:
            query = f"SELECT * FROM {table_name}"
            self.c.execute(query)
            data = self.c.fetchall()
            df = pd.DataFrame(data, columns=[col[0] for col in self.c.description])
            return df
        except sqlite3.Error as error:
            st.error(f"Error connecting to database: {error}")
            return None

    def get_formatted_table_names(self):
        """Fetches all table names and returns them formatted."""
        try:
            # Retrieve all table names
            self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.c.fetchall()

            # Format table names
            formatted_table_names = []
            for table in tables:
                original_name = table[0]
                formatted_name = original_name.replace('_', ' ').title()
                formatted_table_names.append((formatted_name, original_name))  # Keep both formatted and original names

            return formatted_table_names
        except sqlite3.Error as error:
            st.error(f"Error connecting to database: {error}")
            return None


    def get_resumes_with_names(self):
        """Fetches resumes with applicant names"""
        try:
            query = """
              SELECT r.applicant_id, a.name, r.content
              FROM resumes r
              INNER JOIN applicants a ON r.applicant_id = a.id
            """
            self.c.execute(query)
            data = self.c.fetchall()
            df = pd.DataFrame(data, columns=["applicant_id", "applicant_name", "content"])
            return df
        except sqlite3.Error as error:
            print("Error connecting to database:", error)
            return None  # Or handle error differently

    def create_applicant(self, applicant_key, name, email, selected_vac_name, selected_vac_details, start, end=None, last_page=None):
        while True:
            self.c.execute("SELECT applicant_key FROM applicants WHERE applicant_key = ?", (applicant_key,))
            existing_folder = self.c.fetchone()
            if existing_folder is None or not existing_folder:
                break  # Exit the loop if the folder name is unique or if there are no records
        self.c.execute(
            "INSERT INTO applicants (applicant_key, name, email, selected_vac_name, selected_vac_details, start, end, last_page) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (applicant_key, name, email, selected_vac_name, selected_vac_details, start, end,  last_page))
        self.conn.commit()
        return self.c.lastrowid

    def update_table(self, table_name, applicant_id, columns):
        if columns:
            if table_name == "applicants":
                where = "id"
            else:
                where = "applicant_id"
            set_clause = ', '.join([f"{column} = ?" for column in columns.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where} = ?"
            values = list(columns.values()) + [applicant_id]
            self.c.execute(query, values)
            self.conn.commit()

    def insert_into_resumes(self, applicant_id=None, content=None):
        encryption_manager = EncryptionManager(applicant_id=applicant_id)
        # encrypted_text = encryption_manager.encrypt_data(content)
        encrypted_text = content
        # Insert into DB CV content
        self.c.execute("INSERT INTO resumes (applicant_id, content) VALUES (?, ?)", (applicant_id, encrypted_text))
        self.conn.commit()

    def select_from_resumes(self, applicant_id=None):
        query = f"SELECT content FROM resumes WHERE applicant_id = '{applicant_id}'"
        self.c.execute(query)
        result = self.c.fetchone()
        if result is not None and result[0] is not None:
            # env_vars = dotenv_values('env/.data')
            # key = env_vars.get(f'{applicant_id}')
            # encryption_manager = EncryptionManager(applicant_id=applicant_id, key=f"{key}")
            # content = result[0]  # Extract the content from the tuple
            # decrypted_text = encryption_manager.decrypt_data(content)
            self.conn.commit()
            # return decrypted_text  # Return the fetched result
            return result[0]
        else:
            self.conn.commit()
            return False

    def select_from_analysis(self, applicant_id=None, table_name=None):
        query = f"SELECT content FROM {table_name} WHERE applicant_id = ?"
        self.c.execute(query, (applicant_id,))
        # Fetch the results if needed
        result = self.c.fetchone()
        self.conn.commit()
        if result:
            return "\n".join(result)  # Return the fetched result
        else:
            return None  # Return None if no result is found

    def get_selected_vac_details(self, applicant_id=None):
        self.c.execute("SELECT selected_vac_details FROM applicants WHERE id=?", (applicant_id,))
        vacancy_details = self.c.fetchone()
        self.conn.commit()
        return vacancy_details

    def insert_into_reports(self, applicant_id=None, report_table=None, content=None):
        query = f"INSERT INTO {report_table} (applicant_id, content) VALUES (?, ?)"
        self.c.execute(query, (applicant_id, content))
        self.conn.commit()

    def get_applicant_name(self, applicant_id=None):
        self.c.execute("SELECT name FROM applicants WHERE id=?", (applicant_id,))
        applicant_name = self.c.fetchone()
        self.conn.commit()
        return applicant_name

    def get_lastpage(self, applicant_key=None):
        if applicant_key is None:
            return None
        self.c.execute("SELECT last_page FROM applicants WHERE applicant_key=?", (applicant_key,))
        last_page = self.c.fetchone()
        self.conn.commit()
        return last_page

    def get_applicant_details(self, applicant_id=None):
        if applicant_id is None:
            return None
        self.c.execute("SELECT * FROM applicants WHERE id=? ", (applicant_id,))
        row = self.c.fetchone()

        if row is not None:
            # Get column names from the cursor's description
            columns = [column[0] for column in self.c.description]
            # Construct result dictionary with non-empty values
            result_dict = {columns[i]: row[i] for i in range(len(columns)) if row[i] is not None}
            return result_dict

        self.conn.commit()
        return None

    def get_applicant_continue_details(self, applicant_key=None):
        if applicant_key is None:
            return None
        self.c.execute("SELECT * FROM applicants WHERE applicant_key=? ", (applicant_key,))
        row = self.c.fetchone()
        if row is not None:
            # Get column names from the cursor's description
            columns = [column[0] for column in self.c.description]
            # Construct result dictionary with non-empty values
            result_dict = {columns[i]: row[i] for i in range(len(columns)) if row[i] is not None}
            return result_dict

        self.conn.commit()
        return None