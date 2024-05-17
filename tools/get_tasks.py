from tools.error_logger import ErrorLogger
import pandas as pd
from crewai import Task

class GetTaskData:
    def __init__(self):
        e = None
        self.logger = ErrorLogger()
        try:
            sheet_name = 'Tasks'  # replace with your own sheet name
            sheet_id = '1NTrc1Oxt_-f-h0ThZ9qR0uZmtnVOJ_RNp45-1tZ1H-M'  # replace with your sheet's ID
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            self.data = pd.read_csv(url).fillna('Unknown')
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    def get_sheet_headers(self):  # Get the first row of the DataFrame
        try:
            first_row = self.data.iloc[0]
            # Filter columns to exclude those with empty values in the first row
            non_empty_columns = first_row[first_row != 'Unknown']
            return non_empty_columns.index.tolist()
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    def get_custom_column(self, agent_name, column_name):
        try:
            # Select the column for the specified vacancy name
            selected_column = self.data.loc[self.data['agent'] == agent_name, column_name]

            # Check if any rows were found
            if not selected_column.empty:
                # Handle missing values
                selected_column = selected_column.fillna('Unknown')
                # Return the selected column
                return selected_column.tolist()
            else:
                return f"No data found for 'Vacancy Name' equals {agent_name}"
        except KeyError:
            return f"Column '{column_name}' not found"
        except Exception as e:
            return f"An error occurred: {e}"

    def return_task(self, agent_name, agent_instance=None, vac=None, res=None, first_analysis=None, questions_answers=None, final_report=None):
        try:
            headers = self.get_sheet_headers()
            task_details = {}
            found_agent = False
            for agent in self.data["agent"]:

                if agent == agent_name:
                    task_details["agent"] = agent
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        task_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Task(
                description=f"{task_details['description'][0].format(vacancy=vac, resume=res, first_analysis_report=first_analysis, questions_answers=questions_answers, final_report=final_report)}",
                expected_output=f"{task_details['expected_output'][0]}",
                agent=agent_instance
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

