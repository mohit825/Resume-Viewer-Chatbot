# import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")

st.title("resume-ai")
st.write("Ask Gemini a question.")

question = st.chat_input("Ask a question")

# if not api_key:
#     st.error("Add GOOGLE_API_KEY to your .env file, then restart Streamlit.")
#     st.stop()

if question:
    st.write("User:", question)

    try:
        with st.spinner("Gemini is thinking..."):
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.5-flash-lite",
                # api_key=api_key,
                timeout=30,
                max_retries=1,  # One attempt, without automatic retries.
            )
            response = llm.invoke(question)

        # Gemini 3 returns content blocks; .text extracts the readable reply.
        answer = response.text
        if answer:
            st.write("Gemini:", answer)
        else:
            st.warning("Gemini returned no text. Try rephrasing your question.")
    except Exception:
        st.error(
            "Gemini couldn't respond. Check your internet connection, API key, "
            "model access, and API quota, then try again."
        )
