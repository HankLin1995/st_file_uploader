import streamlit as st
from views import display_pdf_upload, display_pdf_viewer

# 假設用戶名已經存儲在 session_state 中
if 'user' not in st.session_state:
    st.session_state.user = "your_username"  # 假設用戶名是在這裡設定

st.sidebar.title("Menu")
menu_option = st.sidebar.selectbox("Select an option", ["Upload PDF", "View PDFs"])

if menu_option == "Upload PDF":
    display_pdf_upload(st.session_state.user)
elif menu_option == "View PDFs":
    display_pdf_viewer(st.session_state.user)
