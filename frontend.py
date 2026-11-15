# import uuid

# import streamlit as st
# from langchain_core.messages import HumanMessage
# from langgraph.types import Command

# from src.graph.graph import app


# st.set_page_config(page_title="Real-World Multi-Agent Travel Planner", layout="wide")

# st.title("Real-World Multi-Agent Travel Planner")

# with st.sidebar:
#     st.subheader("Session")
#     user_id = st.text_input("User ID", value="demo_user")
#     if "thread_id" not in st.session_state:
#         st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
#     if st.button("New Thread"):
#         st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
#         st.session_state.pop("waiting_for_approval", None)
#         st.session_state.pop("latest_result", None)

#     st.caption(f"Thread: {st.session_state.thread_id}")


# query = st.text_area(
#     "Travel request",
#     placeholder="Plan a 7-day Japan trip under Rs. 2 lakh. I prefer budget hotels and no overnight flights.",
#     height=110,
# )

# config = {"configurable": {"thread_id": st.session_state.thread_id}}


# if st.button("Create Draft Plan", type="primary"):
#     if not query.strip():
#         st.warning("Enter a travel request first.")
#     else:
#         with st.spinner("Agents are planning..."):
#             result = app.invoke(
#                 {
#                     "messages": [HumanMessage(content=query)],
#                     "user_id": user_id,
#                     "user_query": query,
#                     "flight_results": "",
#                     "hotel_results": "",
#                     "weather_results": "",
#                     "budget_results": "",
#                     "itinerary": "",
#                     "final_response": "",
#                     "llm_calls": 0,
#                 },
#                 config=config,
#             )

#         st.session_state.latest_result = result
#         st.session_state.waiting_for_approval = "__interrupt__" in result


# result = st.session_state.get("latest_result")

# if result:
#     st.subheader("Supervisor Plan")
#     st.write(result.get("supervisor_reasoning", ""))
#     st.write("Selected agents:", result.get("selected_agents", []))

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Flight")
#         st.markdown(result.get("flight_results", ""))
#         st.subheader("Weather")
#         st.markdown(result.get("weather_results", ""))
#     with col2:
#         st.subheader("Hotels")
#         st.markdown(result.get("hotel_results", ""))
#         st.subheader("Budget")
#         st.markdown(result.get("budget_results", ""))

#     st.subheader("Draft Itinerary")
#     if "__interrupt__" in result:
#         draft = result["__interrupt__"][0].value.get("draft_itinerary", "")
#     else:
#         draft = result.get("itinerary", "")
#     st.markdown(draft)


# if st.session_state.get("waiting_for_approval"):
#     st.divider()
#     st.subheader("Human Approval")

#     approved = st.radio("Approve this draft?", ["Yes", "No, revise it"], horizontal=True)
#     feedback = st.text_area("Feedback", disabled=approved == "Yes")

#     if st.button("Submit Approval"):
#         with st.spinner("Creating final response..."):
#             final_result = app.invoke(
#                 Command(
#                     resume={
#                         "approved": approved == "Yes",
#                         "feedback": feedback,
#                     }
#                 ),
#                 config=config,
#             )
#         st.session_state.latest_result = final_result
#         st.session_state.waiting_for_approval = False
#         st.rerun()


# final_result = st.session_state.get("latest_result")
# if final_result and final_result.get("final_response"):
#     st.divider()
#     st.subheader("Final Travel Plan")
#     st.markdown(final_result["final_response"])


# import uuid
# import streamlit as st

# from langchain_core.messages import HumanMessage
# from langgraph.types import Command

# from src.graph.graph import app


# # ---------------------------------
# # PAGE CONFIGURATION
# # ---------------------------------

# st.set_page_config(
#     page_title="Real-World Multi-Agent Travel Planner",
#     layout="wide"
# )

# st.title("Real-World Multi-Agent Travel Planner")


# # ---------------------------------
# # SESSION MANAGEMENT
# # ---------------------------------

# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = (
#         f"demo_user_{uuid.uuid4().hex[:8]}"
#     )

# if "latest_result" not in st.session_state:
#     st.session_state.latest_result = None

# if "waiting_for_approval" not in st.session_state:
#     st.session_state.waiting_for_approval = False


# with st.sidebar:

#     st.subheader("Session")

#     user_id = st.text_input(
#         "User ID",
#         value="demo_user"
#     )

#     if st.button("New Thread"):

#         st.session_state.thread_id = (
#             f"{user_id}_{uuid.uuid4().hex[:8]}"
#         )

#         st.session_state.latest_result = None
#         st.session_state.waiting_for_approval = False

#         st.rerun()

#     st.caption(
#         f"Thread: {st.session_state.thread_id}"
#     )


# # ---------------------------------
# # GRAPH CONFIG
# # ---------------------------------

# config = {
#     "configurable": {
#         "thread_id": st.session_state.thread_id
#     }
# }


# # ---------------------------------
# # USER INPUT
# # ---------------------------------

# query = st.text_area(
#     "Travel request",
#     placeholder=(
#         "Plan a 7-day Japan trip under Rs. 2 lakh. "
#         "I prefer budget hotels and no overnight flights."
#     ),
#     height=110
# )


# # ---------------------------------
# # INITIAL STATE
# # ---------------------------------

# initial_state = {
#     "messages": [
#         HumanMessage(content=query)
#     ],

#     "user_id": user_id,
#     "user_query": query,

#     "flight_results": "",
#     "hotel_results": "",
#     "weather_results": "",
#     "budget_results": "",
#     "itinerary": "",
#     "final_response": "",

#     "llm_calls": 0,
# }


# # ---------------------------------
# # CREATE DRAFT WITH STREAMING
# # ---------------------------------

# if st.button("Create Draft Plan", type="primary"):

#     if not query.strip():

#         st.warning("Enter a travel request first.")

#     else:

#         progress = st.status(
#             "AI Agents are working...",
#             expanded=True
#         )

#         try:

#             # Stream graph node updates
#             for chunk in app.stream(
#                 initial_state,
#                 config=config,
#                 stream_mode="updates"
#             ):

#                 for node_name, output in chunk.items():

#                     if node_name == "__interrupt__":
#                         continue

#                     progress.write(
#                         f"Agent completed: {node_name}"
#                     )

#             # Read latest checkpoint state
#             snapshot = app.get_state(config)

#             latest_result = dict(snapshot.values)

#             # Extract human interrupts
#             interrupts = []

#             for task in snapshot.tasks:

#                 interrupts.extend(
#                     getattr(task, "interrupts", ()) or ()
#                 )

#             if interrupts:

#                 latest_result["__interrupt__"] = interrupts

#             st.session_state.latest_result = latest_result

#             st.session_state.waiting_for_approval = bool(
#                 interrupts
#             )

#             progress.update(
#                 label="Draft itinerary generated!",
#                 state="complete"
#             )

#         except Exception as e:

#             progress.update(
#                 label="Planning failed",
#                 state="error"
#             )

#             st.error(f"Error: {e}")


# # ---------------------------------
# # DISPLAY AGENT RESULTS
# # ---------------------------------

# result = st.session_state.latest_result

# if result:

#     st.divider()

#     st.subheader("Supervisor Plan")

#     st.write(
#         result.get("supervisor_reasoning", "")
#     )

#     st.write(
#         "Selected agents:",
#         result.get("selected_agents", [])
#     )

#     col1, col2 = st.columns(2)

#     with col1:

#         st.subheader("Flight")

#         st.markdown(
#             result.get("flight_results", "")
#         )

#         st.subheader("Weather")

#         st.markdown(
#             result.get("weather_results", "")
#         )

#     with col2:

#         st.subheader("Hotels")

#         st.markdown(
#             result.get("hotel_results", "")
#         )

#         st.subheader("Budget")

#         st.markdown(
#             result.get("budget_results", "")
#         )

#     st.subheader("Draft Itinerary")

#     if "__interrupt__" in result:

#         draft = (
#             result["__interrupt__"][0]
#             .value.get("draft_itinerary", "")
#         )

#     else:

#         draft = result.get("itinerary", "")

#     if isinstance(draft, str):
#         st.markdown(draft)
#     else:
#         st.write(draft)


# # ---------------------------------
# # HUMAN APPROVAL
# # ---------------------------------

# if st.session_state.waiting_for_approval:

#     st.divider()

#     st.subheader("Human Approval")

#     approved = st.radio(
#         "Approve this draft?",
#         ["Yes", "No, revise it"],
#         horizontal=True
#     )

#     feedback = st.text_area(
#         "Feedback",
#         disabled=(approved == "Yes")
#     )

#     if st.button("Submit Approval"):

#         progress = st.status(
#             "Generating final travel plan...",
#             expanded=True
#         )

#         try:

#             # Stream final LLM tokens
#             def final_response_stream():

#                 for mode, chunk in app.stream(
#                     Command(
#                         resume={
#                             "approved": approved == "Yes",
#                             "feedback": feedback,
#                         }
#                     ),
#                     config=config,
#                     stream_mode=["messages", "updates"]
#                 ):

#                     if mode == "messages":

#                         message_chunk, metadata = chunk

#                         # Graph node name, not Python function name
#                         if metadata.get("langgraph_node") == "final_response":

#                             content = message_chunk.content

#                             if isinstance(content, str) and content:

#                                 yield content

#             st.subheader("Final Travel Plan")

#             # Display tokens as they arrive
#             streamed_text = st.write_stream(
#                 final_response_stream()
#             )

#             # Get final graph state
#             snapshot = app.get_state(config)

#             final_result = dict(snapshot.values)

#             # Fallback if final_response is missing
#             if not final_result.get("final_response"):

#                 final_result["final_response"] = streamed_text

#             st.session_state.latest_result = final_result

#             st.session_state.waiting_for_approval = False

#             progress.update(
#                 label="Final travel plan completed!",
#                 state="complete"
#             )

#         except Exception as e:

#             progress.update(
#                 label="Final response failed",
#                 state="error"
#             )

#             st.error(f"Error: {e}")


# # ---------------------------------
# # FINAL RESPONSE
# # ---------------------------------

# final_result = st.session_state.latest_result

# if (
#     final_result
#     and final_result.get("final_response")
# ):

#     st.divider()

#     st.subheader("Final Travel Plan")

#     st.markdown(
#         final_result["final_response"]
#     )
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.graph.graph import app


st.set_page_config(
    page_title="Real-World Multi-Agent Travel Planner",
    layout="wide",
)
st.title("Real-World Multi-Agent Travel Planner")


# -----------------------------
# Session and thread management
# -----------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"demo_user_{uuid.uuid4().hex[:8]}"
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False

with st.sidebar:
    st.subheader("Session")
    user_id = st.text_input("User ID", value="demo_user")

    if st.button("New Thread"):
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"
        st.session_state.latest_result = None
        st.session_state.waiting_for_approval = False
        st.rerun()

    st.caption(f"Thread: {st.session_state.thread_id}")

config = {"configurable": {"thread_id": st.session_state.thread_id}}


# -----------------------------
# User travel request
# -----------------------------
query = st.text_area(
    "Travel request",
    placeholder=(
        "Plan a 7-day Japan trip under Rs. 2 lakh. "
        "I prefer budget hotels and no overnight flights."
    ),
    height=110,
)

if st.button("Create Draft Plan", type="primary"):
    if not query.strip():
        st.warning("Enter a travel request first.")
    else:
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "user_id": user_id,
            "user_query": query,
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "budget_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        progress = st.status("Travel agents are working...", expanded=True)
        try:
            for update in app.stream(
                initial_state,
                config=config,
                stream_mode="updates",
            ):
                for node_name in update:
                    if node_name != "__interrupt__":
                        progress.write(f"Completed: {node_name}")

            # The graph is checkpointed. Read its latest state after the stream pauses.
            snapshot = app.get_state(config)
            result = dict(snapshot.values)

            interrupts = []
            for task in snapshot.tasks:
                interrupts.extend(getattr(task, "interrupts", ()) or ())

            if interrupts:
                result["__interrupt__"] = interrupts

            st.session_state.latest_result = result
            st.session_state.waiting_for_approval = bool(interrupts)
            progress.update(label="Draft stage finished", state="complete")

        except Exception as exc:
            progress.update(label="Draft generation failed", state="error")
            st.exception(exc)


# -----------------------------
# Display draft and agent data
# -----------------------------
result = st.session_state.latest_result

if result:
    st.divider()
    st.subheader("Supervisor Plan")
    st.write(result.get("supervisor_reasoning", ""))
    st.write("Selected agents:", result.get("selected_agents", []))

    left, right = st.columns(2)
    with left:
        st.subheader("Flight")
        st.markdown(result.get("flight_results", "") or "_No flight result_")
        st.subheader("Weather")
        st.markdown(result.get("weather_results", "") or "_No weather result_")
    with right:
        st.subheader("Hotels")
        st.markdown(result.get("hotel_results", "") or "_No hotel result_")
        st.subheader("Budget")
        st.markdown(result.get("budget_results", "") or "_No budget result_")

    st.subheader("Draft Itinerary")
    draft = result.get("itinerary", "")
    interrupt_items = result.get("__interrupt__", [])
    if interrupt_items:
        interrupt_value = getattr(interrupt_items[0], "value", {})
        if isinstance(interrupt_value, dict):
            draft = interrupt_value.get("draft_itinerary", draft)
    if draft:
        st.markdown(draft)
    else:
        st.info("No draft itinerary was returned in the graph state.")


# -----------------------------
# Human approval and final stream
# -----------------------------
if st.session_state.waiting_for_approval:
    st.divider()
    st.subheader("Human Approval")

    approved_choice = st.radio(
        "Do you approve this draft?",
        ["Yes", "No, revise it"],
        horizontal=True,
        key=f"approval_{st.session_state.thread_id}",
    )
    feedback = st.text_area(
        "Feedback (required when requesting a revision)",
        disabled=(approved_choice == "Yes"),
        key=f"feedback_{st.session_state.thread_id}",
    )

    if st.button("Submit Approval"):
        if approved_choice != "Yes" and not feedback.strip():
            st.warning("Please enter feedback so the agents know what to revise.")
        else:
            progress = st.status("Generating final travel plan...", expanded=True)
            answer_area = st.empty()

            def final_text_chunks():
                # Resume the paused graph on the SAME thread_id.
                for message_chunk, metadata in app.stream(
                    Command(
                        resume={
                            "approved": approved_choice == "Yes",
                            "feedback": feedback,
                        }
                    ),
                    config=config,
                    stream_mode="messages",
                ):
                    if metadata.get("langgraph_node") != "final_response":
                        continue

                    content = getattr(message_chunk, "content", "")
                    if isinstance(content, str) and content:
                        yield content
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block.get("text", "")
                                if text:
                                    yield text

            try:
                st.subheader("Final Travel Plan")
                streamed_answer = st.write_stream(final_text_chunks())

                # Read the committed final state after the graph has completed.
                final_snapshot = app.get_state(config)
                final_result = dict(final_snapshot.values)

                # Fallback for providers/configurations that return no message chunks.
                if not final_result.get("final_response") and isinstance(streamed_answer, str):
                    final_result["final_response"] = streamed_answer

                st.session_state.latest_result = final_result
                st.session_state.waiting_for_approval = False
                progress.update(label="Final travel plan completed", state="complete")

            except Exception as exc:
                progress.update(label="Final response failed", state="error")
                st.exception(exc)


# On later reruns, show the saved final response.
final_result = st.session_state.latest_result
if (
    final_result
    and final_result.get("final_response")
    and not st.session_state.waiting_for_approval
):
    st.divider()
    st.subheader("Saved Final Travel Plan")
    st.markdown(final_result["final_response"])
