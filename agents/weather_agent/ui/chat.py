import streamlit as st

from graph.workflow import app
from persistence import database


def _enable_history_autoscroll() -> None:
    st.iframe(
        """
        <script>
        (() => {
            const scrollToLatest = () => {
                const history = window.parent.document.querySelector(
                    ".st-key-chat_history"
                );
                if (history) history.scrollTop = history.scrollHeight;
            };

            requestAnimationFrame(scrollToLatest);
            [80, 250, 600, 1200, 2500].forEach((delay) => {
                setTimeout(scrollToLatest, delay);
            });

            setTimeout(() => {
                const history = window.parent.document.querySelector(
                    ".st-key-chat_history"
                );
                if (!history) return;
                const observer = new MutationObserver(scrollToLatest);
                observer.observe(history, {
                    childList: true,
                    subtree: true,
                    characterData: true
                });
                setTimeout(() => observer.disconnect(), 3000);
            }, 100);
        })();
        </script>
        """,
        height=1,
        tab_index=-1,
    )


def _initial_state(user_input: str, user_id: str) -> dict:
    return {
        "user_query": user_input,
        "user_id": user_id,
        "intent": "",
        "city": "",
        "required_nodes": [],
        "location_data": {},
        "weather_data": {},
        "forecast_data": {},
        "aqi_data": {},
        "environmental_alerts": [],
        "messages": [],
        "previous_city": st.session_state.get("last_city", ""),
        "reasoning_trace": [],
        "final_response": "",
        "memory_context": {},
        "conversation_context": [],
        "map_data": {},
    }


def render_chat(user_id: str) -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("prefill", "")
    st.session_state.setdefault("last_city", "")
    st.session_state.setdefault("map_data", {})
    st.session_state.setdefault("history_loaded_for", None)

    if st.session_state["history_loaded_for"] != user_id:
        st.session_state["messages"] = []
        recent = database.get_recent_messages(user_id, limit=6)
        for msg in recent:
            st.session_state["messages"].append(
                {"role": msg["role"], "content": msg["content"]}
            )
        st.session_state["history_loaded_for"] = user_id

    with st.container(
        key="chat_history",
        height="stretch",
        border=False,
    ):
        if not st.session_state["messages"]:
            with st.container(key="empty_chat_state"):
                st.markdown("#### What would you like to know?")
                st.caption("Ask about a city or use a quick action from the sidebar.")

        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and msg.get("meta"):
                    st.caption(
                        f"Intent: {msg['meta'].get('intent', '')} | "
                        f"City: {msg['meta'].get('city', '')}"
                    )

        activity_slot = st.empty()
        _enable_history_autoscroll()

    with st.container(key="chat_composer"):
        user_input = st.session_state.pop("prefill", "") or st.chat_input(
            "Ask about weather anywhere...",
            key="weather_chat_input",
        )

    if user_input:
        user_msg = {"role": "user", "content": user_input}
        st.session_state["messages"].append(user_msg)

        # Keep transient activity inside the scrollable history, above composer.
        with activity_slot.container():
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = app.invoke(_initial_state(user_input, user_id))

        st.session_state["last_city"] = result.get("city", "")
        st.session_state["map_data"] = result.get("map_data", {})
        assistant_msg = {
            "role": "assistant",
            "content": result["final_response"],
            "meta": {
                "intent": result.get("intent", ""),
                "city": result.get("city", ""),
            },
        }
        st.session_state["messages"].append(assistant_msg)

        st.rerun()
