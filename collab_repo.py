import streamlit as st
import snowflake.connector
import pandas as pd
from urllib.error import URLError

# FMR logo on top - will adjust the align later
st.image('https://www.fidelity.com/bin-public/060_www_fidelity_com/images/Fidelity-footer-logo.png')
# Titles and headers
st.title(":green[Fidelity AMT Learning Days]")
st.divider()
st.header(':blue[Learning Objectives Submission Form]')
st.caption('This tool will assist in finding associates with similar learning interests, enabling collaboration and the set up of study groups')
st.divider()
st.subheader(':orange[Please enter your details:]')

#init session state
if "ideasList" not in st.session_state:
    st.session_state.ideasList = []

#list
quickList = []

# Input fields
username = st.text_input("Your Name:red[*]", "")
st.write(f'You entered User name : {username}')
useremail = st.text_input("Your email:red[*]","")
st.write(f'You entered User Email : {useremail}')
selected_radio = st.radio(
    "What are you interested in achieving during Learning Days?:red[*]",
    ["Learning :open_book:", "Certification :medal:", "Build a project :desktop_computer:"])

if selected_radio == 'Learning :open_book:':
    objective = 'Learning'
    st.write('You selected Learning.')
    
    # Establish a connection to Snowflake
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

    # To display the list of Technologies
    technology_list = "select technology_name from technology"
    my_cur = my_cnx.cursor()
    my_cur.execute(technology_list)
    data = my_cur.fetchall()
    columns = [desc[0] for desc in my_cur.description]
    df = pd.DataFrame(data, columns= ['technology_name'])
    my_cur.close()
    my_cnx.close()

    selected_tech_name = st.selectbox('Choose Learning subject:red[*]', df['technology_name'], key="selectradio1")

    # Create a checkbox to add a new learning idea
    add_new_idea = st.checkbox("Add New Learning Idea")
    if add_new_idea:
            selected_tech_name = st.text_input('your idea:point_down::')

    st.write(f'You have selected : {selected_tech_name}')

elif selected_radio == "Certification :medal:":
    objective = 'Certification'
    st.write('You selected Certification.')
    
    # Establish a connection to Snowflake
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

    # To display the list of Technologies
    certification_list = "select certification_name from certification"
    my_cur = my_cnx.cursor()
    my_cur.execute(certification_list)
    data = my_cur.fetchall()
    columns = [desc[0] for desc in my_cur.description]
    df = pd.DataFrame(data, columns= ['certification_name'])
    my_cur.close()
    my_cnx.close()

    selected_cert_name = st.selectbox('Choose Certification:red[*]', df['certification_name'], key="selectradio2")

    # Create a checkbox to add a new learning idea
    add_new_idea = st.checkbox("Add New Certification Idea")
    if add_new_idea:
            selected_cert_name = st.text_input('your idea:point_down::')

    st.write(f'You have selected : {selected_cert_name}')
else:
    objective = 'Build a project'
    st.write('You selected Build a project.')
    # Establish a connection to Snowflake
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

    # To display the list of Technologies
    project_list = "select project_name from project"
    my_cur = my_cnx.cursor()
    my_cur.execute(project_list)
    data = my_cur.fetchall()
    columns = [desc[0] for desc in my_cur.description]
    df = pd.DataFrame(data, columns= ['project_name'])
    my_cur.close()
    my_cnx.close()

    selected_project_name = st.selectbox('Choose project type to Build:red[*]', df['project_name'], key="selectradio3")

    # Create a checkbox to add a new project idea
    add_new_idea = st.checkbox("Add New Project Idea")
    if add_new_idea:
            selected_project_name = st.text_input('your idea:point_down::')

    st.write(f'You have selected : {selected_project_name}')

objective_description = st.text_area("Brief your objectives", "")
st.write(f'You entered description : {objective_description}')

#Insert a learning record to snowflake
def insert_learning_rec_snf(username,useremail,selected_tech_name,objective,objective_description):
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_cur = my_cnx.cursor()
        insert_learning_rec = f"INSERT INTO MEMBERS_LEARNING (MEMBER_NAME, MEMBER_EMAIL,TECHNOLOGY_NAME,OBJECTIVE_NAME,OBJECTIVE_DESCRIPTION) VALUES ('{username}', '{useremail}','{selected_tech_name}','{objective}','{objective_description}')"
        my_cur.execute(insert_learning_rec)
        my_cnx.commit()
        my_cur.close()
        my_cnx.close()
        st.success("Data inserted successfully!")
    except URLError as e:
        st.error()

#Insert a certification record to snowflake
def insert_cert_rec_snf(username,useremail,selected_cert_name,objective,objective_description):
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_cur = my_cnx.cursor()
        insert_cert_rec = f"INSERT INTO MEMBERS_CERTIFICATION (MEMBER_NAME, MEMBER_EMAIL,CERTIFICATION_NAME,OBJECTIVE_NAME,OBJECTIVE_DESCRIPTION) VALUES ('{username}', '{useremail}','{selected_cert_name}','{objective}','{objective_description}')"
        my_cur.execute(insert_cert_rec)
        my_cnx.commit()
        my_cur.close()
        my_cnx.close()
        st.success("Data inserted successfully!")
    except URLError as e:
        st.error()

#Insert a project record to snowflake
def insert_project_rec_snf(username,useremail,selected_project_name,objective,objective_description):
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_cur = my_cnx.cursor()
        insert_project_rec = f"INSERT INTO MEMBERS_PROJECT (MEMBER_NAME, MEMBER_EMAIL,PROJECT_NAME,OBJECTIVE_NAME,OBJECTIVE_DESCRIPTION) VALUES ('{username}', '{useremail}','{selected_project_name}','{objective}','{objective_description}')"
        my_cur.execute(insert_project_rec)
        my_cnx.commit()
        my_cur.close()
        my_cnx.close()
        st.success("Data inserted successfully!")
    except URLError as e:
        st.error()

if selected_radio == "Learning :open_book:":
    if st.button("Submit your Interest", key="submit1"):
        if username and useremail and selected_tech_name and objective:
            insert_learning_rec_snf(username,useremail,selected_tech_name,objective,objective_description)
        else:
            st.warning("Please check you have entered the values in all the mandatory fields marked with :red[*].")
elif selected_radio == "Certification :medal:":       
    if st.button("Submit your Interest", key="submit2"):
        if username and useremail and selected_cert_name and objective:
            insert_cert_rec_snf(username,useremail,selected_cert_name,objective,objective_description)
        else:
            st.warning("Please check you have entered the values in all the mandatory fields marked with :red[*].")
else:
    if st.button("Submit your Interest", key="submit3"):
        if username and useremail and selected_project_name and objective:
            insert_project_rec_snf(username,useremail,selected_project_name,objective,objective_description)
        else:
            st.warning("Please check you have entered the values in all the mandatory fields marked with :red[*].")
    
#copy technlogy list to data frame
st.divider()
st.subheader(':orange[People with Similar Interests:]')

if selected_radio == 'Learning :open_book:':
# Function to fetch data from Snowflake table
    def fetch_tech_data_snf(selected_tech_name):
        try:
            my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
            my_cur = my_cnx.cursor()
            sql_query = f"SELECT MEMBER_NAME, MEMBER_EMAIL, TECHNOLOGY_NAME, OBJECTIVE_NAME, OBJECTIVE_DESCRIPTION FROM MEMBERS_LEARNING WHERE TECHNOLOGY_NAME = '{selected_tech_name}'"
            my_cur.execute(sql_query)
            tech_data = my_cur.fetch_pandas_all()
            my_cur.close()
            my_cnx.close()
            return tech_data
        except Exception as e:
            st.error(f"Error: {e}")
        return None


elif selected_radio == "Certification :medal:":
    def fetch_tech_data_snf(selected_cert_name):
        try:
            my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
            my_cur = my_cnx.cursor()
            sql_query = f"SELECT MEMBER_NAME, MEMBER_EMAIL, TECHNOLOGY_NAME, OBJECTIVE_NAME, OBJECTIVE_DESCRIPTION FROM MEMBERS_LEARNING WHERE TECHNOLOGY_NAME = '{selected_cert_name}'"
            my_cur.execute(sql_query)
            tech_data = my_cur.fetch_pandas_all()
            my_cur.close()
            my_cnx.close()
            return tech_data
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    st.write(f'You have selected : {selected_cert_name}')
    table_data = fetch_cert_data_snf(selected_cert_name)
    
else:
    def fetch_project_data_snf(selected_project_name):
        try:
            my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
            my_cur = my_cnx.cursor()
            sql_query = f"SELECT MEMBER_NAME, MEMBER_EMAIL, TECHNOLOGY_NAME, OBJECTIVE_NAME, OBJECTIVE_DESCRIPTION FROM MEMBERS_LEARNING WHERE TECHNOLOGY_NAME = '{selected_project_name}'"
            my_cur.execute(sql_query)
            tech_data = my_cur.fetch_pandas_all()
            my_cur.close()
            my_cnx.close()
            return tech_data
        except Exception as e:
            st.error(f"Error: {e}")
            return None

# Streamlit app

    st.write(f'You have selected : {selected_project_name}')

# Fetch data from Snowflake
    table_data = fetch_project_data_snf(selected_project_name)




# Streamlit app

    st.write(f'You have selected : {selected_tech_name}')

# Fetch data from Snowflake
    table_data = fetch_cert_data_snf(selected_tech_name)
# Check if data retrieval was successful
if table_data is not None and not table_data.empty:
    # Display the data in a Streamlit DataFrame
    st.write(table_data)
else:
    # Display a message when no data is found
    st.success('Sorry, no associates have been matched to your learning objectives')

if st.session_state.ideasList:
    st.title("Ideas")
    for idea in st.session_state.ideasList:
        st.write(idea)
