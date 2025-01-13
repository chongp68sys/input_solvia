def display_conversations(agent_id):
    """Displays the conversations with summary and detail view."""
    initialize_session_state()
    
    # Initialize visibility toggle in session state
    if 'show_conversations' not in st.session_state:
        st.session_state.show_conversations = True

    # Add button to toggle visibility
    if st.button("Hide Conversations" if st.session_state.show_conversations else "Show Conversations"):
        st.session_state.show_conversations = not st.session_state.show_conversations

    # Auto-refresh every 30 seconds
    refreshed = st_autorefresh(interval=30000, key="conversation_refresh")

    # Fetch Conversations Button
    if st.button("Fetch Conversations", key="fetch_conversations_button"):
        data = fetch_conversations(agent_id)
        if data and "conversations" in data:
            fetched_conversations = data["conversations"]
            if not fetched_conversations:
                st.warning("No conversations returned.")
            else:
                append_new_conversations(fetched_conversations)
        else:
            st.warning("No conversations found or unable to retrieve data.")

    # Auto-refresh fetch
    if refreshed:
        data = fetch_conversations(agent_id)
        if data and "conversations" in data:
            fetched_conversations = data["conversations"]
            if fetched_conversations:
                append_new_conversations(fetched_conversations)

    # Display Conversations based on visibility toggle
    if st.session_state.show_conversations:
        if st.session_state.conversations:
            st.subheader("Conversations")
            for i, convo in enumerate(st.session_state.conversations, start=1):
                conversation_id = convo.get("conversation_id", "N/A")
                agent_name = convo.get("agent_name", "N/A")
                call_duration_secs = convo.get("call_duration_secs", "N/A")
                message_count = convo.get("message_count", "N/A")
                call_successful = convo.get("call_successful", "N/A")

                st.write(
                    f"**No.{i} — Agent: {agent_name}**\n"
                    f"- **Conversation ID:** {conversation_id}\n"
                    f"- **Duration:** {call_duration_secs} seconds\n"
                    f"- **Messages:** {message_count}\n"
                    f"- **Successful:** {'Yes' if call_successful else 'No'}"
                )

                with st.expander("View Details", expanded=False):
                    details = fetch_conversation_details(conversation_id)
                    if details:
                        st.json(details)
                    else:
                        st.write("No additional details available for this conversation.")
        else:
            st.info("No conversations to display. Click 'Fetch Conversations' to load.")
    else:
        st.info("Conversations are currently hidden. Click 'Show Conversations' to view.")
