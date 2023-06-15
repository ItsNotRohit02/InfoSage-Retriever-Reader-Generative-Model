from scraper import semmer
import PyPDF2
import re
import uuid
import pandas as pd
import streamlit as st


@st.cache_data
def pdf_reader(file, chunk_size):
    with open(file, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        concatenated_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            text = page_obj.extract_text()
            concatenated_text += text

    text_list = concatenated_text

    cleaned_text = re.sub(r"\n", "", text_list)
    cleaned_text = re.sub(r'[^.,!\w\s]+', "", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text.strip())

    chunked_text = semmer(cleaned_text, chunk_size)
    diction = {
        "data": chunked_text,
        "id": [str(uuid.uuid1()) for _ in range(len(chunked_text))],
    }
    dfs = pd.DataFrame.from_dict(diction)
    return dfs
