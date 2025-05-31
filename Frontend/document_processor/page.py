import streamlit as st
from document_processor.api import upload_file_to_backend


def render_document_processor_page():
    """Renders the themed document upload page for the assistant."""

    st.title("Upload Your Travel Documents")
    st.markdown(
        "Upload your **travel guide** so the assistant can give smarter, context-aware answers."
    )

    st.image("./Frontend/assets/banner.jpg", use_container_width=True)
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None and st.button("Upload & Process"):
        with st.spinner("Processing your document..."):
            response, status_code = upload_file_to_backend(uploaded_file)
            if status_code == 200:
                st.success("Document processed successfully!")
                st.session_state.session_id = response["session_id"]
                st.json(response)
            else:
                st.error(f"Upload failed: {response.get('error', 'Unknown error')}")
