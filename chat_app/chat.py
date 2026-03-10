import streamlit as st
import requests
import json

st.set_page_config(page_title="💬 AI Chatbot", page_icon="🤖")

# --- Chatbot logo ---
st.image("https://img.icons8.com/color/96/000000/robot-2.png", width=60)
#st.image("https://img.icons8.com/color/96/000000/home.png", width=60)

st.title("💬 Chatbot")

API_KEY = st.secrets["OPENROUTER_API_KEY"]
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
model = "gpt-4o-mini"

# --- Conversation session ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Function to send message ---
def send_message():
    user_input = st.session_state.user_input
    if not user_input.strip():
        return
    # Append user message
    st.session_state.conversation.append({"role": "user", "content": user_input})
    payload = {"model": model, "messages": st.session_state.conversation}
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
        # Optionally prepend emoji manually for bot
        bot_reply = f"🤖 {bot_reply}"
        st.session_state.conversation.append({"role": "assistant", "content": bot_reply})
    except Exception as e:
        st.error(f"API Error: {e}")
    # Clear input
    st.session_state.user_input = ""

# --- Display chat with enhanced styling ---
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#D0E8FF;
                color:#000000;
                padding:12px 15px;
                border-radius:12px;
                margin:5px 0;
                box-shadow: 1px 2px 5px rgba(0,0,0,0.1);
                max-width:75%;
            ">
                💬 <b>You:</b> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#F0F0F0;
                color:#000000;
                padding:12px 15px;
                border-radius:12px;
                margin:5px 0;
                box-shadow: 1px 2px 5px rgba(0,0,0,0.1);
                max-width:75%;
            ">
                🤖 {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Input box at the bottom ---
st.text_input(
    "Type your message:",
    key="user_input",
    on_change=send_message,
    placeholder="Press Enter to send...")
