import streamlit as st
import mysql.connector
import hashlib

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='rnsit@007',
        database='tours'
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def home_page():
    st.title('Tourism Management System')
    st.write('Welcome to the Tourism Management System')

def signup_page():
    st.title('Sign Up')
    name = st.text_input('Name')
    phone_no = st.number_input('Phone Number', min_value=0)  # Changed phone number to number_input
    email = st.text_input('Email')
    dob = st.date_input('Date of Birth')
    age = st.number_input('Age', min_value=0)
    password = st.text_input('Password', type='password')
    if st.button('Sign Up'):
        hashed_password = hash_password(password)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO TOURIST (Name, PhoneNo, EmailID, DOB, Age, Password)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, phone_no, email, dob, age, hashed_password))
        conn.commit()
        conn.close()
        st.success('Signup successful!')

def login_page():
    st.title('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        hashed_password = hash_password(password)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM TOURIST WHERE EmailID=%s AND Password=%s
        ''', (email, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            st.success('Login successful!')
        else:
            st.error('Invalid email or password')

pages = {
    'Home': home_page,
    'Login': login_page,
    'Sign Up': signup_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.selectbox('Go to', list(pages.keys()))  # Changed to dropdown

page = pages[selection]
page()
