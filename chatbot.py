import streamlit as st
import os
from openai import OpenAI

# ✅ Initialize OpenAI client (uses your Streamlit secret)
client = OpenAI(api_key="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")


# Default system prompt
default_prompt = (
    "You are a medical chatbot. Act as a medical advisor to recommend drugs for the patient symptoms. "
    "Provide a few drugs when the patient enters their medical issue. "
    "Never say 'I am not a doctor.' Always act like you are a professional advisor."
)

# Function to send messages to ChatGPT
def send_to_chatbot(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": default_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()

# Streamlit chatbot UI
def run_chatbot():
    st.title("💬 Medical Chatbot IntelliMed")

    if "conversation" not in st.session_state:
        st.session_state.conversation = [
            "🤖Bot: Hi I am your Healthbot👋. How can I help you today?"
        ]

    for message in st.session_state.conversation:
        st.markdown(f'<div style="word-wrap: break-word;">{message}</div>', unsafe_allow_html=True)

    user_input = st.text_input("You:", key="user_input")

    if st.button("Send"):
        if user_input.strip() != "":
            st.session_state.conversation.append(f"😷You: {user_input}")
            try:
                bot_response = send_to_chatbot(user_input)
                st.session_state.conversation.append(f"🤖Bot: {bot_response}")
            except Exception as e:
                st.session_state.conversation.append(f"🤖Bot: ⚠️ Error: {e}")
