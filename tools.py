import os
from dotenv import load_dotenv
from langchain.tools import DuckDuckGoSearchRun
import python_weather
import asyncio


def load_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def get_duckduckgo_search_tool():
    return DuckDuckGoSearchRun()

def get_weather_tool():
    try:
        # Check if there's an existing event loop
        loop = asyncio.get_running_loop()
    except RuntimeError:  # No event loop is running
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Now create the weather client
    return python_weather.Client(unit=python_weather.IMPERIAL)

def get_weather_sync(weather_tool, location):
    # This runs the async function in a synchronous way
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(weather_tool.get(location))

search_tool = get_duckduckgo_search_tool()
weather_tool = get_weather_tool()
