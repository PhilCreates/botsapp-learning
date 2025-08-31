
import hashlib
import streamlit as st

st.set_page_config(page_title="WhatsApp-Style Mobile Chat", layout="wide")

# ───────────────────────────────────
# User login at the top
# ───────────────────────────────────
with st.sidebar:
    st.title("🔐 User Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_btn = st.button("Login", key="login_btn")
    # Retrieve valid users from Streamlit secrets
    valid_users = st.secrets.get("users", {})
    if login_btn:
        if username and password:
            if username in valid_users and valid_users[username] == password:
                st.session_state["logged_in_user"] = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please enter both username and password.")

# Optionally, block access to chat if not logged in
if "logged_in_user" not in st.session_state:
    st.stop()

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
    """Switches the view to the selected conversation and reruns the app."""
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
          text-align: left !important;        /* left-justify text */
          display: flex !important;           /* turn wrapper into flexbox */
          flex-direction: column !important;  /* stack multiple label lines */
          align-items: flex-start !important; /* hug the left edge */
          justify-content: flex-start !important;
          white-space: normal !important;     /* allow Markdown line breaks */
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
    GROUP_ICON = "👥"
    USER_ICON = "🙂"
    for name, msgs in st.session_state.history.items():
        # Choose icon based on chat name
        icon = GROUP_ICON if name == "Work Group" else USER_ICON
        # Show last message or placeholder
        preview = msgs[-1]["content"] if msgs else "No messages yet"
        # Markdown label: icon, name, preview
        label = f"{icon} **{name}**  \n{preview}"
        # Safe key for button
        safe_key = f"btn_{hashlib.md5(name.encode()).hexdigest()}"
        if st.button(label, use_container_width=True, key=safe_key):
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
        """Handles user message submission and appends user/assistant messages to chat history."""
        txt = st.session_state["chat_input"]
        st.session_state.history[st.session_state.current_chat] += [
            {
                "role": "user",
                "content": txt,
                "avatar": "🙂"
            },
            {
                "role": "assistant",
                "content": f"Echo: {txt}",
                "avatar": "🤖"
            },
        ]

    st.chat_input(
        "Type a message…",
        key=f"chat_input_{st.session_state.current_chat}",
        on_submit=submit_message
    )
