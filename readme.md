# CV Analysis Application
This application is designed to assist job applicants in analyzing their CVs for specific job vacancies. It uses OpenAI's GPT model to provide feedback on the CV's suitability for the selected vacancy.

## Index
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Navigate to App Folder](#navigate-to-app-folder)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Activate the Virtual Environment](#activate-the-virtual-environment)
    - [On Windows](#on-windows)
    - [On macOS and Linux](#on-macos-and-linux)
    - [Install Dependencies](#install-dependencies)
  - [Create a .env File](#create-a-env-file)
  - [Run the Application](#run-the-application)

## Features

* User-friendly web interface for submitting personal information and CV.
* Supports multiple file formats for CV upload (PDF, DOCX, TXT).
* Integration with OpenAI's GPT model for intelligent analysis.
* Real-time feedback on CV suitability for the selected job vacancy.

## Requirements
* Python 3.12
* Microsoft Visual C++ 14.0 or greater

## Installation

To run this application, you need to have Python installed on your system. Follow these steps to set up the application:

### Clone the Repository
```bash
git clone https://github.com/tuncadev/hr-manager.git
```
### Navigate to App Folder
```bash
cd hr-manager
```

### Create a Virtual Environment
```bash
python3 -m venv venv
```

### Activate the Virtual Environment
#### On Windows:
```bash
 .\venv\Scripts\activate
```
#### On macOS and Linux:
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create a .env File
#### Insert your OpenAI API Key:
```bash
OPENAI_API_KEY="Your-OpenAI-API-Key-Here"
```

### Run the Application
```bash
streamlit run app.py
```

**Ensure that all prerequisites like Python and Microsoft Visual C++ are properly installed before proceeding with the application setup.**
