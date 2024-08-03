import streamlit as st
import pandas as pd

# Create a dataframe to store user data
user_data = pd.DataFrame(columns=['Name', 'Email', 'Password'])

# Function to register a new user
def register_user(name, email, password):
    new_user = pd.DataFrame({'Name': [name], 'Email': [email], 'Password': [password]})
    user_data.loc[len(user_data)] = [name, email, password]
    return "User registered successfully!"

# Function to sign in a user
def sign_in(email, password):
    # TO DO: implement sign in logic here
    return "Sign in successful!"

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Welcome", "Sign In", "Register", "Find a Friend", "Meet a Mentor"])

if page == "Welcome":
    st.title("Mercury")
    st.write("Greek God of Friendship")
    st.write("Cultivating Meaningful Connections")

elif page == "Sign In":
    st.title("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.button("Sign In")
    if submit_button:
        result = sign_in(email, password)
        st.success(result)

elif page == "Register":
    st.title("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit_button = st.button("Register")
    if submit_button:
        if password == confirm_password:
            result = register_user(name, email, password)
            st.success(result)
        else:
            st.error("Passwords do not match. Please try again.")

elif page == "Find a Friend":
    import findfriend
    findfriend.main()

elif page == "Meet a Mentor":
    import meetmentor
    meetmentor.main()

# Display user data on welcome page
if page == "Welcome":
    st.write("Registered Users:")
    st.write(user_data)
