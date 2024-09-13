from langchain.schema import HumanMessage
from tools import search_tool, weather_tool, get_weather_sync
import asyncio

class AICrewMember:
    def __init__(self, name, role, task_prompt, openaigpt4,  use_search=False, 
                 search_tool=None, use_weather=False, weather_tool=None):
        self.name = name
        self.role = role
        self.task_prompt = task_prompt
        self.openaigpt4 = openaigpt4
        self.use_search = use_search
        self.search_tool = search_tool
        self.use_weather = use_weather
        self.weather_tool = weather_tool
        


    async def perform_task(self, data):
        # Format the prompt with the provided data
        formatted_prompt = self.task_prompt.format(**data)

        # Prepare the message in the expected format
        messages = [HumanMessage(content=formatted_prompt)]

        # Get the response from the GPT-4 model
        response = self.openaigpt4(messages)
        result = response.content.strip()

        # If use_search is True, perform a search using the search_tool
        if self.use_search and self.search_tool:
            search_query = f"{data['cities']} travel guide {data['date_range']} {self.role}"
            search_results = self.search_tool.run(search_query)

            # Process search results to append relevant information
            formatted_search_results = self.format_search_results(search_results)
            result += "\n\nSearch Results:\n" + formatted_search_results
                    
        return result

    def format_search_results(self, search_results):
        # Customize this method based on the format of search results
        formatted_results = ""
        for result in search_results:
            title = result.get('title', 'No Title')
            href = result.get('href', 'No URL')
            body = result.get('body', 'No Description')
            formatted_results += f"- **{title}**\n{href}\n{body}\n\n"
        return formatted_results
    
    def get_weather(self, city):
        # Use the synchronous version of the weather tool
        weather = get_weather_sync(self.weather_tool, city)
        forecasts = weather.forecasts[0]
        return f"Weather in {city}: {forecasts.sky_text}, Temperature: {forecasts.temperature}°C"