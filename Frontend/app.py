import streamlit as st
from document_processor.page import render_document_processor_page
from chat.page import render_chat_page
from dotenv import load_dotenv

load_dotenv()


def main():
    """Main entry point for the Streamlit app with sidebar navigation between pages."""

    st.set_page_config(page_title="Document Assistant", layout="centered")

    page = st.sidebar.selectbox("Navigation", ["Document Processor", "Chat"])

    if page == "Document Processor":
        render_document_processor_page()
    elif page == "Chat":
        render_chat_page()


if __name__ == "__main__":
    main()
