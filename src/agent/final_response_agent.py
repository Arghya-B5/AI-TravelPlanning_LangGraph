
from langchain_core.messages import AIMessage

from src.tools.state import TravelState
from src.util.lod import _llm_stream


def final_response_agent(state: TravelState):
    """Create the final plan while yielding model output through LangGraph streaming."""
    if state.get("approved", False):
        prompt = f"""
The human approved this draft itinerary.
Produce the final polished travel plan.

Draft itinerary:
{state.get('itinerary', '')}

Budget notes:
{state.get('budget_results', '')}
"""
    else:
        prompt = f"""
The human did not approve the draft.
Revise the itinerary according to the human feedback.

Original user request:
{state.get('user_query', '')}

Draft itinerary:
{state.get('itinerary', '')}

Human feedback:
{state.get('human_feedback', '')}

Budget notes:
{state.get('budget_results', '')}
"""

    chunks = []
    for text_chunk in _llm_stream(
        "You produce clear, accurate, user-ready travel plans.",
        prompt,
    ):
        chunks.append(text_chunk)

    full_response = "".join(chunks)

    return {
        "final_response": full_response,
        "messages": [AIMessage(content=full_response)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
