"""
app.py
------
Streamlit front-end for "Masha".

M3: chat interface with conversation history.
M4: quick-reply buttons shown when the bot doesn't understand a message,
    so the user always has an easy way to continue the conversation.
"""

import streamlit as st
from chatbot import get_response, QUICK_REPLIES

st.set_page_config(
    page_title="Masha",
    page_icon="🤖",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Dynamic Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #0f2027);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    /* Hide top header and menu */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Glassmorphism Chat messages */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Premium Chat Input */
    [data-testid="stChatInput"] {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Quick reply buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 25px !important;
        color: #fff !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        padding: 0.6rem 1.2rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        border-color: transparent !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
    }
    
    /* Title glowing effect */
    h1 {
        text-align: center;
        text-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
        margin-bottom: 2rem !important;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Masha")
st.caption(
    "A rule-based customer support chatbot. Ask about orders, returns, "
    "product info, or store hours."
)

# --- Conversation state -------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm Masha 👋 How can I help you today?",
        }
    ]
if "last_intent" not in st.session_state:
    st.session_state.last_intent = None


def send_message(text: str) -> None:
    """
    Process one user message: log it, get the bot's reply, log that too.
    Shared by both the chat input box and the quick-reply buttons so their
    behavior never diverges.
    """
    st.session_state.messages.append({"role": "user", "content": text})
    result = get_response(text)
    st.session_state.messages.append({"role": "assistant", "content": result["reply"]})
    st.session_state.last_intent = result["intent"]


# --- Render chat history --------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Quick-reply buttons (shown only after a fallback) -----------------
if st.session_state.last_intent == "fallback":
    st.caption("Or try one of these:")
    cols = st.columns(len(QUICK_REPLIES))
    for i, option in enumerate(QUICK_REPLIES):
        # Key includes message count so each render cycle gets fresh,
        # non-colliding widget keys.
        button_key = f"qr_{len(st.session_state.messages)}_{i}"
        if cols[i].button(option, key=button_key, use_container_width=True):
            send_message(option)
            st.rerun()

# --- Handle typed input -------------------------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    send_message(user_input)
    st.rerun()

# --- Footer -----------------------------------------------------------
st.divider()
st.caption("Built with Python & Streamlit · Pinnacle Labs Internship Program 2026")
