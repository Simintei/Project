import streamlit as st
from streamlit_option_menu import option_menu
from deta import Deta
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

def database_connection():
     #initialize Deta with a Data Key
     deta = Deta("d0c1hbc46rd_MTAekjBwfngvDZrCY4fy3V53Bt56G9fA")
     db = deta.Base("UsersDB")
     db1 = deta.Base("JobsDB")
     db2 = deta.Base("accepted_jobs")
     return db,db1,db2

db,db1,db2 = database_connection()


st.title("User Profile")

menu = ["Login","SignUp"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    def getusers():
        users = db.fetch().items
        return users
    users= getusers()
    names = [user["name"] for user in users]
    usernames=[user["key"] for user in users]
    roles=[user["role"] for user in users]
    passwords=[user["password"] for user in users]
    hashed_passwords = stauth.Hasher(passwords).generate()
    authenticator = stauth.Authenticate(names,usernames, hashed_passwords,'cookie', 'secret',cookie_expiry_days=30)
    
    name,username, authentication_status = authenticator.login('Login','sidebar')

    if st.session_state['authentication_status']:
        #get the user role
        user_role = roles[usernames.index(st.session_state['username'])]
        if user_role == "Client":
            authenticator.logout('Logout','sidebar')
            st.write("You are logged in as", st.session_state['username'])

            st.subheader("Add a Job")
            with st.form(key='my_form'):
                title= st.text_input("Job Title")
                date= str(st.date_input("Date"))              
                job_description= st.text_input("Job Description")
                location=st.text_input("Pickup Location")
                destination=st.text_input("Destination")
                if st.form_submit_button("Submit"):
                    db1.put({"title":title,"date":date,"job_description":job_description,"location":location,"destination":destination})
                    st.success("Job added successfully")
                
        elif user_role == "Driver":
            authenticator.logout('Logout','sidebar')
            st.write("You are logged in as", st.session_state['username'])
            st.subheader("Available Jobs")
            jobs = db1.fetch().items
            selected2 = option_menu(
                menu_title = None,
                options = ["Available jobs","Accepted jobs"],
                icons = ["inbox_tray","outbox_tray"],
                default_index = 0,
                orientation = "horizontal",
            )
            if selected2 == "Available jobs":
            #show the jobs in a forms with unique keys within three columns
                for job in jobs:
                    with st.form(key=job["key"]):
                        st.write("Job Title:",job["title"])
                        st.write("Date:",job["date"])
                        st.write("Job Description:",job["job_description"])
                        st.write("Pickup Location:",job["location"])
                        st.write("Destination:",job["destination"])
                        if st.form_submit_button("Accept"):                        #move the job to the accepted jobs database and delete it from the jobs database and save the driver username
                            db2.put({"title":job["title"],"date":job["date"],"job_description":job["job_description"],"location":job["location"],"destination":job["destination"],"driver":st.session_state['username']})
                            db1.delete(job["key"])
                            st.success("Job accepted and moved to accepted jobs successfully")
            elif selected2 == "Accepted jobs":
                accepted_jobs = db2.fetch().items
                for job in accepted_jobs:
                    if job["driver"] == st.session_state['username']:
                        with st.form(key=job["key"]):
                            st.write("Job Title:",job["title"])
                            st.write("Date:",job["date"])
                            st.write("Job Description:",job["job_description"])
                            st.write("Pickup Location:",job["location"])
                            st.write("Destination:",job["destination"])
                            if st.form_submit_button("Complete"):                  
                                db2.delete(job["key"])
                                st.success("Job completed and moved to completed jobs successfully")
elif choice == "SignUp":
    st.subheader("Create New Account")
    new_name = st.text_input("Name")
    new_user = st.text_input ("Username")
    new_role = st.selectbox("Role",["Driver","Client"])
    new_password = st.text_input("Password", type='password')


    if st.button("SignUp"):
        db.put({"key":new_user,"name":new_name,"role":new_role,"password":new_password})
        st.success("You have successfully created an account") 
        st.info("Go to Login Menu to login")


     
 
 


