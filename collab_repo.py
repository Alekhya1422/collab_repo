import streamlit as st
import snowflake.connector
import pandas as pd

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


# Establish a connection to Snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

# Snowflake query to retrieve data from a table
query = "select * from technology"

# Execute the query and fetch data into a Pandas DataFrame
my_cur = my_cnx.cursor()
my_cur.execute(query)

# Fetch all the data into a Pandas DataFrame
data = my_cur.fetchall()
columns = [desc[0] for desc in my_cur.description]

# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=columns)

# Close the Snowflake connection
my_cnx.close()

# Display the Pandas DataFrame
print(df.head())

# Select a value from the DataFrame using st.radio
selected_name = st.radio('Select a name:', df['technology_name'])

# Display the selected name
st.write(f'You selected: {selected_name}')



# Add a button to load the fruit
#my_data_rows = get_technology_list()
#data = my_cur.fetchall()
#my_cnx.close()


#df = pd.DataFrame(my_data_rows, columns =['technology_name']
#print(df.head())

#technology2 = st.radio('Interested Technologies', df['technology_name'])
#st.write('You selected:', technology2)

#selected_name = st.radio('Select a name:', df['Names'])


#copy technlogy list to data frame

st.divider()

st.subheader(':orange[People with Similar Interests:]')



if st.session_state.ideasList:
    st.title("Ideas")
    for idea in st.session_state.ideasList:
        st.write(idea)
