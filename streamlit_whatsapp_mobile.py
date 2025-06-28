import streamlit as st

st.set_page_config(page_title="BotsApp", layout="wide")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = {
        "Alice": [],
        "Work Group": [],
        "Project X": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Alice"

if "view" not in st.session_state:
    st.session_state.view = "chat_list"  # other value: "conversation"

# ----- Chat List View -----
if st.session_state.view == "chat_list":
    st.title("💬 Chats")
    for chat_name in st.session_state.history:
        if st.button(chat_name, use_container_width=True):
            st.session_state.current_chat = chat_name
            st.session_state.view = "conversation"
            st.rerun()

# ----- Conversation View -----
elif st.session_state.view == "conversation":
    st.markdown(f"### 👤 Chat with {st.session_state.current_chat}")
    if st.button("⬅️ Back to chats", use_container_width=True):
        st.session_state.view = "chat_list"
        st.rerun()

    messages = st.session_state.history[st.session_state.current_chat]

    for msg in messages:
        with st.chat_message(msg["role"], avatar=msg.get("avatar", "🙂" if msg["role"] == "user" else "🤖")):
            st.write(msg["content"])

    def submit_message():
        user_input = st.session_state["chat_input"]
        st.session_state.history[st.session_state.current_chat].append({
            "role": "user",
            "content": user_input,
            "avatar": "🙂"
        })
        st.session_state.history[st.session_state.current_chat].append({
            "role": "assistant",
            "content": f"Echo: {user_input}",
            "avatar": "🤖"
        })

    st.chat_input("Type a message...", key="chat_input", on_submit=submit_message)
