import streamlit as st

from persistence import database


def _activate_user(user_id: str, last_city: str) -> None:
    if st.session_state.get("active_user_id") == user_id:
        return

    st.session_state["active_user_id"] = user_id
    st.session_state["messages"] = []
    st.session_state["history_loaded_for"] = None
    st.session_state["last_city"] = last_city
    st.session_state["map_data"] = {}
    st.session_state["prefill"] = ""


def _reset_visible_chat(user_id: str, reload_history: bool) -> None:
    st.session_state["messages"] = []
    st.session_state["history_loaded_for"] = None if reload_history else user_id
    st.session_state["map_data"] = {}
    st.session_state["prefill"] = ""


def render_sidebar() -> str:
    with st.sidebar:
        st.title("Weather Assistant")
        st.divider()

        st.subheader("User")
        entered_user_id = st.text_input(
            "User ID",
            value="default_user",
            key="user_id_input",
        )
        user_id = entered_user_id.strip() or "default_user"
        st.caption("Your ID keeps preferences and history separate.")

        prefs = database.get_preference(user_id)
        _activate_user(user_id, prefs.get("last_city", ""))

        st.subheader("Preferences")
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Favourite city")
            st.markdown(f"**{prefs.get('favorite_city') or 'Not set'}**")
        with col2:
            st.caption("Last city")
            st.markdown(f"**{prefs.get('last_city') or 'None'}**")

        st.subheader("Quick Actions")
        last_city = prefs.get("last_city") or "your city"
        if st.button("Current weather", use_container_width=True):
            st.session_state["prefill"] = f"What is the weather in {last_city}?"
        if st.button("7-day forecast", use_container_width=True):
            st.session_state["prefill"] = f"What is the forecast for {last_city}?"
        if st.button("Air quality", use_container_width=True):
            st.session_state["prefill"] = f"What is the AQI in {last_city}?"

        st.subheader("Conversation")
        stats = database.get_session_stats(user_id)
        st.caption(f"Messages this session: {stats.get('message_count', 0)}")

        if st.button("New chat", use_container_width=True):
            database.start_new_session(user_id)
            _reset_visible_chat(user_id, reload_history=False)
            st.rerun()

        if st.button("Clear history", use_container_width=True):
            database.clear_conversation(user_id)
            _reset_visible_chat(user_id, reload_history=False)
            st.rerun()

        st.divider()
        st.caption("Powered by Groq + LangGraph")

    return user_id
