import streamlit as st
import requests
import os
import pypdfium2 as pdfium

# 設定FastAPI後端的URL
API_URL = "http://localhost:8000"

# 模擬使用者登入 (這裡可以替換成實際的認證方式)
if 'user' not in st.session_state:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # 在此處可以與FastAPI後端進行認證請求
        st.session_state.user = username
else:
    st.title(f"Welcome, {st.session_state.user}!")
    
    # PDF上傳功能
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file and st.button("Upload"):
        # 將PDF上傳至後端FastAPI並儲存
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/upload_pdf", files=files, data={"username": st.session_state.user})
        
        if response.status_code == 200:
            st.success("File uploaded successfully!")
        else:
            st.error(f"Failed to upload file: {response.status_code}  - {response.text}")
    
    # 從FastAPI取得上傳過的PDF檔案列表

    st.markdown("---")

    @st.cache_data
    def fetch_pdf_files(username):
        response = requests.get(f"{API_URL}/list_files", params={"username": username})
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to retrieve file list.")
            return []

    @st.cache_resource
    def load_pdf(file_name):
        response = requests.get(f"{API_URL}/get_pdf", params={"file_name": file_name})
        if response.status_code == 200:
            pdf_data = response.content
            with open("temp.pdf", "wb") as f:
                f.write(pdf_data)

            # 讀取 PDF 文件
            pdf = pdfium.PdfDocument("temp.pdf")
            return pdf
        else:
            st.error(f"Failed to load PDF. {response.status_code}")
            return None

    st.markdown("### PDF List")

    # 獲取 PDF 文件列表
    files_list = fetch_pdf_files(st.session_state.user)

    if files_list:
        selected_file = st.selectbox("Choose a PDF to view", files_list)

        st.markdown("---")

        if selected_file:
            pdf = load_pdf(selected_file)

            if pdf is not None:
                total_pages = len(pdf)
                st.session_state.current_page = st.session_state.get("current_page", 0)

                # 緩存每一頁的圖像
                if 'pdf_images' not in st.session_state:
                    st.session_state.pdf_images = {}
                    for i in range(total_pages):
                        page = pdf[i]
                        pil_image = page.render(scale=2).to_pil()
                        st.session_state.pdf_images[i] = pil_image

                # 分頁按鈕
                col0,col1, col2,col3 = st.columns([3,2, 2,3])
                with col1:
                    if st.button("往前一頁") and st.session_state.current_page > 0:
                        st.session_state.current_page -= 1

                with col2:
                    if st.button("往後一頁") and st.session_state.current_page < total_pages - 1:
                        st.session_state.current_page += 1
                # 顯示當前頁面
                if 0 <= st.session_state.current_page < total_pages:
                    image_to_show = st.session_state.pdf_images[st.session_state.current_page]
                    st.image(image_to_show, caption=f"Page {st.session_state.current_page + 1} of {total_pages}")


                # 顯示頁碼
                st.write(f"Page {st.session_state.current_page + 1} of {total_pages}")