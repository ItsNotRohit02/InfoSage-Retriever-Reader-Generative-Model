import requests
from bs4 import BeautifulSoup
import regex as re
import uuid
import pandas as pd
import streamlit as st


def semmer(ARTICLE, chunk_size):
    max_chunk = chunk_size
    ARTICLE = re.sub(r"\.(?=\s[A-Z])", ".<eos>", ARTICLE)
    ARTICLE = ARTICLE.replace("?", "?<eos>")
    ARTICLE = ARTICLE.replace("!", "!<eos>")
    sentences = ARTICLE.split("<eos>")
    current_chunk = 0
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1:
            if len(chunks[current_chunk]) + len(sentence.split(" ")) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(" "))
            else:
                current_chunk += 1
                chunks.append(sentence.split(" "))
        else:
            print(current_chunk)
            chunks.append(sentence.split(" "))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = " ".join(chunks[chunk_id])

    return chunks


@st.cache_data
def scrap(URL, chunk_size):
    url = URL

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = soup.find_all("p")
    text = [paragraph.text for paragraph in paragraphs]
    words = " ".join(text)
    words = re.sub(r"\n", "", words)
    words = re.sub(r"\[.*?\]", "", words)
    words = re.sub(r"\(|\)", "", words)
    words = re.sub(r"\\\'", "'", words)

    chunked_text = semmer(words, chunk_size)
    diction = {
        "data": chunked_text,
        "id": [str(uuid.uuid1()) for _ in range(len(chunked_text))],
    }
    dfs = pd.DataFrame.from_dict(diction)

    return dfs
