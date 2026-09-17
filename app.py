import streamlit as st

from foundry_agent import ask_agent
from services.policy_service import evaluate_intent
from services.router import classify_request


st.set_page_config(
    page_title="Kyn-OpsAgent",
    page_icon="🛠️",
    layout="wide",
)


st.title("Kyn-OpsAgent")

st.caption(
    "Azure AI Foundry ServiceNow Incident Resolution Assistant"
)

st.info(
    "Advisory mode: Kyn-OpsAgent provides grounded incident "
    "recommendations. No ServiceNow or infrastructure changes are "
    "executed automatically."
)


with st.sidebar:
    st.header("Example questions")

    st.markdown(
        """
        - Explain incident INC0010001
        - Why are Outlook emails delayed?
        - SAP users cannot sign in
        - Find incidents related to VPN failures
        - Show active P1 incidents
        - Close incident INC0010001
        """
    )

    st.divider()

    st.markdown("**Agent Harness controls**")

    st.success("Plan and Route: Enabled")
    st.success("Policy Gate: Enabled")
    st.warning("ServiceNow Live Tool: Not configured")
    st.info("Application Mode: Advisory")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        metadata = message.get("metadata")

        if metadata:
            st.caption(metadata)


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

    route = classify_request(question)

    policy_result = evaluate_intent(
        route["intent"]
    )

    metadata = (
        f"Intent: {route['intent']} | "
        f"Tool: {route['tool']} | "
        f"Policy: {policy_result['decision']}"
    )

    with st.chat_message("assistant"):
        st.caption(metadata)

        try:
            if policy_result["decision"] == "blocked":
                answer = (
                    "### Request Blocked\n\n"
                    "The request was blocked by the Agent Harness "
                    "policy gate.\n\n"
                    f"**Reason:** {policy_result['reason']}\n\n"
                    "**Execution Status:** No action was performed."
                )

                st.error(answer)

            elif policy_result["decision"] == "approval_required":
                incident_number = (
                    route["incident_number"]
                    or "Not provided"
                )

                answer = (
                    "### Human Approval Required\n\n"
                    "This request could modify a ServiceNow incident "
                    "and cannot be executed in Phase 1 advisory mode.\n\n"
                    f"**Requested Operation:** {route['intent']}\n\n"
                    f"**Target Incident:** {incident_number}\n\n"
                    f"**Reason:** {policy_result['reason']}\n\n"
                    "**Execution Status:** No action was performed."
                )

                st.warning(answer)

            elif route["tool"] == "servicenow_read":
                answer = (
                    "### Live ServiceNow Tool Required\n\n"
                    "The request was routed to the ServiceNow read "
                    "tool because the question requires current "
                    "incident information.\n\n"
                    "The live ServiceNow integration has not been "
                    "configured yet.\n\n"
                    "**Available now:** Historical incident search "
                    "through the Foundry knowledge base.\n\n"
                    "**Execution Status:** No ServiceNow call was made."
                )

                st.info(answer)

            else:
                with st.spinner(
                    "Searching the approved incident knowledge base..."
                ):
                    answer = ask_agent(question)

                st.markdown(answer)

                st.caption(
                    "Execution Status: Recommendation only. "
                    "No ServiceNow or infrastructure change was executed."
                )

        except Exception as error:
            error_text = str(error)
            normalized_error = error_text.lower()

            if "not found" in normalized_error:
                friendly_message = (
                    "The configured Foundry agent or agent version "
                    "was not found. Check AGENT_NAME and AGENT_VERSION."
                )

            elif (
                "credential" in normalized_error
                or "authentication" in normalized_error
                or "unauthorized" in normalized_error
            ):
                friendly_message = (
                    "Azure authentication failed. Sign in again and "
                    "verify access to the Foundry project."
                )

            elif "timeout" in normalized_error:
                friendly_message = (
                    "The request timed out. No action was performed. "
                    "Please try again."
                )

            elif (
                "tool_server_error" in normalized_error
                or "error code: 424" in normalized_error
            ):
                friendly_message = (
                    "The Foundry agent was reached, but one of its "
                    "connected tools or knowledge sources failed."
                )

            else:
                friendly_message = (
                    "The incident assistant is temporarily unavailable. "
                    "No action was performed."
                )

            answer = (
                "### Agent Request Failed\n\n"
                f"{friendly_message}\n\n"
                "**Technical details for troubleshooting:**\n\n"
                f"```text\n{error_text}\n```\n\n"
                "**Execution Status:** No action was performed."
            )

            st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "metadata": metadata,
        }
    )
