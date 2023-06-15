import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from scraper import scrap
from retriever_reader import text_uploader, extractive_pipline, generative_pipline
import time
import requests
import os
from pdf_preprocess import pdf_reader


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.title("Question and Answering Model")
st.subheader("Retriever-reader model")
cols1, cols2 = st.columns([2, 1])


# Form for Login
with cols1:
    with st.form(key="form1"):
        model_type = st.radio(
            "How would you prfer the answer to be in?", ("Generative", "Reader")
        )

        URL = st.text_input("URL")
        file = st.file_uploader(label="Please upload your file", type=["doc", "pdf"])
        if file is not None:
            with open("my_file.pdf", "wb") as f:
        
                    f.write(file.read())
        submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.success(f"Submitted successfully {URL}")
    if URL :
        if model_type == "Reader":
            df = scrap(URL, 50)
            pipe = text_uploader(df)
   
        elif model_type == "Generative":
            df = scrap(URL, 100)
            pipe = text_uploader(df)


    if file:
        if model_type == "Reader":
            df = pdf_reader("C:\QA_model\my_file.pdf", 50)
            pipe = text_uploader(df)

        elif model_type == "Generative":
            df = pdf_reader("C:\QA_model\my_file.pdf", 100)
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
                "Let the Question be appropriate and relavent to the Document"
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
            label="Number of retreived documents", min_value=0, max_value=10
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
                "Let the Question be appropriate and relavent to the Document"
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
        output = pipe.run(
            query=QUERY, params={"retriever": {"top_k": 3}})
        st.subheader("Generative Answer")
        st.text_area(output["results"][0])

