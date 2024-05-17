import streamlit as fw
import pandas as pd
import sqlite3


# Create a connection to the SQLite database
conn = sqlite3.connect('../db/hmdbq.sqlite')

# Query the "applicants" table
query = "SELECT * FROM applicants"
applicants_data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Display the data as a dataframe using Streamlit
fw.dataframe(applicants_data)