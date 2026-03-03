from langchain.tools import tool

@tool 
def get_weather(location:str):
    """
    Get the current weather in a given location.
    """
    return f"The weather in {location} is sunny with a high of 25°C."