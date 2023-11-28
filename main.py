from backend.backend import run_llm
from vectorization.ingestion import ingest_docs
import streamlit as st
from streamlit_chat import message
import base64,io,os, pickle, bcrypt
from pathlib import Path
from typing import List,Tuple
from fpdf import FPDF

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_chat_history(chat_history: List[Tuple[str, str]]):
    for i, (generated_response, user_query) in enumerate(chat_history):
        message(f"{user_query}\n\n{generated_response}", is_user=True, key=f"user_query_{i}")

def txt_to_pdf(txt_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("times", size=12)  # Using the 'times' font
    pdf.multi_cell(0, 10, txt_content)
    return pdf

#Password Managment
file_path = Path(__file__).parent / "hashed_passwords.pkl"

if not os.path.exists(file_path):
    hashed_passwords = {}
    with open(file_path, "wb") as f:
        pickle.dump(hashed_passwords, f)
else:
    with open(file_path, "rb") as f:
        hashed_passwords = pickle.load(f)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login():
    # Subtitle with a stylish underline
    st.markdown(
        """
        <style>
            .title {
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header with title, GitHub, and LinkedIn icons
    st.markdown(
        "<h2 class='title'>Welcome to DocConvo <img src='data:image/jpg;base64,{}' style='margin-left: 10px; width: 30px; height: 30px;'></h2>".format(
            get_base64_of_bin_file("images/doc_convo_icon.jpg")
        ),
        unsafe_allow_html=True,
    )

    # GitHub and LinkedIn icons with links
    st.write(
        "A LLM powered web app to have a direct chat/discussion with your PDFs."
    )

    # Description of the web app
    st.write(
        "DocConvo is a revolutionary web app that allows users to engage in direct conversations with their PDFs. Powered by Language Models (LLM), vector search, and embeddings, DocConvo brings a new level of interaction to your documents. Please note that conversations are limited to PDFs."
    )
    
    # File convertor
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt", accept_multiple_files=False)
    convert_button = st.button("Convert to PDF")

    if uploaded_file is not None and convert_button:
        txt_contents = uploaded_file.read().decode("utf-8")
        pdf = txt_to_pdf(txt_contents)

        # Get the name of the uploaded file
        file_name = os.path.splitext(uploaded_file.name)[0]

        # Save PDF to a BytesIO buffer
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        st.write("Download your converted PDF file 👇", )
        st.download_button(label="Download PDF", data=pdf_buffer, file_name=f"{file_name}.pdf", mime="application/pdf", key="pdf", help="Right-click and save as...")


    #Sidebar login
    with st.sidebar:

        if not hasattr(st.session_state, 'login_successful'):
            setattr(st.session_state, 'login_successful', False)  # Initialize login status

        st.title("Login Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        def on_login_button_click():
            hashed = hashed_passwords.get(username)
            if hashed and check_password(hashed, password):
                st.success("Login successful")
                st.experimental_set_query_params(path="home")
                setattr(st.session_state, 'login_successful', True)  # Set login status to True
            else:
                st.error("Invalid username or password")

        login_button = st.button("Login", help="Click to login after entering username and password", on_click=on_login_button_click)
        create_account = st.button("Don't have an account?", on_click=lambda: st.experimental_set_query_params(path="signup"),help="Click to create an account")
        # Additional check to redirect to home if login was successful
        if st.session_state.login_successful:
            st.experimental_set_query_params(path="home")
def signup():

    # Subtitle with a stylish underline
    st.markdown(
        """
        <style>
            .title {
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header with title, GitHub, and LinkedIn icons
    st.markdown(
        "<h2 class='title'>Welcome to DocConvo <img src='data:image/jpg;base64,{}' style='margin-left: 10px; width: 30px; height: 30px;'></h2>".format(
            get_base64_of_bin_file("images/doc_convo_icon.jpg")
        ),
        unsafe_allow_html=True,
    )

    st.write(
        "A LLM powered web app to have a direct chat/discussion with your PDFs."
    )

    # Description of the web app
    st.write(
        "DocConvo is a revolutionary web app that allows users to engage in direct conversations with their PDFs. Powered by Language Models (LLM), vector search, and embeddings, DocConvo brings a new level of interaction to your documents. Please note that conversations are limited to PDFs."
    )
    
    # File convertor
    uploaded_file = st.file_uploader("Choose a .txt file", type="txt", accept_multiple_files=False)
    convert_button = st.button("Convert to PDF")

    if uploaded_file is not None and convert_button:
        txt_contents = uploaded_file.read().decode("utf-8")
        pdf = txt_to_pdf(txt_contents)

        # Get the name of the uploaded file
        file_name = os.path.splitext(uploaded_file.name)[0]

        # Save PDF to a BytesIO buffer
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        st.write("Download your converted PDF file 👇", )
        st.download_button(label="Download PDF", data=pdf_buffer, file_name=f"{file_name}.pdf", mime="application/pdf", key="pdf", help="Right-click and save as...")

    #Sidebar signup
    with st.sidebar:
        if not hasattr(st.session_state, 'login_successful'):
            setattr(st.session_state, 'login_successful', False)  # Initialize login status

        st.title("Signup Page")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        signup_button = st.button("Signup", help="Click to signup after entering username and password")
        already_have_account = st.button("Already have an account", on_click=lambda: st.experimental_set_query_params(path="login"),help="Click to login")

        if signup_button:
            if not (username and password and confirm_password):
                st.error("Username, password, and confirm password fields cannot be empty.")
            elif password != confirm_password:
                st.error("Password and Confirm Password do not match.")
            else:
                if username in hashed_passwords:
                    st.warning("Username already exists. Try a different username.")
                else:
                    hashed_passwords[username] = hash_password(password)
                    with open(file_path, "wb") as f:
                        pickle.dump(hashed_passwords, f)
                    st.success("Signup successful. You can now login.")

def handle_logout():
    setattr(st.session_state, 'login_successful', False)  # Set login status to False
    st.experimental_set_query_params(path="login")  # Redirect to login page

def home():
    #Main code
    # Subtitle with a stylish underline
    st.markdown(
            """
            <style>
                .title {
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<h2 class='title'>Welcome to DocConvo <img src='data:image/jpg;base64,{}' style='margin-left: 10px; width: 30px; height: 30px;'></h2>".format(get_base64_of_bin_file("images/doc_convo_icon.jpg")), unsafe_allow_html=True)
    st.write("A LLM powered web app to have a direct chat/discussion with your PDFs.\n ")
        
    # Initialize a list to store the names of uploaded files
    uploaded_files_names = []

    # Sidebar
    with st.sidebar:
        # Upload section with a stylish upload button
        uploaded_files = st.file_uploader("Upload your PDFs and click on Process", type=["pdf"], accept_multiple_files=True)
        
        if uploaded_files:
            st.success("File uploaded successfully!")
            
            # Append the names of uploaded files to the list
            for file in uploaded_files:
                uploaded_files_names.append(file.name)
        
        process_button = st.button("Process")
        if process_button:
            with st.spinner("Processing..."):
                # Function to get vectorization of the uploaded PDFs
                vectorization_status = ingest_docs(uploaded_files)
                if vectorization_status == "Success":
                    st.success("Vectorization successful!")
                    # Display section for uploaded file names
                    st.header("Your files")
                    for file_name in uploaded_files_names:
                        st.write(file_name)
                else:
                    st.error("Vectorization failed!")
        
        st.write("\n")
        st.write("\n")

        st.session_state.login_successful = True
        # Logout button
        if st.session_state.login_successful:
            logout_button = st.button("Logout", on_click=handle_logout)

    if "user_prompt_history" not in st.session_state:
        st.session_state["user_prompt_history"] = []
    if "chat_answers_history" not in st.session_state:
        st.session_state["chat_answers_history"] = []

    prompt = st.text_input("Your questions", placeholder="Enter your questions here..")

    if prompt:
        with st.spinner("Generating response.."):
            chat_history = st.session_state.get("chat_history", [])

            generated_response = run_llm(query=prompt, chat_history=chat_history)
            formatted_response = f"{generated_response['answer']} \n\n "
            st.session_state["user_prompt_history"].append(prompt)
            st.session_state["chat_answers_history"].append(formatted_response)
            st.session_state["chat_history"] = chat_history + [(prompt, generated_response["answer"])]


    if st.session_state["chat_answers_history"]:
        for i, (generated_response, user_query) in enumerate(zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
        )):
            user_key = f"my_unique_key_{i}"
            message(user_query, is_user=True, key=user_key)
            message(generated_response, is_user=False, key=f"generated_response_{i}")

    
path = st.experimental_get_query_params().get("path", ["login"])[0]
def main():
    # Page configuration
    st.set_page_config(
        page_title="DocConvo",
        page_icon=get_base64_of_bin_file("images/doc_convo_icon.jpg"),
        layout="wide",
    )
    if path == "login":
        login()
    elif path == "home":
        home()
    elif path == "signup":
        signup()
    else:
        st.error("Unrecognized path")
        st.stop()   


if __name__ == "__main__":
    main()
