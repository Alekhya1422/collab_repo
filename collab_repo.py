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
objective = st.radio(
    "What are you interested in achieving during Learning Days?:red[*]",
    ["Learning:open_book:", "Certification:medal:", "Build a project:desktop_computer:"])

if objective == 'Learning:open_book:':
    st.write('You selected Learning.')
else:
    if objective == 'Certification:medal:':
        st.write('You selected Certification.')
    else:
        if objective == 'Build a project:desktop_computer:':
            st.write('You selected Build a project.')

objective_description = st.text_area("Brief your objectives", "")
st.write(f'You entered description : {objective_description}')

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

selected_tech_name = st.selectbox('Choose Learning subject:red[*]', df['technology_name'])

if selected_tech_name == 'Other':
    selected_tech_name = st.text_input('Enter the technology name you are interested on :point_down::')

st.write(f'You have selected technology: {selected_tech_name}')

#Insert a record to snowflake
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
        
if st.button("Insert Data"):
    if username and useremail and selected_tech_name and objective:
        insert_learning_rec_snf(username,useremail,selected_tech_name,objective,objective_description)
    else:
        st.warning("Please check you have entered the values in all the mandatory fields marked with :red[*].")
    

#copy technlogy list to data frame

st.divider()

st.subheader(':orange[People with Similar Interests:]')



if st.session_state.ideasList:
    st.title("Ideas")
    for idea in st.session_state.ideasList:
        st.write(idea)
