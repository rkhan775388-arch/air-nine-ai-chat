
import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="Air Nine AI",
    page_icon="💠",
    layout="centered",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f, #142b50);
    color: white;
}
.stChatMessage {
    background: #152641;
    border: 1px solid #294365;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("💠 Air Nine AI")
st.caption("Your AI workspace · Powered by Gemini")

api_key = os.getenv("GEMINI_API_KEY", "")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

if not api_key:
    st.warning(
        "Gemini API key is not configured. "
        "Add it in your app's secure secrets settings."
    )
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ New chat"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Message Air Nine...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Air Nine is thinking..."):
            try:
                history = [
                    {
                        "role": (
                            "user" if item["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": item["content"]}],
                    }
                    for item in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history,
                )

                answer = response.text or (
                    "No text response was returned. Please try again."
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as exc:
                st.error(
                    "AI request failed. Check your API key, "
                    "model access, quota, and internet connection."
                )
                st.caption(f"Error type: {type(exc).__name__}")
