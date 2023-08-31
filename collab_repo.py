import streamlit as st
import snowflake.connector
import pandas as pd

# FMR logo on top - will adjust the align later
st.image('https://www.fidelity.com/bin-public/060_www_fidelity_com/images/Fidelity-footer-logo.png')
# Titles and headers
st.title("Fidelity AMT Learning Days")
st.divider()
st.header('Learning Objectives Submission Form')
st.caption('This tool will assist in finding associates with similar learning interests, enabling collaboration and the set up of study groups')
st.divider()
st.subheader('Please enter your details:')

#init session state
if "ideasList" not in st.session_state:
    st.session_state.ideasList = []

#list
quickList = []

# Input fields
userName = st.text_input("Your Name", "")
userEmail = st.text_input("Your email","")
technology = st.multiselect(
    'Interested Technologies ',
    ['Azure', 'Snowflake', 'AWS', 'Oracle','PowerBI', 'Tableau','Submit New Idea'])

if "Submit New Idea" in technology:
    yourIdea = st.text_input("Your Ideas")

st.write('You selected:', technology)

objective = st.radio(
    "What is  your objective",
    ["Learning:open_book:", "Certification:medal:", "Build a project:desktop_computer:"])

if objective == 'Learning:open_book:':
    st.write('You selected Learning.')
else:
    if objective == 'Certification:medal:':
        st.write('You selected Certification.')
    else:
        if objective == 'Build a project:desktop_computer:':
            st.write('You selected Build a project.')

objectives = st.text_area("Brief your objectives", "")

# Submit button
if st.button("Submit"):
    if userName and objectives and technology:
        
        for tech in technology:
            if tech == 'Submit New Idea':
                continue
            quickList.append(tech)
        st.session_state.ideasList.append(f"{userName} : Study ideas: {quickList}    My Objectives: {objectives}") 


    else:
        st.warning("Please fill in both your name and learning objectives.")
 #display ideas back to the user

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

#Snowflake-related functions
def get_technology_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from technology")
    return my_cur.fetchall()

# Add a button to load the fruit
if st.button('Select a interested technology'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_technology_list()
  my_cnx.close()
  st.dataframe(my_data_rows) 


df = pd.DataFrame(my_data_rows)
df.columns = [
    c.replace(', ', '').replace('(', '').replace(')', '') 
    for c in df.columns
]
my_data_rows = df[df.columns]

my_data_rows.dftype

my_data_rows= my_data_rows.astype(object)
my_data_rows

technology2 = st.multiselect( 'Interested Technologies ', my_data_rows)


if "Submit New Idea" in technology2:
    yourIdea = st.text_input("Your Ideas")
    


st.divider()

st.subheader('People with Similar Interests:')



if st.session_state.ideasList:
    st.title("Ideas")
    for idea in st.session_state.ideasList:
        st.write(idea)
