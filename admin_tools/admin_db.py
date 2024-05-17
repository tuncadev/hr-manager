import os
import sqlite3
import panda as pd
from dotenv import dotenv_values
import streamlit as fw
from tools import encryption_manager
from tools.encryption_manager import EncryptionManager

class AdminDBConnect:

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
    def select_all_from(self, table_name):
        if table_name is None:
            return None
        query = f"SELECT * FROM {table_name}"
        self.c.execute(query)
        applicants_data = self.c.fetchall()
        self.conn.commit()
        return applicants_data