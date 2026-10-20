# import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (SystemMessage, AIMessage, HumanMessage)
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()
loader = PyPDFLoader('resume.pdf')
docs = loader.load()
print("Number of documents:", len(docs))
print("Document type:", type(docs[0]))

# api_key = os.getenv("GOOGLE_API_KEY")

st.title("resume-ai")
st.write("Ask Gemini a question.")
llm_messages = [
    SystemMessage(content= "You are a helpful assistant. You have to greet everytime the user with Good Afternoon.")
]

if "messages" not in st.session_state:
    st.session_state.messages = [] 

question = st.chat_input("Ask a question")

if st.button("Clear Chat"):
    st.session_state.messages = []

if question:
    st.session_state.messages.append({
        "role": 'user',
        "content": question
    })

for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.write(item["content"])

for item in st.session_state.messages:
    if item["role"] == "assistant":
            llm_messages.append(
                AIMessage(content= item["content"])
            )
    else:
            llm_messages.append(
                HumanMessage(content=item["content"])
            )

if question:    
    try:
        with st.spinner("Gemini is thinking..."):
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.5-flash-lite",
                # api_key=api_key,
                timeout=30,
                max_retries=1,
            )
            response = llm.invoke(llm_messages)

        # Gemini 3 returns content blocks; .text extracts the readable reply.
        answer = response.text
        if answer:
            with st.chat_message("assistant"):
                st.write(answer)
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
        else:
            st.warning("Gemini returned no text. Try rephrasing your question.")
            st.session_state.messages.pop()
    except Exception as e:
        if (st.session_state.messages and st.session_state.messages[-1]["role"] == "user"):
            st.session_state.messages.pop()
        st.error("Gemini couldn't respond.")
        st.exception(e)

