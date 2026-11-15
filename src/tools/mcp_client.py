import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(override=True)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing in .env")

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY is missing in .env")


client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": (
                "https://mcp.tavily.com/mcp/"
                f"?tavilyApiKey={TAVILY_API_KEY}"
            ),
        },

        "weather": {
            "transport": "stdio",

            "command": (
                r"C:\Users\arghy\OneDrive\Desktop"
                r"\AI-TravelPlanning_LangGraph"
                r"\langgraphtravel_1\Scripts\python.exe"
            ),

            "args": [
                r"C:\Users\arghy\OneDrive\Desktop\AI-TravelPlanning_LangGraph\src\tools\custom_weather_mcp_server.py"
            ],

            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            },
        },
    }
)


# Tool references
search_tool = None
weather_tool = None
forecast_tool = None


async def initialize_mcp():

    global search_tool

    if search_tool is not None:
        return

    tools = await client.get_tools()

    print("\nAvailable MCP Tools:")

    for tool in tools:
        print(tool.name)

    search_tool = next(
        (tool for tool in tools if tool.name == "tavily_search"),
        None,
    )

    if search_tool is None:
        raise ValueError("tavily_search tool not found")


async def tavily_mcp_search(query: str):

    await initialize_mcp()

    return await search_tool.ainvoke(
        {"query": query}
    )


async def initialize_weather_tools():

    global weather_tool, forecast_tool

    if weather_tool is not None and forecast_tool is not None:
        return

    tools = await client.get_tools()

    weather_tool = next(
        (tool for tool in tools if tool.name == "get_current_weather"),
        None,
    )

    forecast_tool = next(
        (tool for tool in tools if tool.name == "get_forecast"),
        None,
    )

    if weather_tool is None:
        raise ValueError("get_current_weather tool not found")

    if forecast_tool is None:
        raise ValueError("get_forecast tool not found")


async def weather_mcp_search(city: str):

    await initialize_weather_tools()

    return await weather_tool.ainvoke(
        {"city": city}
    )


async def forecast_mcp_search(city: str):

    await initialize_weather_tools()

    return await forecast_tool.ainvoke(
        {"city": city}
    )
