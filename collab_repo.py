import streamlit as st
import snowflake.connector
import pandas as pd
from urllib.error import URLError

# Function to establish a Snowflake connection
def connect_to_snowflake():
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        return my_cnx
    except URLError as e:
        st.error("Snowflake connection error.")
        return None

# Function to retrieve data from Snowflake based on the selected objective
def fetch_data_from_snowflake(selected_tech_name, objective):
    try:
        my_cnx = connect_to_snowflake()
        if my_cnx:
            my_cur = my_cnx.cursor()
            table_name = "MEMBERS_LEARNING" if objective == "Learning" else "MEMBERS_CERTIFICATION" if objective == "Certification" else "MEMBERS_PROJECT"
            sql_query = f"SELECT MEMBER_NAME, MEMBER_EMAIL, TECHNOLOGY_NAME, OBJECTIVE_NAME, OBJECTIVE_DESCRIPTION FROM {table_name} WHERE TECHNOLOGY_NAME = '{selected_tech_name}'"
            my_cur.execute(sql_query)
            tech_data = my_cur.fetch_pandas_all()
            my_cur.close()
            my_cnx.close()
            return tech_data
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app
st.image('https://www.fidelity.com/bin-public/060_www_fidelity_com/images/Fidelity-footer-logo.png')
st.title(":green[Fidelity AMT Learning Days]")
st.divider()
st.header(':blue[Learning Objectives Submission Form]')
st.caption('This tool will assist in finding associates with similar learning interests, enabling collaboration and the set up of study groups')
st.divider()
st.subheader(':orange[Please enter your details:]')

# Input fields
username = st.text_input("Your Name:red[*]", "")
useremail = st.text_input("Your email:red[*]", "")
selected_radio = st.radio(
    "What are you interested in achieving during Learning Days?:red[*]",
    ["Learning :open_book:", "Certification :medal:", "Build a project :desktop_computer:"])

if selected_radio == 'Learning :open_book:':
    objective = 'Learning'
    st.write('You selected Learning.')
elif selected_radio == "Certification :medal:":
    objective = 'Certification'
    st.write('You selected Certification.')
else:
    objective = 'Build a project'
    st.write('You selected Build a project.')

# Fetch data from Snowflake based on the selected objective
if selected_radio in ['Learning :open_book:', 'Certification :medal:', 'Build a project :desktop_computer:']:
    my_cnx = connect_to_snowflake()
    if my_cnx:
        my_cur = my_cnx.cursor()
        table_name = "technology" if objective == "Learning" else "certification" if objective == "Certification" else "project"
        
        # Check if the table exists in Snowflake before executing the query
        check_table_query = f"SHOW TABLES LIKE '{table_name.upper()}'"
        my_cur.execute(check_table_query)
        if my_cur.fetchone():
            sql_query = f"SELECT {table_name}_name FROM {table_name}"
            my_cur.execute(sql_query)
            data = my_cur.fetchall()
            columns = [desc[0] for desc in my_cur.description]
            df = pd.DataFrame(data, columns=[f'{table_name}_name'])
            my_cur.close()
            my_cnx.close()

            selected_item = st.selectbox(f'Choose {table_name.replace("_", " ").title()}:red[*]', df[f'{table_name}_name'], key="selectradio")
            st.write(f'You have selected : {selected_item}')

            # Create a checkbox to add a new learning idea, certification, or project
            add_new_idea = st.checkbox(f"Add New {table_name.replace('_', ' ').title()} Idea")
            if add_new_idea:
                selected_item = st.text_input(f'Your idea:point_down::')

            # User objective description input
            objective_description = st.text_area("Brief your objectives", "")
            st.write(f'You entered description: {objective_description}')

            # Button to submit user interest
            if st.button(f"Submit your Interest for {table_name.replace('_', ' ').title()}", key="submit"):
                if username and useremail and selected_item and objective:
                    try:
                        my_cnx = connect_to_snowflake()
                        if my_cnx:
                            my_cur = my_cnx.cursor()
                            table_name = f"MEMBERS_{table_name.upper()}"
                            insert_query = f"INSERT INTO {table_name} (MEMBER_NAME, MEMBER_EMAIL, {table_name[:-1].upper()}_NAME, OBJECTIVE_NAME, OBJECTIVE_DESCRIPTION) VALUES ('{username}', '{useremail}','{selected_item}','{objective}','{objective_description}')"
                            my_cur.execute(insert_query)
                            my_cnx.commit()
                            my_cur.close()
                            my_cnx.close()
                            st.success("Data inserted successfully!")
                    except URLError as e:
                        st.error("Error inserting data into Snowflake.")
                else:
                    st.warning("Please check you have entered values in all the mandatory fields marked with :red[*].")
        else:
            st.error(f"'{table_name}' table does not exist in Snowflake.")
    else:
        st.error("Error connecting to Snowflake.")
        
# Fetch and display data from Snowflake
if selected_radio in ['Learning :open_book:', 'Certification :medal:', 'Build a project :desktop_computer:']:
    st.divider()
    st.subheader(':orange[People with Similar Interests:]')
    table_data = fetch_data_from_snowflake(selected_item, objective)
    
    if table_data is not None and not table_data.empty:
        st.write("Data from Snowflake Table:")
        st.write(table_data)
    else:
        st.success('Sorry, no associates have been matched to your learning objectives')
