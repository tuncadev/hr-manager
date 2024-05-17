import os
import sqlite3
from sqlite3 import Error as SQLiteError
from datetime import datetime
import traceback

class ErrorLogger:
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

    def log_error(self, applicant_id, applicant_ip, error_page, error_class, error_function, error_type, error_message, file_name, line_number):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO error_logs (applicant_id, applicant_ip, error_page, error_class, error_function, error_type, error_message, file_name, line_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (applicant_id, applicant_ip, error_page, error_class, error_function, error_type, error_message, file_name, line_number))
            conn.commit()
        except SQLiteError as e:
            print(f"Error logging to database: {e}")

    def log_error_from_exception(self, applicant_id, applicant_ip, page, exception):
        error_message = str(exception)
        error_type = type(exception).__name__

        # Get the file name and line number where the error occurred
        tb = traceback.extract_tb(exception.__traceback__)[0]
        file_name = tb.filename
        line_number = tb.lineno

        # Check if the same error has already been logged
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM error_logs WHERE error_message = ? AND file_name = ? AND line_number = ?",
                           (error_message, file_name, line_number))
            count = cursor.fetchone()[0]
            if count > 0:
                print("Error already logged. Skipping...")
                return
        except SQLiteError as e:
            print(f"Error checking if error already logged: {e}")

        # If the error has not been logged yet, log it
        self.log_error(applicant_id=applicant_id, applicant_ip=applicant_ip, error_page=page,
                       error_class=None, error_function=None, error_type=error_type, error_message=error_message,
                       file_name=file_name, line_number=line_number)
