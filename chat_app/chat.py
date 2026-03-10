import streamlit as st
import requests
import json

#Page config
st.set_page_config(page_title="💬 Alae Bot", page_icon="🤖")

st.markdown("""
<style>
div.stButton > button {
    width: 130%;
    height: 50px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

#Header
col1, col2 = st.columns([5,1])
with col1:
    st.image("https://img.icons8.com/color/96/000000/robot-2.png", width=60)
    st.title("💬 Alae Bot")

#API
API_KEY = st.secrets["OPENROUTER_API_KEY"]
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"}
model = "gpt-4o-mini"

#prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Alae Bot, an AI assistant created by Alae. "
        "If someone asks who you are, say you are Alae Bot. "
        "Be friendly, concise, and helpful.")}

# conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = [SYSTEM_PROMPT]

#Reset
def reset_conversation():
    st.session_state.conversation = [SYSTEM_PROMPT]

#New chat button
with col2:
    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("🗑️ Delete Chat / New Chat"):
        reset_conversation()
    st.markdown('</div>', unsafe_allow_html=True)

#Send message function
def send_message():
    user_input = st.session_state.user_input
    if not user_input.strip():
        return
    # Add user message
    st.session_state.conversation.append({
        "role": "user",
        "content": user_input})
    payload = {
        "model": model,
        "messages": st.session_state.conversation}
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=30)
        response.raise_for_status()
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
        st.session_state.conversation.append({
            "role": "assistant",
            "content": bot_reply})

    except Exception as e:
        st.error(f"API Error: {e}")

    # clear input
    st.session_state.user_input = ""

#Display conversation
for msg in st.session_state.conversation:
    if msg["role"] == "system":
        continue
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#D0E8FF;
                color:#000;
                padding:12px;
                border-radius:12px;
                margin:8px 0;
                max-width:75%;
                box-shadow:1px 2px 5px rgba(0,0,0,0.1);
            ">
            💬 <b>You:</b> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(
            f"""
            <div style="
                background-color:#F0F0F0;
                color:#000;
                padding:12px;
                border-radius:12px;
                margin:8px 0;
                max-width:75%;
                box-shadow:1px 2px 5px rgba(0,0,0,0.1);
            ">
            🤖 {msg['content']}
            </div>
            """,
            unsafe_allow_html=True)

#Chat input
st.text_input(
    "Type your message",
    key="user_input",
    on_change=send_message,
    placeholder="Ask Alae Bot something and press Enter...")
