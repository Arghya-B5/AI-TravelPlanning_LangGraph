from src.util.lod import  _llm_text
from src.tools.mcp_client import tavily_mcp_search

from langchain_core.messages import AIMessage
from src.tools.state import TravelState


def hotel_agent(state: TravelState):

    query = state["user_query"]
    constraints = state["trip_constraints"]

    destination = constraints["destination"]

   
    # Direct synchronous call
    result = tavily_mcp_search(query)



    prompt = f"""
You are an expert hotel recommendation specialist.

User request:
{query}

Destination:
{destination}

Search results:
{str(result)[:5000]}

Recommend suitable hotels based on:
1. Budget
2. Location
3. Hotel facilities
4. Approximate price
5. Nearby attractions
6. Booking advice

Do not invent availability or confirmed prices.
"""

    hotel_results = _llm_text(
        "You are a professional hotel planning specialist.",
        prompt
    )

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel agent completed.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }