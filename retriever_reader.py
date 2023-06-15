#!pip install - -upgrade pip
#!pip install git+https: // github.com/deepset-ai/haystack.git

from haystack.nodes import PromptNode, PromptTemplate
from haystack.pipelines import Pipeline
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader
from haystack.nodes import DensePassageRetriever
from haystack.document_stores import ElasticsearchDocumentStore
import streamlit as st
import os
import sys

document_store = ElasticsearchDocumentStore()
if len(document_store.get_all_documents()) or len(document_store.get_all_labels()) > 0:
    document_store.delete_documents(index="document")
    document_store.delete_documents(index="label")


@st.cache_data
def text_uploader(df):
    docs = [
        {"content": row["data"], "meta": {"item_id": row["id"]}}
        for _, row in df.drop_duplicates(subset="data").iterrows()
    ]
    document_store.write_documents(documents=docs, index="document")

    print(f"Loaded {document_store.get_document_count()} documents")

    dense_retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        embed_title=False,
        use_fast_tokenizers=True,
    )

    document_store.update_embeddings(retriever=dense_retriever)


@st.cache_resource
def extractive_pipline():
    dense_retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        embed_title=False,
        use_fast_tokenizers=True,
    )

    model_ckpt = "deepset/deberta-v3-large-squad2"
    max_seq_length, doc_stride = 384, 128
    reader = FARMReader(
        model_name_or_path=model_ckpt,
        progress_bar=False,
        max_seq_len=max_seq_length,
        doc_stride=doc_stride,
        return_no_answer=True,
    )

    pipe = ExtractiveQAPipeline(reader=reader, retriever=dense_retriever)
    return pipe


@st.cache_resource
def generative_pipline():
    retriever = DensePassageRetriever(
        document_store=document_store,
        query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
        passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
        embed_title=False,
        use_fast_tokenizers=True,
    )

    lfqa_prompt = PromptTemplate(name='lfqa',
        prompt_text="""Synthesize a comprehensive answer from the following text for the given question. 
                             Provide a clear and concise response that summarizes the key points and information presented in the text. 
                             Your answer should be in your own words and match the context with precise numbers and be no longer than 50 words. 
                             \n\n Related text: {join(documents)} \n\n Question: {query} \n\n Answer:""")

    prompt_node = PromptNode(
        model_name_or_path="declare-lab/flan-alpaca-large",
        default_prompt_template=lfqa_prompt,
        max_length=150,
    )

    pipe = Pipeline()
    pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])

    return pipe
