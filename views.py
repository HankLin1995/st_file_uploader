import streamlit as st
from controllers import upload_pdf, get_pdf_files, load_pdf

def display_pdf_upload(username):
    st.title("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file and st.button("Upload"):
        message = upload_pdf(username, uploaded_file)
        st.success(message["message"])

def display_pdf_viewer(username):
    # st.markdown("### PDF List")
    files_list = get_pdf_files(username)

    if files_list:
        selected_file = st.sidebar.selectbox("Choose a PDF to view", files_list)

        if selected_file:

            pdf = load_pdf(selected_file)
            if pdf is not None:
                total_pages = len(pdf)
                st.session_state.current_page = st.session_state.get("current_page", 0)
                # 頁面圖像緩存
                st.session_state.pdf_images = {}
                
                for i in range(total_pages):
                    page = pdf[i]
                    pil_image = page.render(scale=2).to_pil()
                    st.session_state.pdf_images[i] = pil_image

                # 分頁按鈕
                with st.sidebar:

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("往前一頁") and st.session_state.current_page > 0:
                            st.session_state.current_page -= 1
                            # st.rerun()  # 強制重新渲染

                    with col2:
                        if st.button("往後一頁") and st.session_state.current_page < total_pages - 1:
                            st.session_state.current_page += 1


                # 顯示當前頁面
                if 0 <= st.session_state.current_page < total_pages:
                    image_to_show = st.session_state.pdf_images[st.session_state.current_page]
                    with st.container(border=True):
                        st.image(image_to_show, caption=f"Page {st.session_state.current_page + 1} of {total_pages}")

