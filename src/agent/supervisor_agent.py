import asyncio
import json
import os
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)



from src.util.lod import _json_from_llm, _llm_text
from src.tools.state import TravelState



def supervisor_agent(state: TravelState):
    query = state["user_query"]
            
    # INPUT GUARDRAIL
    guardrail_prompt = f"""
    Determine whether the following request is a valid travel planning request.

    Return only JSON in this format:

    {{
        "allowed": true,
        "reason": ""
    }}

    User request:
    {query}
    """

    guardrail_raw = _llm_text(
        "You are an input validation guardrail. Return strict JSON only.",
        guardrail_prompt,
    )

   
    guardrail_result = _json_from_llm(guardrail_raw)

   

    if not guardrail_result.get("allowed", False):
        reason = guardrail_result.get(
            "reason",
            "Request rejected by input guardrail."
        )

        return {
            "selected_agents": [],
            "trip_constraints": {},
            "supervisor_reasoning": reason,
            "final_response": reason,
            "messages": [
                AIMessage(content=f"Guardrail blocked request: {reason}")
            ],
            "llm_calls": state.get("llm_calls", 0) + 1,
        }


    # supervisor logic is starting from here:

    prompt = f"""
You are the supervisor of a real-world multi-agent travel planning system.

Decide which specialist agents are needed for this user request.

Available agents:
- flight_agent: use when flights, airports, airlines, routes, or airfare guidance are needed
- hotel_agent: use when hotels, stays, neighborhoods, or accommodation are needed
- weather_agent: use when weather, climate, season, packing, or forecast is useful
- budget_agent: use when budget, affordability, cost, or price constraints are mentioned
- itinerary_agent: almost always needed to produce the travel plan

Return only JSON with this schema:
{{
  "selected_agents": ["flight_agent", "hotel_agent", "weather_agent", "budget_agent", "itinerary_agent"],
  "trip_constraints": {{
    "destination": "",
    "origin": "",
    "duration": "",
    "budget": "",
    "travel_style": "",
    "special_preferences": []
  }},
  "reasoning": ""
}}

User request:
{query}
"""

 
    raw = _llm_text(
        "You route work to specialist agents. Return strict JSON only.",
        prompt,
    )


    parsed = _json_from_llm(raw)
   
   
    
    '''
    At first glance they look the same, but they're not:

    raw → string returned by the LLM
    parsed → Python dictionary created from that string

    If you really want to demonstrate the difference, add:

    print(type(raw))
    print(type(parsed))
    Output:

    <class 'str'>
    <class 'dict'>
    Yes, you can get output from a string, but it's much harder and less reliable.
    '''
    
    selected = parsed["selected_agents"]    

    return {
        "selected_agents": selected,
        "trip_constraints": parsed["trip_constraints"],
        "supervisor_reasoning": parsed["reasoning"],
        "messages": [AIMessage(content="Supervisor created the agent plan.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
