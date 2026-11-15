from langgraph.types import interrupt
from langchain_core.messages import AIMessage

from src.tools.state import TravelState


def human_approval_agent(state: TravelState):

    feedback = interrupt(
        {
            "question": "Do you approve this itinerary?",
            "draft_itinerary": state.get("itinerary", ""),
            "approval_request": state.get("approval_request", ""),
            "expected_response": {
                "approved": True,
                "feedback": "Optional feedback for revision",
            },
        }
    )

    # Extract human response safely
    approved = feedback.get("approved", False)
    human_feedback = feedback.get("feedback", "")

  

    return {
        "approved": approved,
        "human_feedback": human_feedback,
        "messages": [
            AIMessage(
                content=f"Human approval received: {approved}"
            )
        ],
    }
