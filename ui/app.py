import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Company RAG Assistant", layout="centered")

st.title("🏢 Company Knowledge Assistant")

st.write("Ask questions from company documents")

# User input
email = st.text_input("Company Email")
question = st.text_area("Your Question")

if st.button("Ask"):
    if not email or not question:
        st.warning("Please enter email and question")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                API_URL,
                json={
                    "email": email,
                    "question": question
                }
            )

        if response.status_code == 200:
            data = response.json()
            st.success("Answer")
            st.write(data["answer"])
            st.caption(f"Role: {data['role']}")
        else:
            st.error(response.json().get("detail", "Error occurred"))
