import requests
import pypdfium2 as pdfium
from models import save_uploaded_file, list_files
import os
import streamlit as st

API_URL = "http://127.0.0.1:8000"  # 根據實際 API 地址調整

def upload_pdf(username, file):
    # 確保存在上傳的目錄
    os.makedirs("uploaded_files", exist_ok=True)
    
    file_location = f"uploaded_files/{file.name}"  # 使用 name 屬性
    with open(file_location, "wb") as f:
        f.write(file.read())
    save_uploaded_file(username, file.name, file_location)  # 使用 name 屬性
    return {"message": "File uploaded successfully"}

def get_pdf_files(username):
    response = requests.get(f"{API_URL}/list_files", params={"username": username})
    if response.status_code == 200:
        return response.json()
    return []
@st.cache_resource
def load_pdf(file_name):
    response = requests.get(f"{API_URL}/get_pdf", params={"file_name": file_name})
    if response.status_code == 200:
        pdf_data = response.content
        with open("temp.pdf", "wb") as f:
            f.write(pdf_data)
        pdf = pdfium.PdfDocument("temp.pdf")
        return pdf
    return None
