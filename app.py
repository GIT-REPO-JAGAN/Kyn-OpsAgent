import streamlit as st

from foundry_agent import ask_agent


st.set_page_config(
    page_title="Kyn-OpsAgent",
    page_icon="🛠️",
    layout="wide",
)


st.title("Kyn-OpsAgent")
st.caption(
    "Azure AI Foundry ServiceNow Incident Resolution Assistant"
)


with st.sidebar:
    st.header("Example questions")

    st.markdown(
        """
        - Explain incident INC0010001
        - Why are Outlook emails delayed?
        - SAP users cannot sign in
        - Server disk space is critically low
        - Find incidents related to VPN failures
        """
    )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask about a ServiceNow incident"
)


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Searching the incident knowledge base..."
        ):
            try:
                answer = ask_agent(question)
                st.markdown(answer)

            except Exception as error:
                answer = (
                    "Unable to call the Azure AI Foundry agent.\n\n"
                    f"Error: `{error}`\n\n"
                    "Check your Azure login, project permissions, "
                    "agent name, agent version, and project endpoint."
                )

                st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
