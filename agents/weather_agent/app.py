import streamlit as st

from ui.chat import render_chat
from ui.map_view import render_map
from ui.sidebar import render_sidebar


st.set_page_config(
    page_title="AI Weather Assistant",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    html,
    body,
    #root,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .stApp {
        height: 100vh;
        overflow: hidden !important;
        font-family: Inter, "Segoe UI", Arial, sans-serif;
    }
    .block-container {
        height: 100%;
        min-height: 0;
        box-sizing: border-box;
        max-width: 1500px;
        padding-top: 4.25rem;
        padding-bottom: 0.75rem;
        overflow: hidden;
    }
    .block-container > [data-testid="stVerticalBlock"] {
        height: 100%;
        min-height: 0;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: #4A90D9;
        z-index: 9999;
    }
    [data-testid="stChatMessage"] {
        border-radius: 8px;
        padding: 0.35rem 0.5rem;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #EAF4FF;
        margin-left: 12%;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: #FFFFFF;
        border: 1px solid #E6EAF0;
        margin-right: 12%;
    }
    .st-key-workspace {
        height: 100% !important;
        min-height: 0;
        overflow: hidden;
    }
    .st-key-workspace > [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-workspace > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
        height: 100%;
        min-height: 0;
    }
    .st-key-workspace > [data-testid="stLayoutWrapper"] {
        flex: 1 1 0 !important;
        height: 100%;
        min-height: 0;
        overflow: hidden;
    }
    .st-key-workspace [data-testid="stHorizontalBlock"] {
        height: 100%;
        min-height: 0;
        align-items: stretch;
    }
    .st-key-workspace [data-testid="stColumn"] {
        height: 100%;
        min-height: 0;
        overflow: hidden;
    }
    .st-key-chat_panel {
        height: 100% !important;
        min-height: 0;
        overflow: hidden;
    }
    .st-key-chat_panel > [data-testid="stVerticalBlockBorderWrapper"],
    .st-key-chat_panel > [data-testid="stVerticalBlockBorderWrapper"] > [data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 0;
    }
    .st-key-chat_panel > [data-testid="stLayoutWrapper"]:has(.st-key-chat_history) {
        flex: 1 1 0 !important;
        min-height: 0;
        overflow: hidden;
    }
    .st-key-chat_panel > [data-testid="stLayoutWrapper"]:has(.st-key-chat_composer) {
        flex: 0 0 auto !important;
        min-height: 0;
    }
    .st-key-chat_history {
        flex: 1 1 0 !important;
        height: auto !important;
        min-height: 0;
        overflow-y: auto;
        overflow-x: hidden;
        overscroll-behavior: contain;
        scroll-behavior: smooth;
        padding: 0.25rem 0.65rem 0.5rem 0;
        scrollbar-width: thin;
    }
    .st-key-chat_history::after {
        content: "";
        display: block;
        flex: 0 0 5rem;
        width: 100%;
        pointer-events: none;
    }
    .st-key-chat_composer {
        position: relative;
        flex: 0 0 auto !important;
        width: 100%;
        background: var(--background-color, #FFFFFF);
        border-top: 1px solid #E6EAF0;
        padding-top: 0.75rem;
        padding-bottom: 0.25rem;
    }
    .st-key-chat_composer [data-testid="stChatInput"] {
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(31, 45, 61, 0.08);
    }
    .st-key-chat_composer textarea {
        max-height: 6rem !important;
        overflow-y: auto !important;
        resize: none !important;
    }
    .st-key-empty_chat_state {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: #667085;
    }
    .st-key-map_panel {
        position: sticky;
        top: 0;
        height: 100%;
        min-height: 0;
        align-self: flex-start;
        overflow: hidden;
    }
    [data-testid="stSidebar"] {
        height: 100vh;
        overflow: hidden;
    }
    [data-testid="stSidebarContent"] {
        height: 100%;
        overflow-y: auto;
        overscroll-behavior: contain;
    }
    @media (max-width: 900px) {
        html,
        body,
        #root,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .stApp {
            height: auto;
            min-height: 100vh;
            overflow: auto !important;
        }
        .block-container {
            height: auto;
            overflow: visible;
        }
        .st-key-workspace {
            height: auto !important;
            overflow: visible;
        }
        .st-key-chat_panel {
            height: 80vh !important;
            min-height: 0;
            overflow: hidden;
        }
        .st-key-workspace [data-testid="stHorizontalBlock"],
        .st-key-workspace [data-testid="stColumn"] {
            height: auto;
            overflow: visible;
        }
        .st-key-chat_history {
            min-height: 0;
        }
        .st-key-map_panel {
            position: static;
            height: auto;
            overflow: visible;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="workspace", height="stretch", border=False, gap=None):
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        with st.container(
            key="chat_panel", height="stretch", border=False, gap="xsmall"
        ):
            st.subheader("💬 Chat")
            user_id = render_sidebar()
            render_chat(user_id)

    with col2:
        with st.container(key="map_panel", height="stretch", border=False):
            st.subheader("🗺 City Map")
            map_data = st.session_state.get("map_data", {})
            render_map(map_data)
