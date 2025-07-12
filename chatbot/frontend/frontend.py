import streamlit as st
import requests

st.title("TokoSawit Chatbot")
user_input = st.text_input("Ask a question about a product:")

if st.button("Submit"):
    res = requests.post("http://localhost:8000/api/v1/messaging/chatbot", json={"question": user_input})
    st.subheader("Answer:")
    st.write(res.json()["answer"])