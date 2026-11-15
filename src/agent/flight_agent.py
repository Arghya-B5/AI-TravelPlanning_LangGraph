from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from src.tools.flight_tool import search_flights
from src.tools.state import TravelState
from src.util.lod import _llm_text

def flight_agent(state: TravelState):

    query = state["user_query"]
    constraints = state["trip_constraints"]
    destination = constraints["destination"]


    # Fetch MCP data
    airports = search_flights(destination)
    airlines = search_flights("")

    

    prompt = f"""
Create flight guidance for this trip.

User request:
{query}

Trip constraints:
{constraints}

Airport MCP data:
{str(airports)[:3000]}

Airline MCP data:
{str(airlines)[:3000]}

Include:
1. Likely departure and arrival airports.
2. Relevant airlines.
3. Estimated flight duration.
4. Estimated fare range.
5. Peak season warning.
6. Booking advice.

Clearly distinguish estimates from confirmed flight information.
"""

    result = _llm_text(
        "You are a flight planning specialist.",
        prompt,
    )

    
    return {
        "flight_results": result,
        "messages": [
            AIMessage(content="Flight agent completed.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
