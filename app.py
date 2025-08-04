import streamlit as st
from login import Login
from model import USERS
from rag_pipeline import get_retriever_for_user, get_chat_chain

st.set_page_config(page_title="FinChat", layout="wide")
st.title("FinChat - Balance Sheet Assistant")

# --- Login ---
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    username = st.text_input("Username", key="login_username")
    if st.button("Login"):
        user = Login().login(username)
        if user:
            st.session_state.user = user
        else:
            st.error("Invalid username")
    st.stop()

st.success(f"Logged in as {st.session_state.user['role']}")

# --- Load RAG pipeline ---
retriever = get_retriever_for_user(st.session_state.user)
qa_chain = get_chat_chain(retriever)

# --- Chat Input ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input("Ask something about the company’s performance...")

if query:
    st.session_state.chat_history.append(("user", query))
    with st.spinner("Thinking..."):
        response = qa_chain.invoke({"query": query})
        st.session_state.chat_history.append(("bot", response["result"]))

# --- Chat Display ---
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)
