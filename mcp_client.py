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
        }


    }

)


# tools discovery
async def main():

    tools = await client.get_tools()

    print("\nAvailable MCP Tools:\n")

    for tool in tools:
        print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())
