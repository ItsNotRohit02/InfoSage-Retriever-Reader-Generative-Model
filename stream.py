import streamlit as st
from streamlit_lottie import st_lottie
from scraper import scrap
from retriever_reader import text_uploader, extractive_pipline, generative_pipline
import requests
from pdf_preprocess import pdf_reader
import DatabaseManager
import hashlib

st.set_page_config(page_title="InfoSage", page_icon="🖥️")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


class SessionState:
    def __init__(self):
        self.username = None


def get_session():
    session_state = st.session_state.get('session_state', None)
    if session_state is None:
        session_state = SessionState()
        st.session_state['session_state'] = session_state
    return session_state


def encrypt_password(password):
    salt = b"random_salt"
    hashed_password = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()
    return hashed_password


def login():
    col1, col2 = st.columns([2, 3])
    with col1:
        st.title("Login")
        username = st.text_input("Username")
        username = username.strip()
        if len(username) >= 50:
            st.error("Username cannot be more than 50 characters")
        password = st.text_input("Password", type="password")
        password = encrypt_password(password)
        if st.button("Login"):
            if username and password:
                status = DatabaseManager.checkLogin(username)
                if status == 'UserDoesNotExist':
                    st.error("Username Does Not Exist")
                elif status == 'UserExists':
                    passw = DatabaseManager.checkPassword(username, password)
                    if passw == 'True':
                        session_state = get_session()
                        session_state.username = username
                        st.success("Logged in as: {}".format(session_state.username))
                    else:
                        st.error("Incorrect Password")
            else:
                st.error("Please enter a username and password.")

        if st.button("Create Account"):
            if username and password:
                status = DatabaseManager.checkLogin(username)
                if status == 'UserDoesNotExist':
                    DatabaseManager.addLogin(username, password)
                    st.success('Created Successfully')
                    session_state = get_session()
                    session_state.username = username
                    st.success("Logged in as: {}".format(session_state.username))
                elif status == 'UserExists':
                    st.error("Username Already Exist")
            else:
                st.error("Please enter a username and password.")
    with col2:
        load_icon = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ab0pxvgc.json")
        st_lottie(load_icon, speed=1, reverse=False, loop=True, quality="low")


def main():
    session_state = get_session()
    if session_state.username is not None:
        st.title("Question and Answering Model")
        st.subheader("Retriever-Reader Model")
        cols1, cols2 = st.columns([2, 1])

        # Form for Login
        with cols1:
            with st.form(key="form1"):
                model_type = st.radio(
                    "How would you prefer the answer to be in?", ("Generative", "Reader")
                )

                URL = st.text_input("URL")
                file = st.file_uploader(label="Please upload your file", type=["doc", "pdf"])
                if file is not None:
                    with open("my_file.pdf", "wb") as f:
                        f.write(file.read())
                submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                st.success(f"Submitted successfully {URL}")
            if URL:
                if model_type == "Reader":
                    df = scrap(URL, 50)
                    pipe = text_uploader(df)

                elif model_type == "Generative":
                    df = scrap(URL, 1000)
                    pipe = text_uploader(df)

            if file:
                if model_type == "Reader":
                    df = pdf_reader("C:\QA_model\my_file.pdf", 50)
                    pipe = text_uploader(df)

                elif model_type == "Generative":
                    df = pdf_reader("C:\QA_model\my_file.pdf", 1000)
                    pipe = text_uploader(df)

        with cols2:
            lottie_url_home = "https://assets7.lottiefiles.com/packages/lf20_pJvtiSVyYH.json"
            lottie_home = load_lottieurl(lottie_url_home)
            st_lottie(lottie_home, key="welcome")

        if model_type == "Reader":
            colr1, colr2 = st.columns([1, 2])
            with st.form(key="form2"):
                with colr2:
                    st.subheader("Enter your Question")
                    QUERY = st.text_input(
                        "Make sure the Question is appropriate and relevant to the Document"
                    )
                with colr1:
                    lottie_url_question = (
                        "https://assets7.lottiefiles.com/packages/lf20_vjxfqggs.json"
                    )
                    lottie_question = load_lottieurl(lottie_url_question)
                    st_lottie(lottie_question, key="question")

                st.subheader("Set appropriate hyperparameters")
                col1, col2 = st.columns(2)
                RETRIVAL_PARAM = col1.slider(
                    label="Number of retrieved documents", min_value=0, max_value=10
                )
                READER_PARAM = col2.slider(
                    label="Number of answers to be generated", min_value=0, max_value=10
                )
                submit_button_2 = st.form_submit_button(label="Submit")

            if submit_button_2:
                pipe = extractive_pipline()
                preds = pipe.run(
                    query=QUERY,
                    params={
                        "Retriever": {"top_k": RETRIVAL_PARAM},
                        "Reader": {"top_k": READER_PARAM},
                    },
                )
                st.subheader("Extractive Answer")
                for idx in range(READER_PARAM):
                    st.text(preds["answers"][idx].answer)


        elif model_type == "Generative":
            colr1, colr2 = st.columns([1, 2])
            with st.form(key="form2"):
                with colr2:
                    st.subheader("Enter your Question")
                    QUERY = st.text_input(
                        "Make sure the Question is appropriate and relevant to the Document"
                    )
                with colr1:
                    lottie_url_question = (
                        "https://assets7.lottiefiles.com/packages/lf20_vjxfqggs.json"
                    )
                    lottie_question = load_lottieurl(lottie_url_question)
                    st_lottie(lottie_question, key="question")
                st.subheader("Appropriate Hyperparameter are set for Generative model ")

                submit_button_2 = st.form_submit_button(label="Submit")

            if submit_button_2:
                pipe = generative_pipline()
                output = pipe.run(query=QUERY, params={"retriever": {"top_k": 2}})
                st.subheader("Generative Answer")
                st.write(output["results"][0])

        st.subheader("Give Feedback")
        with st.form(key="form3"):
            col1, col2 = st.columns([2, 1])
            with col1:
                score = st.number_input("Please rate the response on a scale of 0-10", min_value=0, max_value=10)
                query = str(QUERY)
                submit_button_3 = st.form_submit_button(label="Submit Feedback")
                if submit_button_3:
                    DatabaseManager.addPrompt(session_state.username, query, score)
    else:
        login()


if __name__ == "__main__":
    main()
