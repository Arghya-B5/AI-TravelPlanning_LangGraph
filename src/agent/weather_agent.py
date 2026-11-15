import asyncio

from langchain_core.messages import AIMessage

from src.tools.mcp_client import (
    forecast_mcp_search,
    weather_mcp_search,
)
from src.tools.state import TravelState


async def get_weather_data(city: str):
    """Fetch current weather and forecast in one event loop."""

    weather_data = await weather_mcp_search(city)

    forecast_data = await forecast_mcp_search(city)

    return weather_data, forecast_data


def weather_agent(state: TravelState):

    constraints = state["trip_constraints"]
    city = constraints["destination"]

    # Run both MCP calls inside one event loop
    weather_data, forecast_data = asyncio.run(
        get_weather_data(city)
    )

    result = f"""
Current weather:
{weather_data}

Forecast:
{forecast_data}
"""

    return {
        "weather_results": result,
        "messages": [
            AIMessage(content="Weather agent completed.")
        ],
    }
