import streamlit as st
import os
import getpass
import json
import deeplake
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = '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'
os.environ['ACTIVELOOP_TOKEN'] = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NDExNzE4NiwiZXhwIjoxNjg0MjAzNTczfQ.eyJpZCI6Im9vZ2lqbyJ9.5ABc--92iXagDwgXgBzfxROozX4VZiFZh9uB_gYPKarCGpSI93spJ9JQNBW-eoxrnm_-AbOxf-nkytNSsCnglQ'
os.environ['ACTIVELOOP_ORG'] = 'hub://oogijo/dataset_name'

def load_data():
    with open("data/documentation.json") as f:
        json_data = f.read()
    data = json.loads(json_data)
    text = json.dumps(data)
    return text

def initialize_chatbot(dataset_path, embeddings, text):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    pages = text_splitter.split_text(text)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.create_documents(pages)

    db = DeepLake(dataset_path=dataset_path, read_only=True, embedding_function=embeddings)

    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['k'] = 4

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=False)
    return qa

def display_ui():
    st.title('Telnyx AI Chatbot')
    st.write("Hi there! I'm Telnyx AI Chatbot. I'm here to assist you with the guidelines for sending SMS to different countries using Telnyx.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Pros")
        st.write("I'm available 24/7, no need to wait for office hours!")
    with col2:
        st.header("Cons")
        st.write("I'm still learning and evolving, so bear with me as I improve and provide even better assistance!")

def run_chatbot():
    org = os.environ['ACTIVELOOP_ORG']
    embeddings = OpenAIEmbeddings()
    dataset_path = org

    text = load_data()
    qa = initialize_chatbot(dataset_path, embeddings, text)

    query = st.text_input('Enter query:')
    if query:
        ans = qa({"query": query})
        st.write(ans)

def main():
    display_ui()
    run_chatbot()

main()
