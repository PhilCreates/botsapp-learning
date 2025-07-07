import streamlit as st

# ───────────────────────────────────
# User login at the top
# ───────────────────────────────────
with st.sidebar:
    st.title("🔐 User Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_btn = st.button("Login", key="login_btn")
    if login_btn:
        if username and password:
            st.session_state["logged_in_user"] = username
            st.success(f"Logged in as {username}")
        else:
            st.error("Please enter both username and password.")

# Optionally, block access to chat if not logged in
if "logged_in_user" not in st.session_state:
    st.stop()

st.set_page_config(page_title="WhatsApp-Style Mobile Chat", layout="wide")

# ───────────────────────────────────
# Session-state initialisation
# ───────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = {
        "Alice":      [{"role": "assistant", "content": "Hello!"}],
        "Work Group": [{"role": "assistant", "content": "Meeting at 2?"}],
        "Project X":  []
    }
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Alice"
if "view" not in st.session_state:
    st.session_state.view = "chat_list"          # or "conversation"

# ───────────────────────────────────
# Helper – switch view
# ───────────────────────────────────
def switch_to_conversation(chat_name: str):
    st.session_state.current_chat = chat_name
    st.session_state.view = "conversation"
    st.rerun()

# ───────────────────────────────────
#  CSS patch  →  FULL left alignment
# ───────────────────────────────────
st.markdown(
    """
    <style>
      /* works for every st.button rendered below */
      div.stButton > button {
          text-align: left !important;        /* left-justify text            */
          display:  flex !important;          /* turn wrapper into flexbox    */
          flex-direction: column !important;  /* stack multiple label lines   */
          align-items: flex-start !important; /* hug the left edge            */
          justify-content: flex-start !important;
          white-space: normal !important;     /* allow Markdown line breaks   */
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ───────────────────────────────────
# Chat-LIST VIEW
# ───────────────────────────────────
if st.session_state.view == "chat_list":
    st.title("💬 Chats")
    for name, msgs in st.session_state.history.items():
        icon    = "👥" if name == "Work Group" else "🙂"
        preview = msgs[-1]["content"] if msgs else "No messages yet"
        label   = f"{icon} **{name}**  \n{preview}"  # two-line Markdown label
        if st.button(label, use_container_width=True, key=f"btn_{name}"):
            switch_to_conversation(name)

# ───────────────────────────────────
# Conversation VIEW
# ───────────────────────────────────
else:
    st.header(f"Chat with {st.session_state.current_chat}")
    if st.button("⬅️ Back to chats", use_container_width=True):
        st.session_state.view = "chat_list"
        st.rerun()

    for msg in st.session_state.history[st.session_state.current_chat]:
        with st.chat_message(
            msg["role"],
            avatar=msg.get("avatar", "🙂" if msg["role"] == "user" else "🤖")
        ):
            st.write(msg["content"])

    def submit_message():
        txt = st.session_state["chat_input"]
        st.session_state.history[st.session_state.current_chat] += [
            {"role": "user",      "content": txt,          "avatar": "🙂"},
            {"role": "assistant", "content": f"Echo: {txt}", "avatar": "🤖"},
        ]

    st.chat_input("Type a message…", key="chat_input", on_submit=submit_message)
