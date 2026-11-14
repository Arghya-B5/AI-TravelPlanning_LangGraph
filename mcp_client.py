import os
import asyncio
from pdb import main

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

#load_dotenv()
load_dotenv(override=True)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },
        "weather": {
                    "transport": "stdio",
                    "command": r"C:\Users\arghy\OneDrive\Desktop\AI-TravelPlanning_LangGraph\langgraphtravel_1\Scripts\python.exe",
                    "args": [
                        r"C:\Users\arghy\OneDrive\Desktop\AI-TravelPlanning_LangGraph\custom_weather_mcp_server.py"
                    ],
                    "env": {
                        "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
                    }
                }


    }

)
search_tool = None

async def initialize_mcp():

    global search_tool
    
    if search_tool is not None:
        return

    tools = await client.get_tools()

    print("\nAvailable MCP Tools:\n")

    for tool in tools:
        print(tool.name)

    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )

    



async def tavily_mcp_search(query: str):
    await initialize_mcp()
    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )
    return result


weather_tool = None
forecast_tool = None


async def initialize_weather_tools():

    global weather_tool, forecast_tool

    if weather_tool is not None:
        return

    tools = await client.get_tools()

    weather_tool = next(
        t for t in tools
        if t.name == "get_current_weather"
    )

    forecast_tool = next(
        t for t in tools
        if t.name == "get_forecast"
    )



async def weather_mcp_search(city: str):

    await initialize_weather_tools()

    return await weather_tool.ainvoke(
        {
            "city": city
        }
    )


async def forecast_mcp_search(city: str):

    await initialize_weather_tools()

    return await forecast_tool.ainvoke(
        {
            "city": city
        }
    )

from langchain_groq import ChatGroq

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=1500
)



def extract_destination(query: str):

    prompt = f"""
    Extract only the destination city or country.

    Query:
    {query}

    Return only destination name.
    """

    response = llm.invoke(prompt)

    return response.content.strip()

if __name__ == "__main__":
    asyncio.run(main())