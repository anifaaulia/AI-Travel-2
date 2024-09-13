from langchain.chat_models import ChatOpenAI
from tasks import AICrewMember
from tools import search_tool, weather_tool, get_weather_sync

def initialize_ai_model(api_key):
    return ChatOpenAI(
        model='gpt-4', 
        temperature=0.2, 
        api_key=api_key
    )

def create_ai_crew(openaigpt4):
    """Create the AI crew with different specializations, optionally using the search tool."""
    return [
        AICrewMember(
            name="Transport Specialist",
            role="transportation",
            task_prompt="""You are a travel agent specializing in transportation. Based on the following information, 
            recommend the best transportation options for traveling from {origin} to {cities} between {date_range}.""",
            openaigpt4=openaigpt4,
            use_search=True,  # Enable search for this member
            search_tool=search_tool
        ),
        AICrewMember(
            name="Accommodation Expert",
            role="accommodation",
            task_prompt="""You are an expert in travel accommodations. Based on the following information, recommend 
            the best places to stay in {cities} during the date range of {date_range} considering interests in {interests}.""",
            openaigpt4=openaigpt4,
            use_search=True,  # Enable search for this member
            search_tool=search_tool
        ),
        AICrewMember(
            name="Activity Planner",
            role="activities",
            task_prompt="""You are an activity planner with expertise in history and tourism. Based on the following information, 
            suggest the top activities and experiences to enjoy in {cities} given the date range {date_range} and interests 
            in {interests}. Include any relevant historical information or context about these places in your recommendations.""",
            openaigpt4=openaigpt4,
            use_search=True,  # Enable search for this member
            search_tool=search_tool
        ),
        AICrewMember(
            name="Historical Agent",
            role="historical",
            task_prompt="""You are a historian specializing in travel destinations. Based on the following information, 
            provide historical insights and suggest historically significant sites and activities in {cities} that align with 
            the date range {date_range} and interests in {interests}.""",
            openaigpt4=openaigpt4,
            use_search=True,  # Enable search for this member
            search_tool=search_tool
        ),
         AICrewMember(
            name="Weather Agent",
            role="weather",
            task_prompt="You are a weather expert. Provide current weather information for {cities} for the given date range.",
            openaigpt4=openaigpt4,
            use_weather=True,
            weather_tool=weather_tool
        )
    ]

async def generate_itinerary(data, ai_crew):
    results = {}
    for member in ai_crew:
        result = await member.perform_task(data)
        results[member.role] = result
    
    for member in ai_crew:
        if member.use_weather:
            # For the weather agent, we use the synchronous method
            weather_info = member.get_weather(data['cities'])
            results[member.role] = weather_info
        else:
            # Perform the asynchronous task for non-weather agents
            result = await member.perform_task(data)
            results[member.role] = result
    
    itinerary = f"""
    **Travel Itinerary:**
    
    - **Transportation:** {results.get('transportation', 'No data')}
    - **Accommodation:** {results.get('accommodation', 'No data')}
    - **Activities:** {results.get('activities', 'No data')}
    - **Historical Insights:** {results.get('historical', 'No data')}
    - **Weather Information:** {results.get('weather', 'No data')}       
    """
    
    return itinerary
