import streamlit as st
import requests
import os


def render_chat_page():
    """Renders the Streamlit chat interface and handles user interaction with the assistant."""

    st.title("Chat With Your Travel Assistant")

    # Ensure user uploaded a document
    if "session_id" not in st.session_state:
        st.warning("Please upload a document first using the Document Processor page.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat input field
    user_input = st.chat_input("Say something...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(
            ("assistant", "...")
        )  # Placeholder while loading

        with st.spinner("Thinking..."):
            res = requests.post(
                f"{os.getenv('API_URL')}/chat",
                json={"session_id": st.session_state.session_id, "query": user_input},
            )

            if res.status_code == 200:
                data = res.json()
                response = data["response"]
                retrieved = data["state"].get("documents", "")

                # Replace assistant placeholder with actual response
                st.session_state.chat_history[-1] = ("assistant", response)

                if retrieved:
                    retrieved = (
                        f"Locaction: {data['state'].get('location', '')}\nWeather: {data['state'].get('weather_category', '')}\n"
                        + retrieved
                    )
                    st.session_state.chat_history.append(("retrieved", retrieved))
            else:
                error = res.json().get("error", "Unknown error")
                st.session_state.chat_history[-1] = ("assistant", f"Error: {error}")

    # Display chat history
    for role, content in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(content)
        elif role == "retrieved":
            with st.expander("🔍 Retrieved Document"):
                st.markdown(content.replace("\n", "  \n"))
