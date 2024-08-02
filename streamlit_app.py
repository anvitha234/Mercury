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

# Welcome page
st.title("Mercury")
st.write("Greek god of friendship")
st.write("Cultivating Meaningful Connections")

# Choice between sign in and register
choice = st.selectbox("What would you like to do?", ["Sign In", "Register"])

if choice == "Sign In":
    # Sign in page
    st.title("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.button("Sign In")
    if submit_button:
        result = sign_in(email, password)
        st.success(result)
        st.experimental_set_query_params(page="check_back_in")
elif choice == "Register":
    # Registration form
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
            st.experimental_set_query_params(page="tell_us_about_yourself")
        else:
            st.error("Passwords do not match. Please try again.")

# Check if the user has been redirected to a new page
params = st.query_params    
if params.get("page"):
    page = params["page"][0]
    if page == "check_back_in":
        # Check back in page
        st.title("Check back in with us")
        st.write("Welcome back!")
    elif page == "tell_us_about_yourself":
        # Tell us about yourself page
        st.title("Tell us about yourself")
        st.write("We're excited to get to know you better!")

# Display user data
st.write("Registered Users:")
st.write(user_data)