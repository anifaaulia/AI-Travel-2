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
    return python_weather.Client(format=python_weather.IMPERIAL)

search_tool = get_duckduckgo_search_tool()
weather_tool = get_weather_tool()
