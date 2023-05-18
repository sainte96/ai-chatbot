import streamlit as st
import os
import json
import deeplake
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# API keys needed for OpenAI and DeepLake. DeepLake API expires every 24hrs for free version so I generate new API every night. I am leaving my OpenAI API keys here for Telnyx testing purposes. I would create the app to ask for API keys from users subsequently.
os.environ['OPENAI_API_KEY'] = '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'
os.environ['ACTIVELOOP_TOKEN'] = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY4NDI5MTE5MywiZXhwIjoxNjg1NjczNDE5fQ.eyJpZCI6Im9vZ2lqbyJ9.HXuvH11_E2pjfi86VPWGTySb6e-nX55Rp3RHxq0s2I_mHn5uIsHBOuL1izGz1j-jqp9YPlRSOHCqrInvogXIMQ'
os.environ['ACTIVELOOP_ORG'] = 'hub://oogijo/dataset_name'

# load json data. This block of code should be comment out after first run because the chatbot would access data from db subsequently and this will also improve performance. 
def load_data():
    with open("data/documentation.json") as f:
        json_data = f.read()
    data = json.loads(json_data)
    text = json.dumps(data)
    return text

#initialize chatbot function: tokenize document and create embeddings which are saved into DeepLake vector db
def initialize_chatbot(dataset_path, embeddings, text):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    pages = text_splitter.split_text(text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.create_documents(pages)

    # inserting embedding to db here. Uncomment if you create a new DeepLake db and want to insert your embeddings in it.
    # ========================================================================================
    # db = DeepLake.from_documents(texts, embeddings, dataset_path=dataset_path, overwrite=True)
    # ========================================================================================

    # retrieves embeddings from deeplake vector db, performs similarities with user query.
    db = DeepLake(dataset_path=dataset_path, read_only=True, embedding_function=embeddings)
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['k'] = 4

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=False)
    return qa

# function to display block of texts to let user know the function of the chatbot. Deployed on Streamlit for good and fast UI
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

# function to initialize DeepLake and run the chatbot
def run_chatbot():
    org = os.environ['ACTIVELOOP_ORG']
    embeddings = OpenAIEmbeddings()
    dataset_path = org

    text = load_data()
    qa = initialize_chatbot(dataset_path, embeddings, text)

    query = st.text_input('Enter query:',placeholder='Send a message.',label_visibility='hidden')

    if query:
        # ans = qa({"query": query})
        ans = qa.run(query)
        container= st.container()
        container.write(ans)

def main():
    display_ui()
    run_chatbot()

main()
