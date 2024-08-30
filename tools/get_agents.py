import os
import pandas as pd
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.error_logger import ErrorLogger


class GetAgentData:
    
    def __init__(self):
        e = None
        self.logger = ErrorLogger()
        try:
            sheet_name = 'Agents'  # replace with your own sheet name
            sheet_id = '1vmcwKyoDp3quMJO99FuuY6Et9m_MPfsfmzeVK-nlGT4'  # replace with your sheet's ID
            # OpenAI Environment
            openai_api = os.getenv("OPENAI_API_KEY")
            os.environ["OPENAI_API_KEY"] = openai_api
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
            selected_column = self.data.loc[self.data['role'] == agent_name, column_name]

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

    
    def return_document_expert(self):
        try:
            agent_name = "Document Expert"
            headers = self.get_sheet_headers()
            agent_details = {}
            found_agent = False
            for role in self.data["role"]:
                if role == agent_name:
                    agent_details["role"] = role
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        # Check if details is a list with a single boolean element
                        if isinstance(details, list) and len(details) == 1 and isinstance(details[0], bool):
                            agent_details[header] = details[0]
                        else:
                            agent_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Agent(
                role=agent_details['role'][0],
                goal=agent_details['goal'][0],
                backstory=agent_details['backstory'][0],
                allow_delegation=agent_details['allow_delegation'],
                verbose=agent_details['verbose'],
                llm=ChatOpenAI(
                    model_name="gpt-3.5-turbo-0125",
                    temperature=agent_details['temperature'][0]
                )
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    
    def return_human_resources_manager(self):
        try:
            agent_name = "Human Resources Manager"
            headers = self.get_sheet_headers()
            agent_details = {}
            found_agent = False
            for role in self.data["role"]:
                if role == agent_name:
                    agent_details["role"] = role
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        # Check if details is a list with a single boolean element
                        if isinstance(details, list) and len(details) == 1 and isinstance(details[0], bool):
                            agent_details[header] = details[0]
                        else:
                            agent_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Agent(
                role=agent_details['role'][0],
                goal=agent_details['goal'][0],
                backstory=agent_details['backstory'][0],
                allow_delegation=agent_details['allow_delegation'],
                verbose=agent_details['verbose'],
                llm=ChatOpenAI(
                    model_name="gpt-3.5-turbo-0125",
                    temperature=0.2
                )
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    
    def return_recruitment_manager(self):
        try:
            agent_name = "Recruitment Manager"
            headers = self.get_sheet_headers()
            agent_details = {}
            found_agent = False
            for role in self.data["role"]:
                if role == agent_name:
                    agent_details["role"] = role
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        # Check if details is a list with a single boolean element
                        if isinstance(details, list) and len(details) == 1 and isinstance(details[0], bool):
                            agent_details[header] = details[0]
                        else:
                            agent_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Agent(
                role=agent_details['role'][0],
                goal=agent_details['goal'][0],
                backstory=agent_details['backstory'][0],
                allow_delegation=agent_details['allow_delegation'],
                verbose=agent_details['verbose'],
                llm=ChatOpenAI(
                    model_name="gpt-3.5-turbo-0125",
                    temperature=0.3
                )
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    
    def return_human_resources_director(self):
        try:
            agent_name = "Human Resources Director"
            headers = self.get_sheet_headers()
            agent_details = {}
            found_agent = False
            for role in self.data["role"]:
                if role == agent_name:
                    agent_details["role"] = role
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        # Check if details is a list with a single boolean element
                        if isinstance(details, list) and len(details) == 1 and isinstance(details[0], bool):
                            agent_details[header] = details[0]
                        else:
                            agent_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Agent(
                role=agent_details['role'][0],
                goal=agent_details['goal'][0],
                backstory=agent_details['backstory'][0],
                allow_delegation=agent_details['allow_delegation'],
                verbose=agent_details['verbose'],
                llm=ChatOpenAI(
                    model_name="gpt-3.5-turbo-0125",
                    temperature=0.4
                )
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)

    
    def return_chief_of_hr(self):
        try:
            agent_name = "Chief of Human Resources Officer"
            headers = self.get_sheet_headers()
            agent_details = {}
            found_agent = False
            for role in self.data["role"]:
                if role == agent_name:
                    agent_details["role"] = role
                    for header in headers:
                        details = self.get_custom_column(agent_name, header)
                        # Check if details is a list with a single boolean element
                        if isinstance(details, list) and len(details) == 1 and isinstance(details[0], bool):
                            agent_details[header] = details[0]
                        else:
                            agent_details[header] = details
                    found_agent = True
                    break  # Exit the loop once the agent is found
            if not found_agent:
                return "NO"
            return Agent(
                role=agent_details['role'][0],
                goal=agent_details['goal'][0],
                backstory=agent_details['backstory'][0],
                allow_delegation=agent_details['allow_delegation'],
                verbose=agent_details['verbose'],
                llm=ChatOpenAI(
                    model_name="gpt-3.5-turbo-0125",
                    temperature=0.7
                )
            )
        except Exception as error:
            e = error
        if e:
            self.logger.log_error_from_exception(applicant_id=1, applicant_ip='127.0.0.1', page='test_page', exception=e)



